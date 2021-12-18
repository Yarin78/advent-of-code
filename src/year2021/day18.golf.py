import sys
import functools

def add_right(e, val):
    return e+val if isinstance(e, int) else [e[0], add_right(e[1], val)]

def explode(e, depth=0, al=0):
    if isinstance(e, int):
        return e+al, 0, 0
    if len(e) == 2 and all(isinstance(v, int) for v in e):
        return (0, e[0]+al, e[1]) if depth > 3 else ([e[0]+al, e[1]], 0, 0)
    left, lv, rv = explode(e[0], depth+1, al)
    right, lv2, rv2 = explode(e[1], depth+1, rv)
    return [add_right(left, lv2), right], lv, rv2

def split(e, splitted=False):
    if isinstance(e, int):
        return (e, splitted) if e < 10 or splitted else ([e//2, (e+1)//2], True)
    left, splitted = split(e[0], splitted)
    right, splitted = split(e[1], splitted)
    return ([left, right], splitted)

def reduce(expr):
    expr, splitted = split(explode(expr)[0])
    return reduce(expr) if splitted else expr

def magnitude(e):
    return e if isinstance(e,int) else 3*magnitude(e[0])+2*magnitude(e[1])

exprs = [eval(line) for line in sys.stdin.readlines()]

print(magnitude(functools.reduce(lambda a, b: reduce([a, b]), exprs)))
print(max(magnitude(reduce([a, b])) for a in exprs for b in exprs))
