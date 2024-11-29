import re
from collections import namedtuple


State = namedtuple('State', 'text pos ok stack glob')

def eat(expr):
    code = re.compile(expr)
    def parse(s):
        if (m := code.match(s.text[s.pos:])) is None:
            return s._replace(ok=False)
        pos = s.pos + len(m.group())
        s.glob['err'] = max(s.glob['err'], pos)
        return s._replace(pos=pos)
    return parse

def seq(*funcs):
    def parse(s):
        for f in funcs:
            if not (s := f(s)).ok:
                return s
        return s
    return parse

def alt(*funcs):
    def parse(s):
        for f in funcs:
            if (new_s := f(s)).ok:
                return new_s
        return new_s
    return parse

def many(f):
    def parse(s):
        while (new_s := f(s)).ok:
            s = new_s
        return s
    return parse

def push(f):
    def parse(s):
        pos = s.pos
        if not (s := f(s)).ok:
            return s
        return s._replace(stack=s.stack + (s.text[pos:s.pos],))
    return parse

def to(f):
    n = f.__code__.co_argcount
    def parse(s):
        pos = len(s.stack) - n
        return s._replace(stack=s.stack[:pos] + (f(*s.stack[pos:]),))
    return parse

def group(f):
    def parse(s):
        stack = s.stack
        if not (s := f(s)).ok:
            return s
        return s._replace(stack=stack + (s.stack[len(stack):],))
    return parse

def peek(f):
    def parse(s):
        return s._replace(ok=f(s).ok)
    return parse

def npeek(f):
    def parse(s):
        return s._replace(ok=not f(s).ok)
    return parse

def memo(f):
    def parse(s):
        key = f, s.pos
        tab = s.glob['tab']
        if key not in tab:
            tab[key] = f(s)
        return tab[key]
    return parse

def left(f):
    def parse(s):
        key = f, s.pos
        tab = s.glob['tab']
        if key not in tab:
            tab[key] = s._replace(ok=False)
            pos = s.pos
            while (s := f(s._replace(pos=pos))).pos > tab[key].pos:
                tab[key] = s
        return tab[key]
    return parse

def parse(text, f):
    s = f(State(text, 0, True, (), dict(err=0, tab={})))
    return s._replace(ok=s.ok and s.pos == len(s.text))

empty = lambda s: s
opt = lambda f: alt(f, empty)
some = lambda f: seq(f, many(f))
list_of = lambda f, d: seq(f, many(seq(d, f)))

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
