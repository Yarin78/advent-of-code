import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

def solve(data, exp):
    ysize = len(data)
    xsize = len(data[0])

    map = []
    for tiley in range(exp):
        for y in range(ysize):
            cur = ""
            for tilex in range(exp):
                for x in range(xsize):
                    v = int(lines[y][x])
                    v = v + tiley+tilex
                    while v > 9:
                        v -= 9
                    cur += str(v)
            map.append(cur)

    (grid, xsize, ysize) = read_grid(map)

    def _get_node(p, c):
        return True

    def _get_edge(p1, c1, p2, c2):
        return int(c2)

    g = grid_graph(grid, _get_node, _get_edge, uni_distance=False)

    res = dijkstra(g, Point(0,0))

    return(res[Point(xsize-1,ysize-1)])


lines = [line.strip() for line in sys.stdin.readlines()]

print(solve(lines, 1))
print(solve(lines, 5))
