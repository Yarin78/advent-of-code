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

def get_diffs(ints):
    new_seq = [ints[i+1]-ints[i] for i in range(len(ints)-1)]
    if any(x for x in new_seq):
        (p1, p2) = get_diffs(new_seq)
        return (ints[-1] + p1, ints[0] - p2)
    else:
        return (ints[-1], ints[0])

part1 = 0
part2 = 0
for line in lines:
    seq = get_ints(line)

    (p1, p2) = get_diffs(seq)
    part1 += p1
    part2 += p2

print(part1)
print(part2)
