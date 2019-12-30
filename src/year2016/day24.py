import sys
import re
import itertools
from collections import defaultdict
from lib.util import get_ints
from heapq import *
from lib.geo2d import Point, DIRECTIONS

input = sys.stdin
input = open('year2016/day24.in')
#input = open('year2016/day24.sample.in')

data = [line.strip() for line in input.readlines()]
targets = []
for y in range(len(data)):
    for x in range(len(data[y])):
        if data[y][x] == '0':
            start = Point(x,y)
        elif data[y][x].isdigit():
            targets.append(Point(x,y))

q = []
visited = set()
heappush(q, (0, start, 2**len(targets)-1))
while len(q) > 0:
    (dist, cur, mask) = heappop(q)
    if (cur, mask) in visited:
        continue
    if mask == 0 and cur == start:
        print('Done after %d steps' % dist)
        break
    visited.add((cur, mask))
    for d in DIRECTIONS:
        pos = cur + d
        if pos.x >= 0 and pos.y >= 0 and pos.y < len(data) and pos.x < len(data[pos.y]) and data[pos.y][pos.x] != '#':
            if pos in targets:
                new_mask = mask & ~(2**targets.index(pos))
            else:
                new_mask = mask
            if (pos, new_mask) not in visited:
                heappush(q, (dist + 1, pos, new_mask))
