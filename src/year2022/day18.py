import sys
from queue import Queue
from yal.util import *
from yal.geo3d import *

DIRS = [
    Point(1,0,0),
    Point(-1,0,0),
    Point(0,1,0),
    Point(0,-1,0),
    Point(0,0,1),
    Point(0,0,-1),
]

cubes = set()
outside = set()

for line in sys.stdin.readlines():
    x,y,z = get_ints(line)
    cubes.add(Point(x+1, y+1, z+1))

max_x = max(c.x for c in cubes) + 2
max_y = max(c.y for c in cubes) + 2
max_z = max(c.z for c in cubes) + 2


q = Queue()
start = Point(0,0,0)
outside.add(start)
q.put(start)
while not q.empty():
    cur = q.get()
    for dir in DIRS:
        s = cur + dir
        if s.x >= 0 and s.y >= 0 and s.z >= 0 and s.x < max_x and s.y < max_y and s.z < max_z and s not in cubes and s not in outside:
            outside.add(s)
            q.put(s)

area1 = area2 = 0

for p in cubes:
    for dir in DIRS:
        area1 += p + dir not in cubes
        area2 += p + dir not in cubes and p + dir in outside

print(area1, area2)
