import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid_old import *
from yal.graph import *
from yal.geo2d import *

lines = [line.strip() for line in sys.stdin.readlines()]

algo = lines[0]

grid, xsize, ysize = read_grid(lines[2:])
image = init_matrix(xsize, ysize, '.')
for y in range(ysize):
    for x in range(xsize):
        image[y][x] = grid[y][x]

def show(image):
    for row in image:
        print(''.join(row))
    print()

def cnt(image):
    sum = 0
    for row in image:
        for col in row:
            sum += col == '#'
    return sum

#show(image)
for steps in range(50):
    ysize = len(image)
    xsize = len(image[0])
    new_image = init_matrix(ysize+2, xsize+2, '.')
    for y in range(ysize+2):
        for x in range(xsize+2):
            num = 0
            for dy in range(-1,2):
                for dx in range(-1,2):
                    p = 0
                    ny = y+dy-1
                    nx = x+dx-1
                    if nx >= 0 and nx < xsize and ny >= 0 and ny < ysize:
                        p = image[ny][nx] == '#'
                    else:
                        p = algo[0]=='#' if steps%2==1 else 0
                    num = num * 2 + p

            new_image[y][x] = algo[num]

    image = new_image
    #show(image)
    print(steps, cnt(image))
