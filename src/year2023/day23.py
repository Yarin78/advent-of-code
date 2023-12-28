import sys
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.nxgraph import *
from yal.geo2d import *

lines = [line.strip() for line in sys.stdin.readlines()]

grid = Grid(lines)

start = Point(1, 0)
goal = Point(grid.xsize - 2, grid.ysize - 1)

SLOPES = {">": EAST, "<": WEST, "^": NORTH, "v": SOUTH}

g = grid_graph(
    grid,
    ".<>^v",
    graph=nx.DiGraph,
    get_edge=lambda p1, c1, p2, _: 1 if c1 == "." or p1 + SLOPES[c1] == p2 else False,
    uni_distance=False,
)

compress_paths(g)
part1, _ = longest_path(g, start, goal)
print(part1)  # 2178

g = grid_graph(grid, ".<>^v", graph=nx.Graph, uni_distance=False)
g = nx.convert_node_labels_to_integers(g, label_attribute = "point")

new_start = next(node for node, d in g.nodes(data=True) if d['point']==start)
new_goal = next(node for node, d in g.nodes(data=True) if d['point']==goal)

compress_paths(g)

part2, path = longest_path(g, new_start, new_goal)
print(part2)  # 6486

node_colors = {v: "blue" for v in path}
edge_colors = {(path[i], path[i+1]): "blue" for i in range(len(path) - 1)}

show_graph(g, node_colors={**node_colors, new_start: "green", new_goal: "red"}, edge_colors=edge_colors)
