import sys
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

rope = [Point(0,0) for _ in range(10)]
vis = [set() for _ in range(10)]

for line in sys.stdin.readlines():
    for step in range(int(line[2:])):
        rope[0] += DIRECTION_MAP[line[0]]
        for i in range(1, len(rope)):
            diff = rope[i-1]-rope[i]
            if abs(diff.x) == 2 or abs(diff.y) == 2:
                rope[i] += Point(sign(diff.x), sign(diff.y))
            vis[i].add(rope[i])

print(len(vis[1]), len(vis[9]))
