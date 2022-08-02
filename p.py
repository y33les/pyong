import ast, lark.exceptions
from lark import Lark, Transformer
from astor import to_source
from lark.visitors import Visitor

class V(Visitor): # TODO: AST convertor (see lark.Tree API docs)
    def integer(self,tree):
        return ast.Constant(int(tree))

class T(Transformer): # FIXME: hand lark.Trees properly - maybe replace with a lark.Visitor (see above)?
    def integer(self,tree):
        return tree
        #return ast.Constant(int(tree))

    def character(self,tree):
        return ast.Constant(str(tree))

    def real(self,tree):
        return ast.Constant(float(tree))

    def string(self,tree):
        return ast.Constant(str(tree))

    def symbol(self,tree):
        return ast.Name(tree,ctx=ast.Load())

    def quotsym(self,tree):
        return ast.Call(ast.Name(id='quote',ctx=ast.Load()),ast.Name(tree,ctx=ast.Load()),keywords=[]) # TODO: implement quote

    def list(self,tree):
        return ast.List(elts=tree[0].children,ctx=ast.Load())

    #def lexemeclass(self,tree):
    #    return ast.Expression(tree[0])

    #def factor(self,tree):
    #    return ast.Expression(tree[0])

    #def expression(self,tree):
    #    return ast.Expression(tree[0])

    #def program(self,tree):
    #    return ast.Expression(tree[0])

    def start(self,tree):
        return ast.fix_missing_locations(ast.Expression(tree[0]))

with open('g.lark') as g:
    parser = Lark(g)

t = Transformer()

def parse(text):
    tree = parser.parse(text)
    return t.transform(tree)

if __name__ == '__main__':
    while True:
        try:
            text = input('pyong > ')
            if (text=='q'): break # FIXME: proper solution required in the future
            result = parser.parse(text)
            print(result.pretty()) # show Lark tree (for now)
            #print("  => "+to_source(result)) # AST -> equivalent Python code
            #eval(compile(result,filename='<ast>',mode='eval')) # evaluate AST
        except lark.exceptions.UnexpectedCharacters as e:
            print(e)
        except lark.exceptions.UnexpectedEOF as e:
            print(e)
        except EOFError:
            break
