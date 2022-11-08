# Parser

import ast,o,a,u
from lark import Transformer
from itertools import chain
from astor import to_source
from astunparse import dump

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
             '-': attrWrap('o','kNegate'),            # Negate # Was '=-' for some reason?
             '~':  attrWrap('o','kNot'),              # Not
             '?':  attrWrap('o','kRange'),            # Range
             '%':  attrWrap('o','kReciprocal'),       # Reciprocal
             '|':  attrWrap('o','kReverse'),          # Reverse
             '^':  attrWrap('o','kShape'),            # Shape
             '#':  attrWrap('o','kSize'),             # Size
             '+': attrWrap('o','kTranspose'),         # Transpose # Was '=+' for some reason?
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
    # N.B.: You tried changing this back as lists seemed more intuitive,
    #       but Python can't have lists as dict keys because they are
    #       mutable (but it can have nice, immutable tuples)
    def list(self,tree):
        return ast.Tuple(elts=tree,ctx=ast.Load())

    # arglists are just Python lists of AST nodes ready for inclusion in the supernode
    def arglist(self,tree):
        return tree

    def projarg01(self,tree):
        return [None]+tree

    def projarg10(self,tree):
        return tree+[None]

    def projarg011(self,tree):
        return [None]+tree

    def projarg101(self,tree):
        return [tree[0],None,tree[1]]

    def projarg110(self,tree):
        return tree+[None]

    def projarg001(self,tree):
        return [None,None]+tree

    def projarg010(self,tree):
        return [None]+tree+[None]

    def projarg100(self,tree):
        return tree+[None,None]

    def projarg(self,tree):
        return tree[0]

    def function(self,tree):
        # TODO: {program}
        # TODO: {program}program
        if False: # TODO: remove
            pass
        elif isinstance(tree[0],ast.Name): # symbol projarg # TODO: is this exclusive?  nothing else getting caught here?
            # TODO: check if this still works if any of the actual arguments are None
            if len(tree[1])==2:
                if tree[1][0]==None and tree[1][1]!=None:                        # projarg01
                    # TODO: Does this interfere with existing values named 'x'?
                    return ast.Lambda(args=ast.arguments(posonlyargs=[],args=[ast.arg(arg='x')],kwonlyargs=[],kw_defaults=[],defaults=[]),body=ast.Call(tree[0],args=[ast.Name('x',ctx=ast.Load()),tree[1][1]],keywords=[]))
                elif tree[1][0]!=None and tree[1][1]==None:                      # projarg10
                    return ast.Lambda(args=ast.arguments(posonlyargs=[],args=[ast.arg(arg='y')],kwonlyargs=[],kw_defaults=[],defaults=[]),body=ast.Call(tree[0],args=[tree[1][0],ast.Name('y',ctx=ast.Load())],keywords=[]))
                else:
                    raise Exception("2-projarg with no Nones or both Nones")
            elif len(tree[1])==3:
                if tree[1][0]==None and tree[1][1]!=None and tree[1][2]!=None:   # projarg011
                    return ast.Lambda(args=ast.arguments(posonlyargs=[],args=[ast.arg(arg='x')],kwonlyargs=[],kw_defaults=[],defaults=[]),body=ast.Call(tree[0],args=[ast.Name('x',ctx=ast.Load()),tree[1][1],tree[1][2]],keywords=[]))
                elif tree[1][0]!=None and tree[1][1]==None and tree[1][2]!=None: # projarg101
                    return ast.Lambda(args=ast.arguments(posonlyargs=[],args=[ast.arg(arg='y')],kwonlyargs=[],kw_defaults=[],defaults=[]),body=ast.Call(tree[0],args=[tree[1][0],ast.Name('y',ctx=ast.Load()),tree[1][2]],keywords=[]))
                elif tree[1][0]!=None and tree[1][1]!=None and tree[1][2]==None: # projarg110
                    return ast.Lambda(args=ast.arguments(posonlyargs=[],args=[ast.arg(arg='z')],kwonlyargs=[],kw_defaults=[],defaults=[]),body=ast.Call(tree[0],args=[tree[1][0],tree[1][1],ast.Name('z',ctx=ast.Load())],keywords=[]))
                elif tree[1][0]==None and tree[1][1]==None and tree[1][2]!=None: # projarg001
                    return ast.Lambda(args=ast.arguments(posonlyargs=[],args=[ast.arg(arg='x'),ast.arg(arg='y')],kwonlyargs=[],kw_defaults=[],defaults=[]),body=ast.Call(tree[0],args=[ast.Name('x',ctx=ast.Load()),ast.Name('y',ctx=ast.Load()),tree[1][2]],keywords=[]))
                elif tree[1][0]==None and tree[1][1]!=None and tree[1][2]==None: # projarg010
                    return ast.Lambda(args=ast.arguments(posonlyargs=[],args=[ast.arg(arg='x'),ast.arg(arg='z')],kwonlyargs=[],kw_defaults=[],defaults=[]),body=ast.Call(tree[0],args=[ast.Name('x',ctx=ast.Load()),tree[1][1],ast.Name('z',ctx=ast.Load())],keywords=[]))
                elif tree[1][0]!=None and tree[1][1]==None and tree[1][2]==None: # projarg100
                    return ast.Lambda(args=ast.arguments(posonlyargs=[],args=[ast.arg(arg='y'),ast.arg(arg='z')],kwonlyargs=[],kw_defaults=[],defaults=[]),body=ast.Call(tree[0],args=[tree[1][0],ast.Name('y',ctx=ast.Load()),ast.Name('z',ctx=ast.Load())],keywords=[]))
                else:
                    raise Exception("3-projarg with the wrong number of Nones")
            else:
                raise Exception("projarg with neither 2 nor 3 args")
        else:
            raise Exception("function that isn't a {program}, {program}program or symbol projarg")

    def conditional(self,tree):
        if ((len(tree)-3)%2)!=0:
            raise Exception("wrong number of clauses in a conditional")
        elif len(tree)==3: # if,then,else
            return ast.IfExp(test=tree[0],body=tree[1],orelse=tree[2])
        else:
            return ast.IfExp(test=tree[0],body=tree[1],orelse=self.conditional(tree[2:])) # careful of recursion depth?

    def factor(self,tree):
        if len(tree)==1: # lexemeclass, function, (expression), conditional, list, dictionary
            return tree[0]
        elif len(tree)==2: # symbol+arglist, function+arglist, monad+expression
            # FIXME: better to check ifinstance(tree[1],list) for arglists?
            if isinstance(tree[0],ast.Name): # symbol+arglist
                return ast.Call(tree[0],args=tree[1],keywords=[])
            elif isinstance(tree[0],ast.Lambda): # function+arglist # TODO: is this exclusive?  nothing else getting caught here?
                return ast.Call(tree[0],args=tree[1],keywords=[])
                # FIXME once function is implemented
                # TODO: so we'll need to return a Call of tree[-1], but what about the side-effects?
                pass # TODO
            elif isinstance(tree[0],ast.Attribute): # monad+expression # TODO: is this exclusive?  nothing else getting caught here?
                return ast.Call(func=tree[0],args=[tree[1]],keywords=[])
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

    def operator(self,tree):
        return tree[0]

    def monad(self,tree):
        if len(tree)==1: # No adverbs
            return monadOps[tree[0].value]
        else:            # At least one adverb
            raise Exception("NYI: monad with adverb+") # FIXME

    def dyad(self,tree):
        if len(tree)==1: # No adverbs
            return dyadOps[tree[0].value]
        else:            # At least one adverb
            raise Exception("NYI: dyad with adverb+") # FIXME

    def expression(self,tree):
        if len(tree)==1:
            return tree[0]
        elif len(tree)==3:
            return ast.Call(func=tree[1],args=[tree[0],tree[2]],keywords=[])
        else:
            raise Exception("you've got an expression which is neither a factor nor a factor, dyad, expression")

    def program(self,tree):
        return tree

    def start(self,tree):
        return list(map(lambda n: ast.fix_missing_locations(ast.Expression(n)), flatten(tree))) # using flattened program list - N.B.: relies on there not being any lists in the tree below it!

    # TODO: implement \ help functions

    def quit(self,tree): # TODO: is this the correct way to quit?
        quit()           # TODO: ignore/throw exception if running inside python rather than the pyong interpreter

# For testing
from lark import Lark
with open('g.lark') as g:
    p = Lark(g)
t = T()
def d(e):
    for i in t.transform(p.parse(e)):
        print(dump(i)+"\n")
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
