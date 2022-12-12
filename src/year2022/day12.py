from yal.grid import *
from yal.graph import *

grid = Grid.read()

start = grid.find_and_replace('S', 'a')[0]
goal = grid.find_and_replace('E', 'z')[0]

g = grid_graph(grid, get_edge=lambda p1,c1,p2,c2:ord(c2) <= ord(c1)+1)

print(bfs(g, start)[goal])
print(bfs(g, grid.find('a'))[goal])
