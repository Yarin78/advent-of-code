from collections import defaultdict
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.nxgraph import *
from yal.geo2d import *

grid = Grid.read()

g1 = nx.DiGraph()
g2 = nx.DiGraph()
for p in grid.all_points():
    for lastdir in [NORTH, SOUTH, EAST, WEST]:
        for dir in [NORTH, SOUTH, EAST, WEST]:
            if dir.x == lastdir.x or dir.y == lastdir.y:
                continue
            cost = 0
            np = p
            for d in range(10):
                np = np + dir
                if grid.is_within(np):
                    cost += int(grid.get(np))
                    if d <= 2:
                        g1.add_edge((p,lastdir), (np, dir), cost=cost)
                    if d >= 3:
                        g2.add_edge((p,lastdir), (np, dir), cost=cost)
                else:
                    break



startp = Point(0,0)
endp = Point(grid.xsize-1, grid.ysize-1)

def solve(graph):
    best = 9999999
    for startdir in [WEST, NORTH]:
        res=nx.shortest_path_length(graph, (startp, startdir), weight="cost")
        for enddir in [EAST, SOUTH]:
            best = min(best, res[(endp, enddir)])
    return best

print("Running Dijkstra")

print(solve(g1))
print(solve(g2))
