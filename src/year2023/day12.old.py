import sys
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

lines = [line.strip() for line in sys.stdin.readlines()]

part1 = 0
for line in lines:
    pattern, counts = line.split(' ')
    counts = get_ints(counts)

    poss = 0
    for p in replace_wildcards(pattern, "?", [".", "#"]):
        actual = []
        for part in p.split('.'):
            if len(part):
                actual.append(len(part))

        if actual == counts:
            poss += 1

    part1 += poss

print(part1)
