import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from vm.vm import *

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
lines = [line.strip() for line in sys.stdin.readlines()]

flipped = set()
for line in lines:
    p = Point(0,0)
    i = 0
    while i < len(line):
        if line[i]=="e":
            p += Point(1,0)
            i+=1
        elif line[i]=="w":
            p += Point(-1,0)
            i+=1
        elif line[i:i+2]=="se":
            p += Point(0,1)
            i+=2
        elif line[i:i+2]=="sw":
            p += Point(-1,1)
            i+=2
        elif line[i:i+2]=="ne":
            p += Point(1,-1)
            i+=2
        elif line[i:i+2]=="nw":
            p += Point(0,-1)
            i+=2
    if p in flipped:
        flipped.remove(p)
    else:
        flipped.add(p)

dirs = [Point(1,0), Point(-1,0), Point(0,1), Point(-1,1), Point(1,-1), Point(0,-1)]

for day in range(101):
    print(day, len(flipped))

    miny = min(f.y for f in flipped)
    maxy = max(f.y for f in flipped)
    minx = min(f.x for f in flipped)
    maxx = max(f.x for f in flipped)

    new_flipped = set()
    for y in range(miny-1, maxy+2):
        for x in range(minx-1, maxx+2):
            p = Point(x,y)
            cnt = 0
            for d in dirs:
                q = p+d
                if q in flipped:
                    cnt += 1
            if p in flipped and (cnt == 0 or cnt > 2):
                pass
            elif p not in flipped and cnt == 2:
                new_flipped.add(p)
            elif p in flipped:
                new_flipped.add(p)

    flipped = new_flipped

