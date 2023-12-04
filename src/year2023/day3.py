import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

lines = [line.strip() for line in sys.stdin.readlines()]
grid = Grid(lines)

part1 = 0
part2 = 0
gears = defaultdict(set)

for p in grid.all_points():
    if grid.get(p).isdigit() and (p.x == 0 or not grid.get(p+LEFT).isdigit()):
        q = p
        while grid.is_within(q) and grid.get(q).isdigit():
            q = q+RIGHT
        num = int(lines[p.y][p.x:q.x])
        adj_symbol = False
        for digx in range(p.x, q.x):
            for dp in DIRECTIONS_INCL_DIAGONALS:
                q = Point(digx, p.y) + dp
                c = grid.get_safe(q)
                if c is not None and not c.isdigit() and c != '.':
                    adj_symbol=True
                if c == '*':
                    gears[q].add((p, num))

        if adj_symbol:
            part1 += num

print(part1)
for d in gears.values():
    nums = [num for (_, num) in d]
    if len(nums) == 2:
        part2 += nums[0] * nums[1]
print(part2)
