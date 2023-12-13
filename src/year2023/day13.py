import sys
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

lines = [line.strip() for line in sys.stdin.readlines()]
sections = split_lines(lines)

part = [0, 0]
for section in sections:
    grid = Grid(section)

    rows = grid.get_row_masks('.')
    cols = grid.get_col_masks('.')

    def find_split(ints, target, mult):
        splits = []
        size = len(ints)
        for split in range(1, size):
            bits_differ = 0
            for i in range(size):
                if split-1-i < 0 or split+i >= size:
                    break
                bits_differ += count_bits(ints[split-1-i]^ints[split+i])

            if bits_differ == target:
                splits.append(split * mult)
        return splits

    for p in range(2):
        splits = [*find_split(rows, p, 100), *find_split(cols, p, 1)]
        assert len(splits) == 1
        part[p] += max(splits)

print(part)
