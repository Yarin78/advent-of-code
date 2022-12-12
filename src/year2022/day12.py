from yal.grid import *
from yal.graph import *

def _is_forward_edge(p1:Point, c1:str, p2:Point, c2:str):
    return ord(c2)<=ord(c1)+1

def _is_back_edge(p1:Point, c1:str, p2:Point, c2:str):
    return ord(c1)<=ord(c2)+1

def _is_node(p1:Point, c1:str):
    return True

grid = Grid.read()
start = grid.find('S')[0]
goal = grid.find('E')[0]

grid[start] = 'a'
grid[goal] = 'z'

g = grid_graph(grid, is_node=_is_node, get_edge=_is_forward_edge)

part1 = bfs(g, start)
print(part1[goal])

g = grid_graph(grid, is_node=_is_node, get_edge=_is_back_edge)
res = bfs(g, goal)

print(min(res[p] for p in res.keys() if grid[p] == 'a'))
