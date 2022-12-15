import sys
from typing import Dict
from yal.util import *
from yal.geo2d import *

# Sample
# TARGET_Y = 10
# MAXX = 20
# MAXY = 20

# Actual
# Really slow though, 100 seconds :(
TARGET_Y = 2000000
MAXX=4000000
MAXY=4000000

sensors: Dict[Point, Point] = {}

for line in sys.stdin.readlines():
    sx, sy, bx, by = get_ints(line)
    sensors[Point(sx, sy)] = Point(bx,by)

possible = set()

for y in range(MAXY+1):
    ivals = []
    for sp, bp in sensors.items():
        manhattan_dist = abs(sp.x-bp.x)+abs(sp.y-bp.y)
        ydist = abs(y - sp.y)
        dleft = manhattan_dist - ydist
        if dleft >= 0:
            ival = (sp.x - dleft, sp.x + dleft+1)
            ivals.append(ival)
            if y == TARGET_Y:
                possible.update(range(ival[0], ival[1]))

    # Ugly, assumes the looked for point is not at the edges
    last_stop = 0
    for a, b in sorted(ivals):
        if a > last_stop:
            print("Part 2:", last_stop * 4000000 + y)
        last_stop = max(last_stop, b)

possible.difference_update([beacon.x for beacon in sensors.values() if beacon.y == TARGET_Y])
print("Part 1:", len(possible))
