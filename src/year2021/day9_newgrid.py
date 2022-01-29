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

def _is_node(p, c):
    return c != '9'

def _is_edge(p1, c1, p2, c2):
    return c2 > c1

graph = grid_graph(grid, _is_node, _is_edge)

tot_risk = 0
basins = []
for p in grid.all_points():
    if all(grid.get(p) < grid.get(q) for q in grid.neighbors(p)):
        tot_risk += int(grid.get(p))+1

        res = bfs(graph, p)
        basins.append(len(res))

print(tot_risk)
basins.sort()
print(basins[-1]*basins[-2]*basins[-3])
