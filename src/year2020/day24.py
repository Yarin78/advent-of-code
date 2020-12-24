import sys
from collections import defaultdict
from yal.geo2d import *
from yal.hexgrid import *

flipped = defaultdict(bool)
for line in sys.stdin.readlines():
    count = {s: line.count(s) for s in HEX_DIRS_EW.keys()}
    count["e"] -= count["se"] + count["ne"]
    count["w"] -= count["sw"] + count["nw"]
    p = sum((HEX_DIRS_EW[d] * cnt for d, cnt in count.items()), start=Point(0,0))
    flipped[p] = not flipped[p]

flipped = set(p for p, v in flipped.items() if v)
print(len(flipped))  # part 1

for day in range(100):
    bb = Point.bounding_box(flipped)
    flipped = {p for p in Point.range(bb[0]-Point(1,1), bb[1]+Point(2,2)) if sum(p+d in flipped for d in HEX_DIRS_EW.values()) in [2-(p in flipped),2]}
print(len(flipped))  # part 2
