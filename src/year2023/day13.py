import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

lines = [line.strip() for line in sys.stdin.readlines()]
sections = split_lines(lines)

part1 = 0
part2 = 0
for section in sections:
    grid = Grid(section)

    rows = []
    cols = []
    for y in range(grid.ysize):
        mask = 0
        for x in range(grid.xsize):
            mask = mask * 2 + (1 if grid.get(Point(x,y)) == '#' else 0)
        rows.append(mask)
    for x in range(grid.xsize):
        mask = 0
        for y in range(grid.ysize):
            mask = mask * 2 + (1 if grid.get(Point(x,y)) == '#' else 0)
        cols.append(mask)

    def find_split(rows, size):
        for split in range(1, size):
            match = True
            for i in range(size):
                if split-1-i < 0 or split+i >= size:
                    break
                if not rows[split-1-i] == rows[split+i]:
                    match = False

            if match:
                return split
        return 0

    def is_matching(mask1, mask2, can_change):
        if not can_change:
            return mask1 == mask2
        return count_bits(max(mask1, mask2)-min(mask1, mask2)) == 1

    def find_near_split(rows, size, old_split):
        for changed in range(0,size):
            for split in range(1, size):
                if split == old_split:
                    continue
                match = True
                for i in range(size):
                    if split-1-i < 0 or split+i >= size:
                        break
                    if not is_matching(rows[split-1-i], rows[split+i], split-1-i == changed or split+i == changed):
                        match = False

                if match:
                    return split
        return 0

    ysplit = find_split(rows, grid.ysize)
    xsplit = find_split(cols, grid.xsize)
    part1 += ysplit * 100 + xsplit

    ysplit2 = find_near_split(rows, grid.ysize, ysplit)
    xsplit2 = find_near_split(cols, grid.xsize, xsplit)
    part2 += ysplit2 * 100 + xsplit2

print(part1)
print(part2)
