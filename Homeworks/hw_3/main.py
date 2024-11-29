from peco import *


def test():
    src = '''
    (def name 2)
    (def new $(name))
    (def lst [$(new), 2])
    '''
    src2 = '''
    // There is a program
    ( def dict { ip => [9, 3], mem => 2, sub => {  cnt=>$(num), val => 'true' } } )
    ( def str 'Hello, World!' )
    '''
    s = parse(src2, main)
    print(s)
    
test()


