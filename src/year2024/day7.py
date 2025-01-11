import sys
from dataclasses import dataclass
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

# Make sure ~/.config/aocd/token is correct! (Application tab -> Cookies)
# scanner = Scanner(sys.stdin)
lines = [line.strip() for line in sys.stdin.readlines()]
# Split input into an array of array of lines, split by empty line
# sections = split_lines(lines)

# data = [int(x) for x in lines]
def go(v, cur, i, searched):
    if i == len(v):
        return cur == searched
    return go(v, cur + v[i], i + 1, searched) or go(v, cur * v[i], i+1, searched) or go(v, int(f"{cur}{v[i]}"), i+1, searched)

ans = 0
for line in lines:
    v = get_ints(line)
    res = v[0]
    v = v[1:]
    if go(v, v[0], 1, res):
        ans += res

print(ans)
