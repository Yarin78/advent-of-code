import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.graph import *
from yal.geo2d import *

lines = [line.strip() for line in sys.stdin.readlines()]

MAX = 1000

m = init_matrix(MAX, MAX)
for line in lines:
    (x, y, x2, y2) = get_ints(line)
    m[y][x] += 1
    while x != x2 or y != y2:
        x += sign(x2-x)
        y += sign(y2-y)
        m[y][x] += 1

print(sum(m[y][x] >= 2 for y in range(MAX) for x in range(MAX)))
