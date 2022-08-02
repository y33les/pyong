import ast
from lark import Lark, Transformer
from astor import to_source

with open('g.lark') as g:
    parser = Lark(g)

def parse(text):
    tree = parser.parse(text)
    return tree # transformer.transform(tree)

if __name__ == '__main__':
    while True:
        try:
            text = input('pyong > ')
            if (text=='q'): break # FIXME: proper solution required in the future
            result = parser.parse(text)
            print(result.pretty()) # show Lark tree (for now)
            # print("  => "+to_source(result)) # AST -> equivalent Python code
            # eval(compile(result,filename='<ast>',mode='eval') # evaluate AST
        except EOFError:
            break
