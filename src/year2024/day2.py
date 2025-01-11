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
ans = 0

def is_safe(levels):
    if sorted(levels) == levels or sorted(levels,reverse=True) == levels:
        ok = True
        for i in range(len(levels) - 1):
            diff = abs(levels[i] - levels[i+1])
            if diff < 1 or diff > 3 :
                ok = False
        if ok:
            return True
    return False

ans2 = 0
for line in lines:
    levels = get_ints(line)
    if is_safe(levels):
        ans += 1
    ok = False
    for i in range(len(levels)):
        l = []
        for j in range(len(levels)):
            if i != j:
                l.append(levels[j])
        if is_safe(l):
            ok = True
    if ok:
        ans2 += 1


print(ans)
print(ans2)
