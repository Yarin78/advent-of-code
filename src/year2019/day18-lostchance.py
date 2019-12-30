import sys
from queue import Queue
import heapq
from collections import defaultdict
from itertools import permutations
from lib.util import *
from lib.graph import *
from lib.geo2d import *
from lib.intcode import *
from aocd import data, submit


lines = data.strip().split('\n')
#prog = Program(data)

map = []
key_loc = [0]*27
door_loc = [0]*26
num_keys = 0
y=0
for line in lines:
    x=0
    map.append(line)
    for c in line:
        if c >= 'a' and c <='z':
            num_keys += 1
            key_loc[ord(c)-ord('a')] = Point(x,y)
        if c >= 'A' and c <='Z':
            door_loc[ord(c)-ord('A')] = Point(x,y)
        if c == '@':
            start=Point(x,y)  # 40,40
        x+=1
    y+=1

dist={}
all_keys = (2 ** num_keys)-1
xsize=len(map[0])
ysize=len(map)

q = Queue()
dist = {}
q.put((start, 0))
dist[(start,0)]=0
next_dist = 1
while not q.empty():
    (cur, keys) = q.get()
    cur_dist = dist[(cur,keys)]
    #print('dist %d: at %s with keys %d' % (cur_dist, cur, keys))
    if cur_dist == next_dist:
        print(cur_dist)
        next_dist += 1

    if keys == all_keys:
        print(cur_dist)
        break
    for d in DIRECTIONS:
        np = cur+d
        c = map[np.y][np.x]
        if c != '#':
            if c >= 'A' and c <= 'Z':
                key_req = 2**(ord(c)-65)
                if key_req & keys == 0:
                    continue
            new_keys = keys
            if c >= 'a' and c <= 'z':
                key_got = 2**(ord(c)-97)
                new_keys |= key_got
            if (np, new_keys) not in dist:
                dist[(np, new_keys)] = cur_dist+1
                q.put((np, new_keys))
