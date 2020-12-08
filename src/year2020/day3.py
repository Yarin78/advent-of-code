import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from aocd import data, submit

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
lines = data.strip().split('\n')
# intlines = [int(x) for x in lines]
ans = ans2 = 0
ans2 = 1
for slope in [(1,1),(3,1),(5,1),(7,1),(1,2)]:
    y = 0
    x = 0
    ans=0
    while y < len(lines):
        if lines[y][x%len(lines[y])] == '#':
            ans += 1
        y += slope[1]
        x += slope[0]
    ans2 *= ans


print(ans2)
# submit(ans, part="a", day=3, year=2020)
# submit(ans2, part="b", day=3, year=2020)
