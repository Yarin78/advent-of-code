import sys
from yal.util import *
from yal.grid import *

grid = Grid.empty(1000, 170)

maxy = 0
for line in sys.stdin.readlines():
    pairs = pair_up(get_ints(line))
    for i in range(1, len(pairs)):
        src = Point(pairs[i-1][0], pairs[i-1][1])
        dest = Point(pairs[i][0], pairs[i][1])
        grid.set(src, '#')
        while src != dest:
            src = src + Point(sign(dest.x-src.x), sign(dest.y-src.y))
            grid.set(src, '#')
            if src.y > maxy:
                maxy = src.y

floory = maxy+2
for x in range(1000):
    grid[floory,x] = '#'

part1 = 0
part2 = 0
part1_done = False
while grid[0,500] == '.':
    y = 0
    x = 500

    while True:
        if grid[y+1,x] == '.':
            y += 1
        elif grid[y+1,x-1] == '.':
            y += 1
            x -= 1
        elif grid[y+1,x+1] == '.':
            y += 1
            x += 1
        else:
            grid[y,x] = 'O'
            if y == floory-1:
                part1_done = True
            part1 += not part1_done
            part2 += 1
            break

print(part1, part2)
