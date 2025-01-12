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

start = grid.find('S')[0]
goal = grid.find('E')[0]
grid[start] = '.'
grid[goal] = '.'

g = defaultdict(list)

for p in grid.all_points():
    if grid[p] == '.':
        for i, d in enumerate(DIRECTIONS):
            g[(p, i)].append(((p, (i+1)%4), 1000))
            g[(p, i)].append(((p, (i+3)%4), 1000))
            if grid[p+d] == '.':
                g[(p, i)].append(((p+d, i), 1))


best = dijkstra2((start, 1), neighbors=lambda p: g[p], done_func=lambda p: p[0] == goal)

print(best)
INF = 1_000_000_000

tiles = set()
for goal_dir in range(4):
    res1 = dijkstra(g, (start, 1))
    res2 = dijkstra(g, (goal, goal_dir))

    for p in grid.all_points():
        if grid[p] == '.':
            for d in range(4):
                if res1.get((p, d), INF) + res2.get((p, (d+2)%4), INF) == best:
                    tiles.add(p)

for t in tiles:
    grid[t] = 'O'

grid.show()
print(len(tiles))

