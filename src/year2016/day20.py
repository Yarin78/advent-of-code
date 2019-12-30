import sys
import re
import itertools
import hashlib
from collections import defaultdict
from lib.util import get_ints

input = sys.stdin
input = open('year2016/day20.in')
#input = open('year2016/day20.sample.in')

MAX_VALUE = 4294967295
#MAX_VALUE = 10

ranges = []
for line in input.readlines():
    parts = line.strip().split('-')
    start = int(parts[0])
    stop = int(parts[1])
    ranges.append((start, 0))
    ranges.append((stop+1, 1))

ranges.sort()
#print(ranges)
inside_cnt = 0
if ranges[0][0] != 0:
    print(0)
    exit(0)

empty_start = 0
allowed = 0
for (pos,type) in ranges:
    if type == 0:
        if inside_cnt == 0:
            allowed += pos - empty_start
        inside_cnt += 1
    else:
        inside_cnt -= 1
        if inside_cnt == 0:
            #print(pos)
            empty_start = pos

allowed += MAX_VALUE - empty_start + 1

print(allowed)