import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
# scanner = Scanner(sys.stdin)

DIGITS = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9
}

lines = [line.strip() for line in sys.stdin.readlines()]
cnt = 0
sum = 0
for line in lines:
    a, b = line.split('|')
    signals = a.strip().split(' ')
    digits = b.strip().split(' ')
    m = defaultdict(set) # digit -> set(str)
    #print(signals)

    for d in signals:
        m[len(d)].add(d)

    # print(sum(len(v) for v in m.values()))
    #print(m)
    for p in itertools.permutations(range(7)):
        mapping = {}
        for a, b in enumerate(p):
            mapping[chr(97+a)] = chr(97+b)
        #print(mapping)

        def _resolve_digit(s):
            #print("RD", s)
            t = ""
            for c in s:
                t += mapping[c]
            t = ''.join(sorted(t))
            return DIGITS.get(t)

        ok = True
        for d in signals:
            rd = _resolve_digit(d)
            if rd is None:
                ok = False
        if not ok:
            continue

        value = 0
        for d in digits:
            value *= 10
            rd = _resolve_digit(d)
            if rd is not None:
                value += rd
            else:
                ok = False
        assert ok

        print(value)
        sum += value

print(sum)
