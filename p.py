import ast, lark.exceptions, f
from lark import Lark, Transformer
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

    def quit(self,tree):
        quit()

    def start(self,tree):
        return ast.fix_missing_locations(ast.Expression(tree[0])) # FIXME: This only works for single expressions!!

if __name__ == '__main__':
    with open('g.lark') as g:
        p = Lark(g)
    t = T()
    while True:
        try:
            text = input('pyong > ')
            result = p.parse(text)
            #print(result.pretty()) # show Lark tree (for now)
            result = t.transform(result)
            print("        => "+to_source(result)) # AST -> equivalent Python code
            eval(compile(result,filename='<ast>',mode='eval')) # evaluate AST
        except lark.exceptions.UnexpectedCharacters as e:
            print(e)
        except lark.exceptions.UnexpectedEOF as e:
            print(e)
        except NameError as e:
            print(e)
        except EOFError:
            break
