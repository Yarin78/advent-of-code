import functools
import sys
from yal.util import *

lines = [line.strip() for line in sys.stdin.readlines()]

def comp(l1: List, l2: List):
    for (a,b) in zip(l1, l2):
        aint = isinstance(a, int)
        bint = isinstance(b, int)

        if aint and bint:
            cmp = a-b
        elif not aint and not bint:
            cmp = comp(a, b)
        elif aint:
            cmp = comp([a], b)
        else:
            cmp = comp(a, [b])
        if cmp:
            return cmp
    return len(l1) - len(l2)


part1 = 0
for ix, pairs in enumerate(split_lines(lines)):
    if comp(eval(pairs[0]), eval(pairs[1])) < 0:
        part1 += ix+1

print(part1)

DIV1 = [[2]]
DIV2 = [[6]]
all_packs = [DIV1, DIV2] + [eval(line) for line in lines if line]

sorted_packs = sorted(all_packs, key=functools.cmp_to_key(comp))

divs = [ix+1 for ix, p in enumerate(sorted_packs) if p in (DIV1, DIV2)]
print(divs[0] * divs[1])
