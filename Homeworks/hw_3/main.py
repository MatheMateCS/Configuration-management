from peco import *


def highligth(s, type='err', beg=0, end=-1) -> str:
    lb, rb = '\033[91m', '\033[0m'
    if type == 'ok':
        lb = '\033[92m'
    if end < 0:
        return s[:beg] + lb + s[beg:len(s)+end+1] + rb
    return s[:beg] + lb + s[beg:end] + rb + s[end:]

def check_syntax(s: State) -> bool:
    if not s.ok:
        err_ptr = s.glob['err']
        slice = s.text[:err_ptr+1]
        num = slice.count('\n')
        pos = slice.rfind('\n')
        print(highligth(f"Синтаксическая ошибка в {num} строке:"))
        print(highligth(s.text.split('\n')[num], "err", err_ptr-pos-1, err_ptr-pos))
        return False
    print(highligth("Синтаксических ошибок не обнаружено", type='ok'))
    return True

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


