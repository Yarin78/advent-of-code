import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
# scanner = Scanner(sys.stdin)
lines = [line.strip() for line in sys.stdin.readlines()]
# Split input into an array of array of lines, split by empty line
# sections = split_lines(lines)

def dist(p1, p2):
    d = p1-p2
    return abs(d.x)+abs(d.y)

TARGET_Y = 2000000

MAXX=4000000
MAXY=4000000
poss = set()
beacons = set()
sensors = {}


def find_empty(iv: List[Tuple[int,int]]):
    iv = sorted(iv)
    #print(iv)

    stops = iv[0][1]
    assert iv[0][0] <= 0


    for i in range(1, len(iv)):
        if iv[i][0] > stops:
            return iv[i][0] - 1
        stops = max(stops, iv[i][1])

    assert stops >= MAXX
    return -1



ivals: Dict[int, List[Tuple[int,int]]] = {}
for y in range(MAXY+1):
    ivals[y] = []

for line in lines:
    sx, sy, bx, by = get_ints(line)
    beacons.add(Point(bx,by))
    d = abs(sx-bx)+abs(sy-by)
    sp = Point(sx,sy)
    sensors[sp] = d
    for ty in range(MAXY+1):
        ydist = abs(ty - sy)
        dleft = d - ydist
        r = (sx - dleft, sx + dleft+1)
        if dleft >= 0:
            ivals[ty].append(r)
    print(f"Sensor {sp} done")


for y in range(MAXY+1):
    ex = find_empty(ivals[y])
    # print(y, ex)
    if ex >= 0:
        ans = ex * 4000000 + y
        print(ex, y, ans)


# Y = 2000000
# cnt = 0
# for x in range(-2000000, 2000000):
#     can = True
#     p = Point(x,Y)
#     if p in sensors:
#         continue
#     if p in beacons:
#         continue
#     for spoint, closest in sensors.items():
#         #print(spoint, closest)
#         d = dist(spoint, p)
#         if d <= closest:
#             can = False
#             break
#     if not can:
#         # print(x)
#         cnt += 1

# print("ANS", cnt)

