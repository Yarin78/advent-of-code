import sys
from yal.geo4d import *

data = [line.strip() for line in sys.stdin.readlines()]

#cur = set(Point(x,y,0) for y in range(len(data)) for x in range(len(data[y])) if data[y][x] == '#')
cur = set(Point(x,y,0,0) for y in range(len(data)) for x in range(len(data[y])) if data[y][x] == '#')

for i in range(6):
    prev = cur
    cur = set()

    minx, maxx = min(p.x for p in prev), max(p.x for p in prev)
    miny, maxy = min(p.y for p in prev), max(p.y for p in prev)
    minz, maxz = min(p.z for p in prev), max(p.z for p in prev)
    minh, maxh = min(p.h for p in prev), max(p.h for p in prev)

    #for p in Point.range(Point(minx-1, miny-1, minz-1), Point(maxx+2, maxy+2, maxz+2)):
    for p in Point.range(Point(minx-1, miny-1, minz-1, minh-1), Point(maxx+2, maxy+2, maxz+2, maxh+2)):
        #num_act = sum(p + dp != p and p + dp in prev for dp in Point.range(Point(-1, -1, -1), Point(2, 2, 2)))
        num_act = sum(p + dp != p and p + dp in prev for dp in Point.range(Point(-1, -1, -1, -1), Point(2, 2, 2, 2)))

        if p in prev and (num_act == 2 or num_act == 3):
            cur.add(p)
        if p not in prev and num_act == 3:
            cur.add(p)

print(len(cur))
