# Pyong interpreter

import p,o,a,u,lark.exceptions
from lark import Lark

# FIXME: evaluate can't find Python-defined variables
#        e.g. a=2 then pyong.evaluate(":a") can't find a
# TODO:  implement tacit?

def parseTree(text):
    with open('g.lark') as g:
        parser = Lark(g)
    return parser.parse(text)

def evaluate(text):
    transformer = p.T()
    with open('g.lark') as g:
        parser = Lark(g)
    result = transformer.transform(parser.parse(text))
    return eval(compile(result,filename='<ast>',mode='eval'))

    # FIXME: this only works for expressions, not statements
    #        for statements (e.g. assignment), we need something like this:
    #
    #        eval(
    #            compile(
    #                ast.fix_missing_locations(
    #                    ast.Module( # Note Module, not Expression
    #                        [ast.Assign(
    #                            targets=[ast.Name(id='foo',ctx=ast.Store())],
    #                            value=ast.Constant(2))],
    #                        type_ignores=[])),
    #                filename='<ast>',
    #                mode='exec')) # Note 'exec', not 'eval'
    #
    #        statements discard their results; expressions don't
    #        https://stackoverflow.com/a/68944101

if __name__ == '__main__':
    transformer = p.T()
    with open('g.lark') as g:
        parser = Lark(g)
    while True:
        try:
            text = input('pyong > ')
            #result = parser.parse(text)
            #print(result.pretty()) # show Lark tree (for now)
            #result = transformer.transform(result)
            #print("        => "+to_source(result)) # AST -> equivalent Python code
            print(evaluate(text))
        except lark.exceptions.UnexpectedCharacters as e:
            print(e)
        except lark.exceptions.UnexpectedEOF as e:
            print(e)
        except NameError as e:
            print(e)
        except EOFError:
            break
