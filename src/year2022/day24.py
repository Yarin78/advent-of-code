import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

grid = Grid.read()

# state = (point,time)
start = Point(1,0)
goal = Point(grid.xsize-2, grid.ysize-1)

xsize = grid.xsize-2
ysize = grid.ysize-2

MOD = xsize*ysize//math.gcd(xsize, ysize)

print(xsize, ysize, MOD)

has_wind = set()
for y in range(ysize):
    for x in range(xsize):
        p = Point(x+1, y+1)
        c = grid[p]
        dir = None
        if c == '>':
            dir = RIGHT
        elif c == '<':
            dir = LEFT
        elif c == '^':
            dir = UP
        elif c == 'v':
            dir = DOWN
        if dir:
            p = Point(x,y)
            for tm in range(MOD):
                p2 = p + dir*tm
                p2 = Point(p2.x % xsize, p2.y % ysize)
                has_wind.add((p2, tm))

#print(has_wind)
print("precalc done")

def add(p: Point, tm: int):
    global grid
    if (p, tm) in visited:
        return
    if not grid.is_within(p):
        return
    if grid[p] == '#':
        return
    if (Point(p.x-1, p.y-1), tm%MOD) in has_wind:
        #print(f"Can't go to {p} at time {tm}")
        return
    visited.add((p, tm))
    q.put((p, tm))

q = Queue()
visited = set()
q.put((start, 0))
visited.add((start,0))

while not q.empty():
    cur, tm = q.get()
    #print(f"Time {tm}, at {cur}")
    if cur == goal:
        print("Part 1", tm)
        break

    add(cur, tm+1)
    for d in DIRECTIONS:
       add(cur + d, tm+1)


assert tm
q = Queue()
visited = set()
q.put((goal, tm))
visited.add((goal, tm))

while not q.empty():
    cur, tm = q.get()
    #print(f"Time {tm}, at {cur}")
    if cur == start:
        #print(tm)
        break

    add(cur, tm+1)
    for d in DIRECTIONS:
       add(cur + d, tm+1)

assert tm
q = Queue()
visited = set()
q.put((start, tm))
visited.add((start, tm))

while not q.empty():
    cur, tm = q.get()
    #print(f"Time {tm}, at {cur}")
    if cur == goal:
        print("Part 2", tm)
        break

    add(cur, tm+1)
    for d in DIRECTIONS:
       add(cur + d, tm+1)
