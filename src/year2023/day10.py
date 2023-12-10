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

start = grid.find_first('S')

def neighbors(p: Point):
    c = grid.get(p)
    if c == '-':
        return [p+LEFT, p+RIGHT]
    if c == '|':
        return [p+UP, p+DOWN]
    if c == 'L':
        return [p+UP, p+RIGHT]
    if c == 'J':
        return [p+UP, p+LEFT]
    if c == '7':
        return [p+DOWN, p+LEFT]
    if c == 'F':
        return [p+DOWN, p+RIGHT]
    assert False

first_neighbors = sorted([n for n in grid.neighbors(start) if start in neighbors(n)])
assert len(first_neighbors) == 2

for c in '-|LJ7F':
    grid.set(start, c)
    if sorted(neighbors(start)) == first_neighbors:
        break
    grid.set(start, 'S')

assert grid.get(start) != 'S'

cur = first_neighbors[0]
last = start
loop_tiles = set()
loop_tiles.add(start)
while cur != start:
    loop_tiles.add(cur)
    n = neighbors(cur)
    if n[0] == last:
        next = n[1]
    else:
        next = n[0]
    last = cur
    cur = next

print(len(loop_tiles) // 2)

part2 = 0
for y in range(grid.ysize):
    s = ""
    inside = False
    for x in range(grid.xsize):
        p = Point(x,y)
        c = grid.get(p)
        if p in loop_tiles and (c == '|' or c == '7' or c == 'F'):
            inside = not inside
        if p not in loop_tiles:
            if inside:
                s += 'I'
            else:
                s += '.'
            part2 += inside
        else:
            s += '#'

print(part2)
