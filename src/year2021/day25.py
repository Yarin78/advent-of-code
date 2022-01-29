from yal.io import *
from yal.util import *
from yal.grid_old import *
from yal.graph import *
from yal.geo2d import *

(grid, xsize, ysize) = read_grid()
m = grid_split(grid)

steps = 0    
while True:
    steps += 1
    moved = False
    for y in range(ysize):
        moving_x = [x for x in range(xsize) if m[y][x] == '>' and m[y][(x+1)%xsize] == '.']
        moved |= len(moving_x) > 0 
        for x in moving_x:
            m[y][(x+1)%xsize] = '>'
            m[y][x] = '.'

    for x in range(xsize):
        moving_y = [y for y in range(ysize) if m[y][x] == 'v' and m[(y+1)%ysize][x] == '.']
        moved |= len(moving_y) > 0 
        for y in moving_y:
            m[(y+1)%ysize][x] = 'v'
            m[y][x] = '.'
        
    if not moved:
        break

    # print("After %d steps" % steps)
    # for y in range(ysize):
    #     print("".join(m[y]))
    # print()

print(steps)
