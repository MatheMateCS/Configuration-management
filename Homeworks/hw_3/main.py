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

def is_str(s):
    return re.fullmatch(r"\'[^\']*\'", s) != None

output = ''
def to_output(str):
    global output
    output += str + '\n'

def serialize(obj, name='', indent='', delim='  '):
    id = ''
    if name != '':
        id = f" name='{name}'"
    if type(obj) == float:
        to_output(indent + f"<number{id}>{obj}</number>")
    elif type(obj) == str:
        if is_str(obj):
            to_output(indent + f"<string{id}>{obj[1:-1]}</string>")
        else:
            if obj in constants:
                serialize(constants[obj], name=name, indent=indent)
            else:
                print(highligth(f"There is no constant '{obj}' declared in this scope!"))
                exit(0)
    elif type(obj) == list:
        to_output(indent + f"<array{id}>")
        for el in obj:
            serialize(el, indent=indent+delim)
        to_output(indent + "</array>")
    elif type(obj) == dict:
        to_output(indent + f"<dictionary{id}>")
        for val in obj.items():
            to_output(indent + delim + f"<entry key='{val[0]}'>")
            serialize(val[1], indent=indent+2*delim)
            to_output(indent + delim + '</entry>')
        to_output(indent + '</dictionary>')
    

src = '''
    (def name 2)
    (def new $(name))
    (def lst [$(new), 2])
    '''
src2 = '''
    // There is a program
    (def num 5)
    (def typer [-9, 'plus', 7])
    ( def dict { ip => [9, 3], mem => 2, sub => {  cnt=>$(num), val => 'true' } } )
    ( def str 'Hello, World!' )
    '''

obj = parse(src2, main)
ss = obj.stack[0]
constants = dict()
for i in range(len(ss)):
    if i % 2 == 0:
        constants[ss[i]] = ss[i+1]
print(constants)
for d in constants.items():
    serialize(d[1], name=d[0])
print(output[:-1])

def test():
    pass
    # for n in s.glob['tab'].values():
    #     print(n.stack)

test()
# def main():
#     ...

# if __name__ == '__main__':
#     test()
    


