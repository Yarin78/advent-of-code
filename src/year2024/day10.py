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

def go(p: Point, pos):
    if grid[p] == '9':
        pos.add(p)
        return 1
    cnt = 0
    for d in DIRECTIONS:
        if grid.is_within(p + d) and grid[p+d] == chr(ord(grid[p]) + 1):
            cnt += go(p+d, pos)
    return cnt

ans = 0
ans2 = 0
for p in grid.find('0'):
    pos = set()
    ans2 += go(p, pos)
    ans += len(pos)

print(ans)
print(ans2)
