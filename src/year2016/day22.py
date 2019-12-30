import sys
import re
import itertools
import hashlib
from collections import defaultdict
from lib.util import get_ints
from lib.geo2d import Point, DIRECTIONS
from heapq import *

input = sys.stdin
input = open('year2016/day22.in')
#input = open('year2016/day22.sample.in')

disk = {} # Point => (size, used)

for line in input.readlines():
    a = get_ints(line)
    if len(a) == 0:
        continue
    x=a[0]
    y=a[1]
    size=a[2]
    used=a[3]
    avail=a[4]
    disk[Point(x,y)] = (size,used,avail)

valid = set()
no_viable = 0
maxx = 0
for a in disk.keys():
    if a.y == 0 and a.x > maxx:
        maxx = a.x
    if disk[a][1] == 0:
        hole = a
        valid.add(a)
        continue
    for b in disk.keys():
        if a != b:
            if disk[a][1] <= disk[b][2]:
                no_viable += 1
                valid.add(a)
                #print(a,b)

#print(no_viable)
visited = set()
last_dist = 0
q = [(0, hole, Point(maxx, 0))]
while len(q) > 0:
    (dist, hole, target) = heappop(q)
    if (hole,target) in visited:
        continue
    if dist > last_dist:
        print('At distance %d, states visited %d' % (dist, len(visited)))
        last_dist = dist
    visited.add((hole, target))

    #print('%2d: Hole at %s, target at %s' % (dist, hole, target))
    if target==Point(0,0):
        print('Done in %d steps' % dist)
        break
    for d in DIRECTIONS:
        new_hole = hole + d
        if new_hole in valid:
            new_target = hole if new_hole == target else target
            p = (new_hole, new_target)
            if p not in visited:
                heappush(q, (dist+1, new_hole, new_target))

