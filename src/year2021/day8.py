import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

lines = [line.strip() for line in sys.stdin.readlines()]
sum = 0
for line in lines:
    left, right = line.split('|')
    signals = left.strip().split(' ')
    digits = right.strip().split(' ')
    all = [*signals, *digits]

    def _is_superset(a, b):
        return set(a).issuperset(set(b))

    def _sorted(s):
        return ''.join(sorted(s))

    m = {}
    for d in all:
        if len(d) == 2:
            m[1] = d
        if len(d) == 4:
            m[4] = d
        if len(d) == 3:
            m[7] = d
        if len(d) == 7:
            m[8] = d
    for d in all:
        if len(d) == 6:
            if _is_superset(d, m[4]):
                m[9] = d
            elif _is_superset(d, m[7]):
                m[0] = d
            else:
                m[6] = d
    for d in all:
        if len(d) == 5:
            if _is_superset(d, m[1]):
                m[3] = d
            elif _is_superset(m[9], d):
                m[5] = d
            else:
                m[2] = d

    rev = {_sorted(v):k for k,v in m.items()}

    number = int(''.join(str(rev[_sorted(d)]) for d in digits))
    sum += number

print(sum)
