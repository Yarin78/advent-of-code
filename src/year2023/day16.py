import sys
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

lines = [line.strip() for line in sys.stdin.readlines()]

def search(grid, start, dir):
    seen = set()
    vis = set()
    q = []

    def add(p, dir):
        if grid.is_within(p) and (p, dir) not in seen:
            seen.add((p, dir))
            q.append((p, dir))
            vis.add(p)

    add(start, dir)

    while len(q):
        cur, dir = q.pop()
        
        if grid.get(cur) == '.':
            add(cur + dir, dir)
        elif grid.get(cur) == '/':
            if dir == EAST:
                ndir = NORTH
            elif dir == NORTH:
                ndir = EAST
            elif dir == WEST:
                ndir = SOUTH
            else:
                ndir = WEST
            add(cur + ndir, ndir)    
        elif grid.get(cur) == '\\':
            if dir == EAST:
                ndir = SOUTH
            elif dir == SOUTH:
                ndir = EAST
            elif dir == WEST:
                ndir = NORTH
            else:
                ndir = WEST
            add(cur + ndir, ndir)    
        elif grid.get(cur) == '|':
            if dir == WEST or dir == EAST:
                add(cur + NORTH, NORTH)  
                add(cur + SOUTH, SOUTH)
            else:
                add(cur+dir, dir)
        elif grid.get(cur) == '-':
            if dir == SOUTH or dir == NORTH:
                add(cur + WEST, WEST)  
                add(cur + EAST, EAST)
            else:
                add(cur+dir, dir)

    return len(vis)


grid = Grid(lines)
print(search(grid, Point(0,0), EAST))

best = 0
for p in grid.all_points():
    if p.y == 0:
        best = max(best, search(grid, p, SOUTH))
    if p.x == 0:
        best = max(best, search(grid, p, EAST))
    if p.x == grid.xsize-1:
        best = max(best, search(grid, p, WEST))
    if p.y == grid.ysize-1:
        best = max(best, search(grid, p, NORTH_EAST))
    
print(best)
