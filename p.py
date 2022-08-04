# Parser

import ast,o,a,u
from lark import Transformer
from astor import to_source

# Generate an AST node referencing an object a in package p
def attrWrap(p,a):
    return ast.Attribute(value=ast.Name(id=p,ctx=ast.Load()),attr=a,ctx=ast.Load())

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

    def character(self,tree): # TODO: Remove 0c prefix
        return ast.Constant(str(tree[0].value))

    def real(self,tree):
        return ast.Constant(float(tree[0].value))

    def string(self,tree): # TODO: Remove quotes
        return ast.Constant(str(tree[0].value))

    def symbol(self,tree):
        return ast.Name(tree[0].value,ctx=ast.Load())

    def quotsym(self,tree):
        return ast.Call(ast.Attribute(value=ast.Name(id='u',ctx=ast.Load()),attr='quote',ctx=ast.Load()),args=[tree[0]],keywords=[]) # FIXME: possible interference if another package imported as f?  also requires f to be imported in whatever's calling this

    def lexemeclass(self,tree):
        return tree[0]

    def list(self,tree):
        return ast.List(elts=tree,ctx=ast.Load())

    def factor(self,tree):
        return tree[0] # FIXME: This only works for lexemeclasses!!

    def expression(self,tree):
        return tree[0] # FIXME: This only works for single expressions!!

    def program(self,tree):
        return tree[0] # FIXME: This only works for single expressions!!

    # TODO: implement \ help functions

    def quit(self,tree):
        quit()

    def start(self,tree):
        return ast.fix_missing_locations(ast.Expression(tree[0])) # FIXME: This only works for single expressions!!
