from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

grid = Grid.read()

steps = 0    
while True:
    steps += 1
    moved = False
    for y in range(grid.ysize):
        moving_x = [x for x in range(grid.xsize) if grid[y,x] == '>' and grid[y,(x+1)%grid.xsize] == '.']
        moved |= len(moving_x) > 0 
        for x in moving_x:
            grid[y,(x+1)%grid.xsize] = '>'
            grid[y,x] = '.'

    for x in range(grid.xsize):
        moving_y = [y for y in range(grid.ysize) if grid[y,x] == 'v' and grid[(y+1)%grid.ysize,x] == '.']
        moved |= len(moving_y) > 0 
        for y in moving_y:
            grid[(y+1)%grid.ysize,x] = 'v'
            grid[y,x] = '.'
        
    if not moved:
        break

    # print("After %d steps" % steps)
    # for y in range(ysize):
    #     print("".join(m[y]))
    # print()

print(steps)
