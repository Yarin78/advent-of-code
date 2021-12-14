import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.graph import *
from yal.geo2d import *

data = [get_ints(line) for line in sys.stdin.readlines()]
lines = [Line(Point(d[0], d[1]), Point(d[2], d[3])) for d in data]

# part1 = defaultdict(int)
# part2 = defaultdict(int)
# for la, lb in itertools.combinations(lines, 2):
#     p = line_intersect_segment(la, lb, include_endpoints=True)
#     if p:
#         part2[p] += 1

# print(part2)
# print(sum(map(lambda v: v >= 2, part2.values())))

l1 = Line(Point(2,0), Point(4,0))
l2 = Line(Point(4,0), Point(4,2))
print(line_intersect_segment(l1, l2))
