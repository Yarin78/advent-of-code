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

p = grid.find('^')[0]
grid[p] = '.'

def simulate(grid, p):
    dir = 0
    seen = set()
    seen_coords = set()
    while grid.is_within(p):
        seen_coords.add(p)
        if (p, dir) in seen:
            return False
        seen.add((p, dir))
        c = grid.get_safe(p + DIRECTIONS[dir])
        if c == '#':
            dir = (dir + 1) % 4
        else:
            p += DIRECTIONS[dir]

    # print(len(seen_coords))
    return seen_coords

visited_coords = simulate(grid, p)
assert visited_coords
print(len(visited_coords))
# for p in seen_coords:
#     grid[p] = 'X'
# grid.show()

ans = 0
for i, q in enumerate(visited_coords):
    if i % 100 == 0:
        print(f"{i} / {len(visited_coords)}")
    if p != q and grid[q] == '.':
        grid[q] = '#'
        if not simulate(grid, p):
            ans += 1
        grid[q] = '.'

print(ans)
