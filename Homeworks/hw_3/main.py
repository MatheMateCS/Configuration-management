import re
import sys
from peco import State, parse, program


class Converter:
    @staticmethod
    def is_str(s: str) -> bool:
        return re.fullmatch(r"\'[^\']*\'", s) != None
    
    @staticmethod
    def highligth(s: str, type: str = 'err', beg: int = 0, end: int = -1) -> str:
        lb, rb = '\033[91m', '\033[0m'
        if type == 'ok':
            lb = '\033[92m'
        if end < 0:
            return s[:beg] + lb + s[beg:len(s)+end+1] + rb
        return s[:beg] + lb + s[beg:end] + rb + s[end:]

    def __init__(self) -> None:
        self.src: str = ''
        self.obj: State = None
        self.constants: dict = dict()
        self.xml: str = ''
    
    def load(self, text: str) -> None:
        self.src = text

    def __parse(self) -> None:
        self.obj = parse(self.src, program)

    def __check_syntax(self) -> bool:
        if not self.obj.ok:
            err_ptr = self.obj.glob['err']
            slice = self.obj.text[:err_ptr+1]
            num = slice.count('\n')
            pos = slice.rfind('\n')
            print(Converter.highligth(f"Синтаксическая ошибка в {num} строке:"))
            print(Converter.highligth(self.obj.text.split('\n')[num], "err", err_ptr-pos-1, err_ptr-pos))
            return False
        print(Converter.highligth("Синтаксических ошибок не обнаружено", type='ok'))
        return True

    def __to_output(self, str: str) -> None:
        self.xml += str + '\n'

    def __serialize(self, obj: State, name: str = '', indent: str = '', delim: str = '  ') -> None:
        id = ''
        if name != '':
            id = f" name='{name}'"
        if type(obj) == float:
            self.__to_output(indent + f"<number{id}>{obj}</number>")
        elif type(obj) == str:
            if Converter.is_str(obj):
                self.__to_output(indent + f"<string{id}>{obj[1:-1]}</string>")
            else:
                if obj in self.constants:
                    self.__serialize(self.constants[obj], name=name, indent=indent)
                else:
                    print(Converter.highligth(f"There is no constant '{obj}' declared in this scope!"))
                    exit(-1)
        elif type(obj) == list:
            self.__to_output(indent + f"<array{id}>")
            for el in obj:
                self.__serialize(el, indent=indent+delim)
            self.__to_output(indent + "</array>")
        elif type(obj) == dict:
            self.__to_output(indent + f"<dictionary{id}>")
            for val in obj.items():
                self.__to_output(indent + delim + f"<entry key='{val[0]}'>")
                self.__serialize(val[1], indent=indent+2*delim)
                self.__to_output(indent + delim + '</entry>')
            self.__to_output(indent + '</dictionary>')

    def convert(self) -> str:
        self.__parse()
        if(self.__check_syntax()):
            stack = self.obj.stack[0]
            for i in range(len(stack)):
                if i % 2 == 0:
                    self.constants[stack[i]] = stack[i+1]
            for cst in self.constants.items():
                self.__serialize(cst[1], name=cst[0])
        else:
            exit(-1)
        return self.xml[:-1]

  
test1 = '''
    (def name 2)
    (def new $(name))
    (def lst [$(new), 2])
    '''
test2 = '''
    // There is a program
    (def num 5)
    (def typer [-9, 'plus', 7])
    ( def dict { ip => [9, 3], mem => 2, sub => {  cnt=>$(num), val => 'true' } } )
    ( def str 'Hello, World!' )
    '''

def read_cmd() -> str:
    input = ''
    for line in sys.stdin:
        input += line
    return input

def main():
    converter = Converter()
    print(read_cmd())

if __name__ == '__main__':
    main()
    


