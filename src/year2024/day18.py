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

XSIZE = 71
YSIZE = 71

lo = 0
hi = len(lines)

while lo < hi:
    n = (lo+hi) // 2

    grid = Grid.empty(XSIZE, YSIZE)
    for line in lines[:n]:
        x, y = get_ints(line)
        grid[y,x] = '#'

    # grid.show()
    g = grid_graph(grid, is_node=lambda p, c: c != '#')

    dist = bfs(g, Point(0,0))
    if Point(XSIZE-1, YSIZE-1) in dist:
        lo = n + 1
    else:
        hi = n

print(lines[lo-1])
