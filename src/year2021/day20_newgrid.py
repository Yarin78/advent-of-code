import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

lines = [line.strip() for line in sys.stdin.readlines()]

algo = lines[0]

image = Grid(lines[2:])

# image.show()
# print()
for steps in range(50):
    def trans(grid: Grid, x, y):
        global algo, steps
        num = 0
        for dy in range(-1,2):
            for dx in range(-1,2):
                p = Point(x+dx, y+dy)
                c = grid.get_safe(p) or ('#' if algo[0] == '#' and steps%2 else '.')
                num = num * 2 + (c == '#')
        return algo[num]

    image = image.transform(trans, 1)
    
    # image.show()
    # print()
    print(steps, len(image.find('#')))
