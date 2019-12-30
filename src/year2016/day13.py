import sys
import re
import itertools
from collections import defaultdict
from lib.util import get_ints
from lib.geo2d import Point, DIRECTIONS
from heapq import *

input = sys.stdin
#input = open('year2016/day13.in')
#input = open('year2016/day13.sample.in')

#input = 10
input = 1362

def is_wall(cur):
    x = cur.x
    y = cur.y
    global input
    sum = x*x + 3*x + 2*x*y + y + y*y + input
    cnt = 0
    while sum:
        sum &= (sum-1)
        cnt += 1
    return cnt % 2 == 1

GOAL = Point(31,39)
#GOAL = Point(7,4)

q = []
heappush(q, (0,Point(1,1)))
visited = set()
reached = 0

while True:
    (dist, cur) = heappop(q)
    if cur in visited:
        continue
    if dist <= 50:
        reached += 1
    visited.add(cur)
    if cur == GOAL:
        print('Done in %d steps' % dist)
        break
    for d in DIRECTIONS:
        np = cur + d
        if not is_wall(np) and np.x >= 0 and np.y >= 0:
            heappush(q, (dist+1, np))

print('50 or less:', reached)