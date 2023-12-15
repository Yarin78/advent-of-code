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
    for p in grid.edge_points(dir):
        last = p
        while grid.is_within(p):
            if grid.get(p) == 'O':
                grid.set(p, '.')
                grid.set(last, 'O')
                last -= dir
            elif grid.get(p) == '#':
                last = p - dir
            p -= dir

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
    key = grid.get_hash_key()
    if key in seen:
        left %= (seen[key] - left)
    seen[key] = left

    for d in [NORTH, WEST, SOUTH, EAST]:
        grid = tilt(grid, d)

    left -= 1

assert left == 0

print(get_score(grid))
