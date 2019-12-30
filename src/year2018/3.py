import sys
import re

p = re.compile("#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")

YSIZE = 1000
XSIZE = 1000

area = []
claim = []
for i in range(YSIZE):
    area.append([0] * XSIZE)
    claim.append([-1] * XSIZE)

cnt = 0
can_be = set()

for line in sys.stdin.readlines():
    #1 @ 469,741: 22x26
    m = p.match(line.strip())
    [id, sx, sy, w, h] = map(lambda x:int(x), list(m.groups()))
    can_be.add(id)
    #print x,y,w,h
    for x in range(sx,sx+w):
        for y in range(sy,sy+h):
            area[y][x] += 1
            if area[y][x] == 2:
                cnt += 1
            if area[y][x] >= 2:
                can_be.discard(claim[y][x])
                can_be.discard(id)
            claim[y][x] = id

print cnt
print can_be

