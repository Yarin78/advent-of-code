import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

grid = Grid.read()

e = grid.to_ints()

flashes = 0
steps = 0
while True:
    steps += 1
    fq = []
    for p in grid.all_points():
        e[p.y][p.x] += 1
        if e[p.y][p.x] == 10:
            fq.append(p)

    flashed = []
    while len(fq) > 0:
        flashes += 1
        p = fq.pop()
        flashed.append(p)
        for np in grid.neighbors(p, 8):
            e[np.y][np.x] += 1
            if e[np.y][np.x] == 10:
                fq.append(np)

    for p in flashed:
        e[p.y][p.x] = 0

    if steps == 100:
        print("part 1", flashes)

    if len(flashed) == 100:
        print("part 2", steps)
        break
