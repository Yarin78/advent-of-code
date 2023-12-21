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

dist = bfs(grid_graph(grid, lambda p, c: c == '.', lambda p1,c1,p2,c2: c1 == '.' and c2 == '.'), start)

print(sum(d % 2 == 0 and d <= 64 for p, d in dist.items()))

STEPS = 26501365
MOD = STEPS % 2

dist_nw = bfs(grid_graph(grid, lambda p, c: c == '.', lambda p1,c1,p2,c2: c1 == '.' and c2 == '.'), Point(0,0))
dist_ne = bfs(grid_graph(grid, lambda p, c: c == '.', lambda p1,c1,p2,c2: c1 == '.' and c2 == '.'), Point(grid.xsize-1,0))
dist_sw = bfs(grid_graph(grid, lambda p, c: c == '.', lambda p1,c1,p2,c2: c1 == '.' and c2 == '.'), Point(0, grid.ysize-1))
dist_se = bfs(grid_graph(grid, lambda p, c: c == '.', lambda p1,c1,p2,c2: c1 == '.' and c2 == '.'), Point(grid.xsize-1,grid.ysize-1))

dist_w = bfs(grid_graph(grid, lambda p, c: c == '.', lambda p1,c1,p2,c2: c1 == '.' and c2 == '.'), Point(0, start.y))
dist_e = bfs(grid_graph(grid, lambda p, c: c == '.', lambda p1,c1,p2,c2: c1 == '.' and c2 == '.'), Point(grid.xsize-1, start.y))
dist_n = bfs(grid_graph(grid, lambda p, c: c == '.', lambda p1,c1,p2,c2: c1 == '.' and c2 == '.'), Point(start.x, 0))
dist_s = bfs(grid_graph(grid, lambda p, c: c == '.', lambda p1,c1,p2,c2: c1 == '.' and c2 == '.'), Point(start.x, grid.ysize-1))


@functools.cache
def count_it(n, d):
    cnt2 = 0
    # This should be possible to do in a closed formula
    for s in range(0, n+1):
        if (s + d) % 2 == MOD:
            cnt2 += s + 1
    return cnt2

def count_diag(d):
    return count_it((STEPS - d - 2) // grid.xsize, d%2)

def count_straight(d):
    n = (STEPS - d - 1) // grid.xsize
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

print(count)
