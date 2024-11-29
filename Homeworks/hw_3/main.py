import re
import sys
from peco import State, parse, program


# Implements the process of translating from configuration language to xml format
class Converter:

    # Checks is it a string value or name of constant
    @staticmethod
    def is_str(s: str) -> bool:
        return re.fullmatch(r"\'[^\']*\'", s) != None

    # Highlights part of string with certain color  
    @staticmethod
    def highligth(s: str, type: str = 'err', beg: int = 0, end: int = -1) -> str:
        lb, rb = '\033[91m', '\033[0m'
        if type == 'ok':
            lb = '\033[92m'
        if end < 0:
            return s[:beg] + lb + s[beg:len(s)+end+1] + rb
        return s[:beg] + lb + s[beg:end] + rb + s[end:]

    # Standart constructor
    def __init__(self) -> None:
        self._src: str = ''
        self._obj: State = None
        self._constants: dict = dict()
        self._xml: str = ''
    
    # Loads the source program written in configuration language
    def load(self, text: str) -> None:
        self._src = text

    # Parses code according to peco rules
    def __parse(self) -> None:
        self._obj = parse(self._src, program)

    # Checks correctness of source code
    def __check_syntax(self) -> bool:
        if not self._obj.ok:
            err_ptr = self._obj.glob['err']
            slice = self._obj.text[:err_ptr+1]
            num = slice.count('\n')
            pos = slice.rfind('\n')
            print(Converter.highligth(f"Синтаксическая ошибка в {num} строке:"))
            print(Converter.highligth(self._obj.text.split('\n')[num], "err", err_ptr-pos-1, err_ptr-pos))
            return False
        print(Converter.highligth("Синтаксических ошибок не обнаружено", type='ok'))
        return True

    # Appends another string to the xml result 
    def __to_output(self, str: str) -> None:
        self._xml += str + '\n'

    # Serializes code element to xml format
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
                if obj in self._constants:
                    self.__serialize(self._constants[obj], name=name, indent=indent)
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

    # Main method that converts source code to xml
    def convert(self) -> str:
        self.__parse()
        if(self.__check_syntax()):
            stack = self._obj.stack[0]
            for i in range(len(stack)):
                if i % 2 == 0:
                    self._constants[stack[i]] = stack[i+1]
            for cst in self._constants.items():
                self.__serialize(cst[1], name=cst[0])
        else:
            exit(-1)
        return self._xml[:-1]


# Reads from standard input
def read_cmd() -> str:
    input = ''
    for line in sys.stdin:
        input += line
    return input

def main():
    converter = Converter()
    converter.load(read_cmd())
    print(converter.convert())

if __name__ == '__main__':
    main()
    


