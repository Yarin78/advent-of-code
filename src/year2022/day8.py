from yal.grid import *

grid = Grid.read()

part1 = set()
part2 = 0
for p in grid.all_points():
    v = 1
    for d in DIRECTIONS:
        cp = p + d
        cnt = 0
        while grid.is_within(cp):
            cnt += 1
            if grid[cp]>=grid[p]:
                break
            cp += d
        if not grid.is_within(cp):
            part1.add(p)
        v *= cnt
    part2=max(part2, v)

print(len(part1), part2)
