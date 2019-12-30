import sys
import math
from queue import Queue
from collections import defaultdict
from itertools import permutations
from lib import util
from lib.geo2d import *
from lib.intcode import *
from aocd import data, submit

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a%b)

gcd_cnt = defaultdict(int)


lines = data.strip().split('\n')
best = 0
for y in range(len(lines)):
    for x in range(len(lines[y])):
        if lines[y][x] == '#':
            cnt = 0
            for ty in range(len(lines)):
                for tx in range(len(lines[ty])):
                    if lines[ty][tx] != '#':
                        continue
                    if y == ty and x == tx:
                        continue
                    dx = tx-x
                    dy = ty-y
                    d = gcd(abs(dx), abs(dy))
                    dx //= d
                    dy //= d
                    cx = x+dx
                    cy = y+dy
                    can_see = True
                    #print(x,y, tx, ty, dx,dy, cx, cy)
                    while cx != tx or cy != ty:
                        #print('  ', cx,cy)
                        if lines[cy][cx] == '#':
                            can_see = False
                        cx += dx
                        cy += dy
                    if can_see:
                        #print('%d, %d' % (tx, ty))
                        cnt += 1
            #sys.stdout.write('%d' % cnt)
            if cnt > best:
                sx = x
                sy = y
                best = cnt
        #else:
        #    sys.stdout.write('.')

print(best, sx, sy)

#sx = 31
#sy = 20


# for y in range(len(lines)):
#     for x in range(len(lines[y])):
#         if x == sx and y == sy:
#             continue
#         if lines[y][x] != '#':
#             continue
#         dx = x-sx
#         dy = y-sy
#         d = gcd(abs(dx), abs(dy))
#         dx //= d
#         dy //= d
#         gcd_cnt[(dx,dy)] += 1

# most = max(gcd_cnt.values())

# print(most)
# for ((dx, dy), cnt) in gcd_cnt.items():
#     if cnt == most:
#     #if cnt > 1:
#         print(dx,dy,cnt)
#         cx = sx+dx
#         cy = sy+dy
#         seen = 0
#         while True:
#             if lines[cy][cx] == '#':
#                 print('hitting at %d,%d' % (cx,cy))
#                 seen += 1
#                 if seen == most:
#                     break
#             cx += dx
#             cy += dy

#         print(cx, cy, cx*100+cy)

#sx = 8
#sy = 3

m = []
for y in range(len(lines)):
    s = []
    for x in range(len(lines[y])):
        s.append(lines[y][x])
    m.append(s)


wave = 0
r = []
while True:
    wave += 1
    removed = 0
    done = set()
    print('wave %d' % wave)
    for ty in range(len(lines)):
        for tx in range(len(lines[ty])):
            if m[ty][tx] != '#':
                continue
            if sy == ty and sx == tx:
                continue
            dx = tx-sx
            dy = ty-sy
            d = gcd(abs(dx), abs(dy))
            dx //= d
            dy //= d
            if (dx,dy) in done:
                continue
            done.add((dx,dy))
            cx = sx+dx
            cy = sy+dy
            while True:
                if m[cy][cx] == '#':
                    #print('removing %d,%d' % (cx,cy))
                    angle = math.atan2(dy,dx)
                    if dy < 0 and dx < 0:
                        angle += 2*math.pi
                    r.append((wave,angle, cx, cy))
                    m[cy][cx] = '.'
                    removed += 1
                    break
                cx += dx
                cy += dy
    if removed == 0:
        break

r.sort()
ix = 1
for x in r:
    print(ix, x)
    ix += 1


#prog = Program(data)

# submit(?, part="a", day=10, year=2019)
# submit(?, part="b", day=10, year=2019)
