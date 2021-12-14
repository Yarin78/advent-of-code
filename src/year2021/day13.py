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
lines = [line.strip() for line in sys.stdin.readlines()]

dots = set()
for line in lines:
    if line == "":
        break
    (x,y) = get_ints(line)
    p = Point(x,y)
    dots.add(p)

print(len(dots))

for line in lines:
    if line.startswith("fold"):
        pos = get_ints(line)[0]
        new_dots = set()
        if 'y' in line:
            for d in dots:
                np = d if d.y < pos else Point(d.x, 2*pos-d.y)
                new_dots.add(np)
        else:
            for d in dots:
                np = d if d.x < pos else Point(2*pos-d.x, d.y)
                new_dots.add(np)
        dots = new_dots
        for p in dots:
            assert p.x >= 0 and p.y >= 0

print(len(dots))

v = {x:'#' for x in dots}
s = gridify_sparse_map(v)
for line in s:
    print(line)