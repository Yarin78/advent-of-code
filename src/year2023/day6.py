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

def count(time_avail, to_beat):
    cnt = 0
    for t in range(time_avail):
        rt = time_avail - t
        dist = t  * rt
        cnt += dist > to_beat
    return cnt

times = get_ints(lines[0])
dist_to_beat = get_ints(lines[1])

part1 = 1
for i in range(len(times)):
    part1 *= count(times[i], dist_to_beat[i])

print(part1)

part2_time = int(lines[0].replace(' ', '').split(':')[1])
part2_dist_to_beat = int(lines[1].replace(' ', '').split(':')[1])

print(count(part2_time, part2_dist_to_beat))
