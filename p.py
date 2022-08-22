# Parser

import ast,o,a,u
from lark import Transformer
from itertools import chain
from astor import to_source

# Generate an AST node referencing an object a in package p
def attrWrap(p,a):
    return ast.Attribute(value=ast.Name(id=p,ctx=ast.Load()),attr=a,ctx=ast.Load())

# Flatten an arbitrarily nested list (TODO: Does this hit the stack limit for recursion?)
# See 'Flatten List of Lists Using Lambda' on https://stackabuse.com/python-how-to-flatten-list-of-lists/
flatten = lambda l: [e for i in l for e in flatten(i)] if type(l) is list else [l]

# Monadic operator lookup table
monadOps =  {'@':  attrWrap('o','kAtom'),             # Atom
             ':#': attrWrap('o','kChar'),             # Char
             '!':  attrWrap('o','kEnumerate'),        # Enumerate
             '&':  attrWrap('o','kExpandWhere'),      # Expand/Where
             '*':  attrWrap('o','kFirst'),            # First
             '_':  attrWrap('o','kFloor'),            # Floor
             '$':  attrWrap('o','kFormat'),           # Format
             '>':  attrWrap('o','kGradeDown'),        # Grade-Down
             '<':  attrWrap('o','kGradeUp'),          # Grade-Up
             '=':  attrWrap('o','kGroup'),            # Group
             ',':  attrWrap('o','kList'),             # List
             '=-': attrWrap('o','kNegate'),           # Negate
             '~':  attrWrap('o','kNot'),              # Not
             '?':  attrWrap('o','kRange'),            # Range
             '%':  attrWrap('o','kReciprocal'),       # Reciprocal
             '|':  attrWrap('o','kReverse'),          # Reverse
             '^':  attrWrap('o','kShape'),            # Shape
             '#':  attrWrap('o','kSize'),             # Size
             '=+': attrWrap('o','kTranspose'),        # Transpose
             ':_': attrWrap('o','kUndefined')}        # Undefined

# Dyadic operator lookup table
dyadOps =   {':=': attrWrap('o','kAmend'),            # Amend
             ':-': attrWrap('o','kAmendInDepth'),     # Amend-in-Depth
             ':_': attrWrap('o','kCut'),              # Cut
             '::': attrWrap('o','kDefine'),           # Define
             '%':  attrWrap('o','kDivide'),           # Divide
             '_':  attrWrap('o','kDrop'),             # Drop
             '=':  attrWrap('o','kEqual'),            # Equal
             '?':  attrWrap('o','kFind'),             # Find
             ':$': attrWrap('o','kForm'),             # Form
             '$':  attrWrap('o','kFormat2'),          # Format2
             '@':  attrWrap('o','kIndexApply'),       # Index/Apply
             ':@': attrWrap('o','kIndexInDepth'),     # Index-in-Depth
             ':%': attrWrap('o','kIntegerDivide'),    # Integer-Divide
             ',':  attrWrap('o','kJoin'),             # Join
             '<':  attrWrap('o','kLess'),             # Less
             '~':  attrWrap('o','kMatch'),            # Match
             '|':  attrWrap('o','kMaxOr'),            # Max/Or
             '&':  attrWrap('o','kMinAnd'),           # Min/And
             '-':  attrWrap('o','kMinus'),            # Minus
             '>':  attrWrap('o','kMore'),             # More
             '+':  attrWrap('o','kPlus'),             # Plus
             '^':  attrWrap('o','kPower'),            # Power
             ':^': attrWrap('o','kReshape'),          # Reshape
             '!':  attrWrap('o','kRemainder'),        # Remainder
             ':+': attrWrap('o','kRotate'),           # Rotate
             ':#': attrWrap('o','kSplit'),            # Split
             '#':  attrWrap('o','kTake'),             # Take
             '*':  attrWrap('o','kTimes')}            # Times

# Monadic adverb lookup table
monadAdvs = {"'":   attrWrap('a','kEach'),            # Each
             ":'":  attrWrap('a','kEachPair'),        # Each-Pair
             '/':   attrWrap('a','kOver'),            # Over
             ':~':  attrWrap('a','kConverge'),        # Converge
             '\\':  attrWrap('a','kScanOver'),        # Scan-Over
             '\\~': attrWrap('a','kScanConverging')}  # Scan-Converging

# Dyadic adverb lookup table
dyadAdvs =  {"'":   attrWrap('a','kEach2'),           # Each2
             ':\\': attrWrap('a','kEachLeft'),        # Each-Left
             ':/':  attrWrap('a','kEachRight'),       # Each-Right
             '/':   attrWrap('a','kOverNeutral'),     # Over-Neutral
             ':~':  attrWrap('a','kWhile'),           # While
             ':*':  attrWrap('a','kIterate'),         # Iterate
             '\\':  attrWrap('a','kScanOverNeutral'), # Scan-Over-Neutral
             '\\~': attrWrap('a','kScanWhile'),       # Scan-While
             '\\*': attrWrap('a','kScanIterating')}   # Scan-Iterating

# Transformer from Lark parse tree to Python AST
class T(Transformer):
    def integer(self,tree):
        return ast.Constant(int(tree[0].value))

    def character(self,tree):
        return ast.Constant(str(tree[0].value[-1])) # TODO: Any Unicode situations this won't work for?

    def real(self,tree):
        return ast.Constant(float(tree[0].value))

    def string(self,tree):
        return ast.Constant(str(tree[0].value[1:-1:]))

    def symbol(self,tree):
        return ast.Name(tree[0].value,ctx=ast.Load())

    def quotsym(self,tree):
        return ast.Call(ast.Attribute(value=ast.Name(id='u',ctx=ast.Load()),attr='quote',ctx=ast.Load()),args=[tree[0]],keywords=[]) # FIXME: possible interference if another package imported as u?  also requires u to be imported in whatever's calling this

    def lexemeclass(self,tree):
        return tree[0]

    # Klong lists are immutable, so we use Python tuples instead of lists
    # (this also solves the dictionary lists-as-keys problem)
    def list(self,tree):
        return ast.Tuple(elts=tree,ctx=ast.Load())

    # arglists are just Python lists of AST nodes ready for inclusion in the supernode
    def arglist(self,tree):
        return tree

    def factor(self,tree):
        if len(tree)==1: # lexemeclass
            return tree[0]
        elif len(tree)==2: # symbol+arglist, function+arglist, monad+expression
            # FIXME: better to check ifinstance(tree[1],list) for arglists?
            if isinstance(tree[0],ast.Name): # symbol+arglist
                return ast.Call(tree[0],args=tree[1],keywords=[])
            elif isinstance(tree[0],ast.Expression): # function+arglist
                # FIXME when function implemented: is it definitely a Expression?
                pass # TODO
            elif isinstance(tree[0],ast.Call): # monad+expression
                # FIXME when monad implemented: is it definitely a Call?
                pass # TODO
            else:
                raise Exception("2-element factor but not a symbol, function or monad first?")
        else:
            raise Exception("a factor with more than 2 elements?  smells like a parser bug to me")

    def tuple(self,tree):
        return ast.Dict(keys=[tree[0]],values=[tree[1]])

    def dictionary(self,tree):
        d = tree[0]
        if len(tree)==1:
            return d
        else:
            for i in tree[1::]:
                d.keys=d.keys+i.keys
                d.values=d.values+i.values
            return d

    def expression(self,tree):
        if len(tree)==1:
            return ast.Expression(tree[0])
        else:
            pass # TODO: implement 'factor dyad expression' version

    def program(self,tree):
        if len(tree)==1:
            return [ast.fix_missing_locations(tree[0])]
        else:
            return list(map(lambda n: ast.fix_missing_locations(n), flatten(tree))) # using flattened program list - N.B.: relies on there not being any lists in the tree below it!

    # TODO: implement \ help functions

    def quit(self,tree):
        quit() # TODO: is this the correct way to quit?
               # TODO: ignore/throw exception if running inside python rather than the pyong interpreter

    def start(self,tree):
        return tree[0]

# For testing
from lark import Lark
with open('g.lark') as g:
    p = Lark(g)
t = T()
def dump(e):
    return list(map(ast.dump,t.transform(p.parse(e))))
def pp(e):
    print(p.parse(e).pretty())
def src(e):
    for i in t.transform(p.parse(e)):
        print(to_source(i))
def ev(e):
    l = t.transform(p.parse(e))
    for i in l[0:-1]:
        eval(compile(i,filename='<ast>',mode='eval'))
    return eval(compile(l[-1],filename='<ast>',mode='eval'))
