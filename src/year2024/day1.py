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

va = []
vb = []
cnt = defaultdict(int)
for line in lines:
    a, b = get_ints(line)
    va.append(a)
    vb.append(b)
    cnt[b] += 1

ans = 0
for i,j in zip(sorted(va), sorted(vb)):
    ans += abs(i-j)

print(ans)

ans2 = 0
for i in va:
    ans2 += i*cnt[i]

print(ans2)