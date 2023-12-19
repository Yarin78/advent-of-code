import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

# Extremely ugly

lines = [line.strip() for line in sys.stdin.readlines()]

edges = set()

cur = Point(0,0)
edges.add(cur)
instr = []
ux = set()
uy = set()
ux.add(0)
uy.add(0)
for line in lines:
    dir, steps, col = line.split(' ')
    steps = int(col[2:7], 16)
    dir = [RIGHT, DOWN, LEFT, UP][int(col[-2])]
    instr.append((steps, dir))
    cur += dir * steps
    ux.add(cur.x)
    uy.add(cur.y)

def get_rel_coords(a):
    a = sorted(a)
    res = []
    for i in range(len(a)):
        if i > 0 and a[i] - a[i-1] > 1:
            res.append((a[i-1]+1, a[i]-a[i-1]-1))
        res.append((a[i], 1))
    return res
        
xcoords = {x: (i, len) for i, (x, len) in enumerate(get_rel_coords(ux))}
ycoords = {y: (i, len) for i, (y, len) in enumerate(get_rel_coords(uy))}

xcoordsize = {i: len for i, (x, len) in enumerate(get_rel_coords(ux))}
ycoordsize = {i: len for i, (y, len) in enumerate(get_rel_coords(uy))}

edges = set()    

cur = Point(0,0)
for steps, q in instr:
    x1 = xcoords[cur.x][0]
    y1 = ycoords[cur.y][0]
    cur = cur + q * steps
    x2 = xcoords[cur.x][0]
    y2 = ycoords[cur.y][0]
    if y1 == y2:
        x1,x2 = sorted([x1,x2])
        for i in range(x1,x2+1):
            edges.add(Point(i, y1))
    else:
        y1,y2 = sorted([y1,y2])
        for i in range(y1,y2+1):
            edges.add(Point(x1, i))

q = []
interior = set()
def add(p):
    if p not in edges and p not in interior:
        interior.add(p)
        q.append(p)

xmin = min(p.x for p in edges)
ymin = min(p.y for p in edges)
xmax = max(p.x for p in edges)
ymax = max(p.y for p in edges)

# for y in range(ymin, ymax+1):
#     s = ""
#     for x in range(xmin, xmax+1):
#         if Point(x,y) in edges:
#             s += "#"
#         else:
#             s += "."
#     print(s)

add(Point(xmin+28,ymin+5))
while q:
    cur = q.pop()
    if cur.x < xmin or cur.y < ymin or cur.x > xmax or cur.y > ymax:
        raise Exception()
    for d in [NORTH, SOUTH, EAST, WEST]:
        add(cur+d)

# print(len(edges) + len(interior))

for p in interior:
    edges.add(p)

part2=0
for p in edges:
    part2 += xcoordsize[p.x]*ycoordsize[p.y]

print(part2)
