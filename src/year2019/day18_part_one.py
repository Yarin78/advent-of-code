import sys
from queue import Queue
import heapq
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from intcode.intcode import *
from aocd import data, submit


lines = data.strip().split('\n')
#prog = Program(data)

keys = set()
doors = set()
map = []
key_loc = [0]*27
door_loc = [0]*26

y=0
for line in lines:
    x=0
    map.append(line)
    for c in line:
        if c >= 'a' and c <='z':
            key_loc[ord(c)-ord('a')] = Point(x,y)
            keys.add(c)
        if c >= 'A' and c <='Z':
            door_loc[ord(c)-ord('A')] = Point(x,y)
            doors.add(c)
        if c == '@':
            start=Point(x,y)
        x+=1
    y+=1

dist={}

xsize=len(map[0])
ysize=len(map)

seen = set()

keys_req = {} # keys_req['a] = set('b','c')
def dfs(cur, doors):
    global map
    global seen
    if cur in seen:
        return
    seen.add(cur)

    for d in DIRECTIONS:
        p = cur+d
        c = map[p.y][p.x]
        if c != '#':
            new_doors=set(doors)
            if c >= 'a' and c <= 'z':
                keys_req[c] = doors
            if c >= 'A' and c <= 'Z':
                new_doors.add(chr(ord(c)+32))
            dfs(p, new_doors)

dfs(start,set())
print(keys_req)

masks_req = {}
for k, v in keys_req.items():
    mask = 0
    for c in v:
        mask |= (2**(ord(c)-ord('a')))
    masks_req[ord(k)-ord('a')] = mask

print(masks_req)

g = grid_graph(map, lambda p, c: c !='#')

key_dist = defaultdict(lambda :defaultdict(int))  # key_dist[4][3] = distance between key 4 and 3  (26 == start pos)

for c in range(len(keys_req)):
    kd = bfs(g, key_loc[c])
    for t in range(len(keys_req)):
        key_dist[c][t] = kd[key_loc[t]]
    key_dist[c][26] = kd[start]
    key_dist[26][c] = kd[start]

key_loc[26] = start

q = []
dist = {}

def add(loc, keys, d):
    global q, dist
    node = (loc, keys)
    if node not in dist or d < dist[node]:
        dist[node] = d
        heapq.heappush(q, (d, node))

final_mask = (2**len(masks_req))-1
add(26, 0, 0)
while len(q):
    (cur_dist, (cur, keys)) = heapq.heappop(q)
    #print('dist %d: at key %c, with keys %d' % (cur_dist, chr(cur+97), keys))
    if keys == final_mask:
        print(cur_dist)
        break

    if cur_dist == dist[(cur,keys)]:
        for i in range(len(masks_req)):
            if (masks_req[i] & keys) == masks_req[i]:
                add(i, keys|(2**i), cur_dist+key_dist[cur][i])
