import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
# scanner = Scanner(sys.stdin)
lines = [line.strip() for line in sys.stdin.readlines()]
# Split input into an array of array of lines, split by empty line
# sections = split_lines(lines)

part1 = part2 = 0
for line in lines:
    amin, amax, bmin, bmax = get_non_negative_ints(line)

    if (amin >= bmin and amax <= bmax) or (bmin >= amin and bmax <= amax):
        part1 += 1
    if not (amax < bmin or amin > bmax):
        part2 += 1

print(part1, part2)
