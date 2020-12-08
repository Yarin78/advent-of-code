import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations, combinations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from aocd import data, submit

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
lines = data.strip().split('\n')
# intlines = [int(x) for x in lines]
ans = ans2 = 0
for line in lines:
    minmax = get_ints(line)

    parts = line.split(' ')
    c = parts[1][0]
    pw = parts[2]
    t = 0
    p1 = minmax[0]-1
    p2 = -minmax[1]-1
    if p1 >= 0 and p1 < len(pw) and pw[p1] == c:
        t += 1
    if p2 >= 0 and p2 < len(pw) and pw[p2] == c:
        t += 1
    #print(t)
    if t == 1:
        ans += 1

print(ans)
# submit(ans, part="a", day=2, year=2020)
# submit(ans2, part="b", day=2, year=2020)
