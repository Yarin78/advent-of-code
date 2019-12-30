import sys
from lib.geo2d import Point, DIRECTIONS

input = sys.stdin
input = open('year2016/day1.in')

cur = Point(0,0)
seen = set([cur])
d = 0
for dir in input.readline().split(", "):
    if dir[0] == 'L':
        d = (d+1) % 4
    else:
        d = (d+3) % 4
    t = int(dir[1:])
    while t:
        cur += DIRECTIONS[d]
        if seen and cur in seen:
            print('First seen:', cur)
            seen = None
        if seen:
            seen.add(cur)
        t -= 1

print(abs(cur.x)+abs(cur.y))
