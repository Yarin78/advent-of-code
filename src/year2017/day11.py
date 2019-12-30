import sys
from collections import defaultdict
from lib import util

x,y,z = 0,0,0
maxdist=0
dirs = sys.stdin.readline().strip().split(',')
for d in dirs:
    if d == 'n':
        y += 1
        z -= 1
    elif d == 'ne':
        x += 1
        z -= 1
    elif d == 'se':
        x += 1
        y -= 1
    elif d == 's':
        z += 1
        y -= 1
    elif d == 'sw':
        x -= 1
        z += 1
    elif d == 'nw':
        x -= 1
        y += 1
    else:
        assert False

    dist = (abs(x)+abs(y)+abs(z)) // 2
    maxdist=max(maxdist, dist)

dist = (abs(x)+abs(y)+abs(z)) // 2
print(dist)
print(maxdist)
