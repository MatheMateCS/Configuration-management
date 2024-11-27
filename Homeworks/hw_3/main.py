from peco import *


mknum = to(lambda n: float(n))
mkstr = to(lambda s: s[1:-1])
mkarr = to(lambda a: list(a))
mkdict = to(lambda o: dict(o))

ws = many(eat(r'\s+|//.*'))
token = lambda f: memo(seq(ws, f, ws))
tok = lambda c: token(push(eat(c)))
skip = lambda c: token(eat(c))

number_rule = seq(tok(r'[-+]?\d+\.?\d*'), mknum)
string_rule = seq(tok(r'\'[^\']*\''), mkstr)

value_rule = lambda s : value_rule(s)

name_rule = tok(r'[a-zA-Z][_a-zA-Z0-9]*')
define_rule = seq(skip(r'\('), skip(r'def'), name_rule, value_rule, skip(r'\)'))
access_rule = seq(skip(r'\$'), skip(r'\('), name_rule, skip(r'\)'))

array_rule = seq(skip(r'\['), group(list_of(value_rule, skip(r','))), skip(r'\]'), mkarr)

entry_rule = group(seq(name_rule, skip(r'=>'), value_rule))
dictionary_rule = seq(skip(r'{'), group(list_of(entry_rule, skip(r','))), skip(r'}'), mkdict)

value_rule = alt(number_rule, string_rule, array_rule, dictionary_rule, access_rule)

main = seq(group(many(define_rule)), ws)


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
    print(s.ok)

test()


