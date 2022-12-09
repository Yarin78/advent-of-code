import sys
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

rope = [Point(0,0) for _ in range(10)]
tail_vis = set([rope[-1]])

for line in sys.stdin.readlines():
    dir = DIRECTION_MAP[line[0]]

    for step in range(int(line[2:])):
        rope[0] += dir
        for i in range(1, len(rope)):
            diff = rope[i-1]-rope[i]
            if abs(diff.x) == 2 or abs(diff.y) == 2:
                rope[i] += Point(sign(diff.x), sign(diff.y))

        tail_vis.add(rope[-1])

print(len(tail_vis))
