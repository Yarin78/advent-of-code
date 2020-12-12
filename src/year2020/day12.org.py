import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from vm.vm import *

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
lines = [line.strip() for line in sys.stdin.readlines()]
# prog = Program(lines)

# data = [int(x) for x in lines]
ans = 0
cur = Point(0,0)
wp = Point(10, 1)
# dirs = [Point(1,0), Point(0, -1), Point(-1,0), Point(0, 1)]
# E = positive, N = positive
for line in lines:
    steps=int(line[1:])
    d = line[0]
    if d == 'F':
        cur += wp*steps
    elif d == 'L':
        c = steps//90
        while c > 0:
            wp = Point(-wp.y, wp.x)
            c -= 1
    elif d == 'R':
        c = steps//90
        while c > 0:
            wp = Point(wp.y, -wp.x)
            c -= 1
    elif d == 'E':
        wp += Point(steps,0)
    elif d == 'W':
        wp += Point(-steps,0)
    elif d == 'N':
        wp += Point(0, steps)
    elif d == 'S':
        wp += Point(0, -steps)

print(cur, wp)
print(abs(cur.x)+abs(cur.y))

# 1148