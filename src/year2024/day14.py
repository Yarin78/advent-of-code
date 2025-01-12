import sys
from dataclasses import dataclass
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

# Make sure ~/.config/aocd/token is correct! (Application tab -> Cookies)
# scanner = Scanner(sys.stdin)
lines = [line.strip() for line in sys.stdin.readlines()]
# Split input into an array of array of lines, split by empty line
# sections = split_lines(lines)

STEPS = 100
# XSIZE = 11
# YSIZE = 7
XSIZE = 101
YSIZE = 103

quad_cnt = defaultdict(int)

for line in lines:
    px, py, dx, dy = get_ints(line)
    p = Point(px, py)
    d = Point(dx, dy)

    tx = (px + dx * STEPS) % XSIZE
    ty = (py + dy * STEPS) % YSIZE
    assert tx >= 0 and ty >= 0

    if tx != XSIZE // 2 and ty != YSIZE // 2:
        if tx < XSIZE // 2:
            quad = 0 if ty < YSIZE // 2 else 1
        else:
            quad = 2 if ty < YSIZE // 2 else 3

        quad_cnt[quad] += 1

print(quad_cnt)
print(math.prod(quad_cnt.values()))


pos = []
dir = []

for line in lines:
    px, py, dx, dy = get_ints(line)
    pos.append(Point(px, py))
    dir.append(Point(dx, dy))

step = 0
w = defaultdict(int)
while step < 100000:
    step += 1
    if step % 100 == 0:
        print(f"Step {step}")
    neighbors = 0
    for i in range(len(pos)):
        pos[i] = Point((pos[i].x + dir[i].x) % XSIZE, (pos[i].y + dir[i].y) % YSIZE)
        # g[pos[i]] = '#'
        w[pos[i]] = step
        for d in DIRECTIONS_INCL_DIAGONALS:
            if w[pos[i] + d] == step:
                neighbors += 1

    if neighbors > 500:
        print(f"Neighbors at step {step}: {neighbors}")
        g = Grid.empty(XSIZE, YSIZE)
        for p in pos:
            g[p] = '#'
        print(f"Grid after {step} steps:")
        g.show()
        exit(0)