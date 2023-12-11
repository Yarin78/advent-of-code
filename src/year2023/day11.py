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
emptyy = set(grid.get_empty_rows('.'))
emptyx = set(grid.get_empty_cols('.'))

points = grid.find('#')
answer = [0, 0]
for p,q in itertools.combinations(points, 2):
    x1,x2=sorted([p.x,q.x])
    y1,y2=sorted([p.y,q.y])
    for part, expand in enumerate([1, 1000000-1]):
        xdist = x2-x1 + sum(x in emptyx for x in range(x1+1,x2)) * expand
        ydist = y2-y1 + sum(y in emptyy for y in range(y1+1,y2)) * expand
        answer[part] += xdist+ydist

print(answer)
