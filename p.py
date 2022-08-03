import ast, f
from lark import Transformer
from astor import to_source

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
        return ast.Call(ast.Attribute(value=ast.Name(id='f',ctx=ast.Load()),attr='quote',ctx=ast.Load()),args=[tree[0]],keywords=[]) # FIXME: possible interference if another package imported as f?  also requires f to be imported in whatever's calling this

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
