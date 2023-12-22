import sys
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

lines = [line.strip() for line in sys.stdin.readlines()]

grid = Grid(lines)

start = grid.find_first('S')
assert start
grid.set(start, '.')

# Solution assumes these
assert grid.xsize == grid.ysize
assert grid.xsize % 2 == 1

graph = grid_graph(grid, ".")
dist = bfs(graph, start)

print(sum(d % 2 == 0 and d <= 64 for p, d in dist.items()))  # 3751

STEPS = 26501365
MOD = STEPS % 2

dist_nw = bfs(graph, Point(0,0))
dist_ne = bfs(graph, Point(grid.xsize-1,0))
dist_sw = bfs(graph, Point(0, grid.ysize-1))
dist_se = bfs(graph, Point(grid.xsize-1,grid.ysize-1))

dist_w = bfs(graph, Point(0, start.y))
dist_e = bfs(graph, Point(grid.xsize-1, start.y))
dist_n = bfs(graph, Point(start.x, 0))
dist_s = bfs(graph, Point(start.x, grid.ysize-1))

def count_diag(d):
    n = (STEPS - d - 2) // grid.xsize
    # Count number of ways to sum two non-negative integers so the sum is _at most_ n
    # and that the modulo of the final sum is either 0 or 1 depending on distance left
    if d % 2 == MOD:
        m = n // 2 + 1
        return m*m
    else:
        m = (n+1) // 2
        return m*(m+1)

def count_straight(d):
    n = (STEPS - d - 1) // grid.xsize
    # Count number of non-negative integers up to n
    # so that the modulo is either 0 or 1 depending on distance left
    return (n + 1 + (d % 2 != MOD)) // 2

IS_SAMPLE = grid.xsize == 11
INF = 99999999

count = 0
for p in grid.all_points():
    if grid.get(p) == '.' and p in dist:
        if dist[p] <= STEPS and dist[p] % 2 == MOD:
            count += 1

        count += count_diag(dist_nw[start] + dist_se[p])
        count += count_diag(dist_ne[start] + dist_sw[p])
        count += count_diag(dist_sw[start] + dist_ne[p])
        count += count_diag(dist_se[start] + dist_nw[p])
        # The real input guarantees walking in a straight line works
        # Could be made general by doing min to all points along the edges
        count += count_straight(min(dist_nw[start] + dist_sw[p], dist_ne[start] + dist_se[p], dist_n[start] + dist_s[p] if not IS_SAMPLE else INF))
        count += count_straight(min(dist_nw[start] + dist_ne[p], dist_sw[start] + dist_se[p], dist_w[start] + dist_e[p] if not IS_SAMPLE else INF))
        count += count_straight(min(dist_se[start] + dist_sw[p], dist_ne[start] + dist_nw[p], dist_e[start] + dist_w[p] if not IS_SAMPLE else INF))
        count += count_straight(min(dist_sw[start] + dist_nw[p], dist_se[start] + dist_ne[p], dist_s[start] + dist_n[p] if not IS_SAMPLE else INF))

print(count)  # 619407349431167
