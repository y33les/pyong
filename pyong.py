import p,f,lark.exceptions
from lark import Lark

# FIXME: evaluate can't find Python-defined variables
#        e.g. a=2 then pyong.evaluate(":a") can't find a

def evaluate(text):
    transformer = p.T()
    with open('g.lark') as g:
        parser = Lark(g)
    result = transformer.transform(parser.parse(text))
    return eval(compile(result,filename='<ast>',mode='eval'))

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
