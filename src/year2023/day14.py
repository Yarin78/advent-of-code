import sys
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

lines = [line.strip() for line in sys.stdin.readlines()]

sort_dir = {
    NORTH: lambda p: (p.y, p.x),
    WEST: lambda p: (p.x, p.y),
    SOUTH: lambda p: (-p.y, p.x),
    EAST: lambda p: (-p.x, p.y)
}

def tilt(grid: Grid, dir:Point):
    o = sorted(grid.find('O'), key=sort_dir[dir])

    for p in o:
        grid.set(p, '.')

    for p in o:
        assert grid.get(p) == '.'
        q = p
        while grid.get_safe(q + dir) == '.':
            q = q + dir
        grid.set(q, 'O')

    return grid


def get_score(grid):
    return sum(grid.ysize - o.y for o in grid.find('O'))

def grid_key(grid):
    s = ""
    for y in range(grid.ysize):
        s += ''.join(grid.cells[y])
    return s

print(get_score(tilt(Grid(lines), NORTH)))

grid = Grid(lines)
seen = {}

left = 1000000000
while left > 0:
    key = grid_key(grid)
    if key in seen:
        left %= (seen[key] - left)
    seen[key] = left

    for d in [NORTH, WEST, SOUTH, EAST]:
        grid = tilt(grid, d)

    left -= 1

assert left == 0

print(get_score(grid))
