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

grid = Grid(lines)
ans = 0
ans2 = 0
for y in range(grid.ysize):
    for x in range(grid.xsize):
        p = Point(x,y)
        for d in DIRECTIONS_INCL_DIAGONALS:
            ok = True
            for i, c in enumerate('XMAS'):
                if grid.get_safe(p+d*i) != c:
                    ok = False
            if ok:
                ans += 1

print(ans)

for y in range(grid.ysize):
    for x in range(grid.xsize):
        p = Point(x,y)
        if grid[p] == 'A':
            c1 = grid.get_safe(p + NORTH_EAST)
            c2 = grid.get_safe(p + SOUTH_WEST)
            c3 = grid.get_safe(p + NORTH_WEST)
            c4 = grid.get_safe(p + SOUTH_EAST)
            ok = 0
            if (c1 == 'M' and c2 == 'S') or (c1 == 'S' and c2 == 'M'):
                ok += 1
            if (c3 == 'M' and c4 == 'S') or (c3 == 'S' and c4 == 'M'):
                ok += 1
            if ok == 2:
                ans2 += 1

print(ans2)
