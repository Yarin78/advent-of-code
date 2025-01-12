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
graph = grid_graph(grid, get_edge=lambda p, c, q, d: c == d)

vis = set()
cost = 0
cost2 = 0
for p in grid.all_points():
    if p in vis:
        continue
    c = grid[p]

    region = bfs(graph, p)
    vis.update(region.keys())

    perimeter = 0
    sides = 0
    for v in region.keys():
        for d in DIRECTIONS:
            if grid.get_safe(v + d) != grid[p]:
                perimeter += 1

        if grid.get_safe(v + NORTH) != c and (grid.get_safe(v + EAST) != c or grid.get_safe(v + EAST + NORTH) == c):
            sides += 1
        if grid.get_safe(v + EAST) != c and (grid.get_safe(v + SOUTH) != c or grid.get_safe(v + EAST + SOUTH) == c):
            sides += 1
        if grid.get_safe(v + SOUTH) != c and (grid.get_safe(v + WEST) != c or grid.get_safe(v + WEST + SOUTH) == c):
            sides += 1
        if grid.get_safe(v + WEST) != c and (grid.get_safe(v + NORTH) != c or grid.get_safe(v + WEST + NORTH) == c):
            sides += 1

    print(f"Region {grid[p]} has area {len(region)} and perimeter {perimeter} and sides {sides}")
    cost += perimeter * len(region)
    cost2 += sides * len(region)
    # print(grid[p], visited)

print(cost)
print(cost2)
