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
end = grid.find('E')[0]
grid[start] = '.'
grid[end] = '.'

g = grid_graph(grid, lambda p,c: c != '#')

distance = bfs(g, start)[end]
print(distance)

num_saved = defaultdict(int)

dstart = bfs(g, start)
dend = bfs(g, end)

MAX_STEPS = 20

for p in grid.find('.'):
    for x in range(-MAX_STEPS, MAX_STEPS+1):
         for y in range(-MAX_STEPS, MAX_STEPS+1):
            cheat_steps = abs(x) + abs(y)
            if cheat_steps < 2 or cheat_steps > MAX_STEPS:
                continue
            q = p + Point(x,y)
            if grid.is_within(q) and grid[q] == '.':
                saved = distance - (dstart[p] + dend[q] + cheat_steps)
                if saved > 0:
                    num_saved[saved] += 1


cnt = 0
for time_saved, num_cheats in sorted(num_saved.items(), key=lambda x: x[0]):
    print(f"There are {num_cheats} cheats that save {time_saved} picoseconds.")
    if time_saved >= 100:
        cnt += num_cheats

print(cnt)
