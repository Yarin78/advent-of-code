import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

(grid, xsize, ysize) = read_grid()

def _is_node(p, c):
    return c != '9'

def _is_edge(p1, c1, p2, c2):
    return c2 > c1

graph = grid_graph(grid, _is_node, _is_edge)

tot = 0
sizes = []
for y in range(ysize):
    for x in range(xsize):
        is_low = True
        for d in DIRECTIONS:
            nx = x+ d.x
            ny = y+d.y
            if within_grid(grid, Point(nx, ny)):
                if grid[y][x] >= grid[ny][nx]:
                    is_low=False
        if is_low:
            risk = int(grid[y][x])+1
            tot+=risk

            res = bfs(graph, Point(x,y))
            sizes.append(len(res))

print(tot)
sizes.sort()
print(sizes[-1]*sizes[-2]*sizes[-3])
