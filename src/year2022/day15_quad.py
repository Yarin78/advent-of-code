import sys
from yal.util import *

# Sample
# TARGET_Y = 10
# MAXX = 20
# MAXY = 20

# Actual
TARGET_Y = 2000000
MAXX=4000000
MAXY=4000000

sensors: List[Tuple[int, int, int]] = []

for line in sys.stdin.readlines():
    sx, sy, bx, by = get_ints(line)
    sensors.append((sx, sy, abs(sx-bx)+abs(sy-by)))

def find_point(x1: int, y1: int, x2: int, y2: int):
    if x1 == x2 or y1 == y2:
        return None

    for sx, sy, safe_dist in sensors:
        if (safe_dist >= abs(sx-x1)+abs(sy-y1) and
            safe_dist >= abs(sx-x1)+abs(sy-(y2-1)) and
            safe_dist >= abs(sx-(x2-1))+abs(sy-y1) and
            safe_dist >= abs(sx-(x2-1))+abs(sy-(y2-1))):
            return None

    if x1+1 == x2 and y1+1 == y2:
        return (x1,y1)

    mx = (x1+x2)//2
    my = (y1+y2)//2

    return (find_point(x1, y1, mx, my) or find_point(mx, y1, x2, my) or
        find_point(x1, my, mx, y2) or find_point(mx, my, x2, y2))


# Part 2 only
p = find_point(0, 0, MAXX+1, MAXY+1)
assert p
print(p[0] * 4000000 + p[1])
