from collections import defaultdict

GRID_SIZE = 300

serial = 3463
grid = []
for y in range(1,GRID_SIZE + 1):
    row = []
    for x in range(1,GRID_SIZE + 1):
        rack = x + 10
        power = (rack * y + serial) * rack
        power = (power / 100) % 10 - 5
        row.append(power)
    grid.append(row)


part_sum = []
best = 0
for y in range(0, GRID_SIZE):
    part_sum.append([])
    for x in range(0, GRID_SIZE):
        part_sum[y].append(grid[y][x] + (part_sum[y-1][x] if y > 0 else 0) + (part_sum[y][x-1] if x > 0 else 0) - (part_sum[y-1][x-1] if x > 0 and y > 0 else 0))

best = 0
for y in range(0, GRID_SIZE):
    for x in range(0, GRID_SIZE):
        for size in range(1, min(x,y)):
            sum = part_sum[y][x] - part_sum[y-size][x] - part_sum[y][x-size] + part_sum[y-size][x-size]
            if sum > best:
                best = sum
                bx = x - size + 2
                by = y - size + 2
                bs = size

#for line in grid:
#    print line
#print
#for line in part_sum:
#    print line

print 'Best sum %d at %d,%d,%d' % (best, bx, by, bs)
