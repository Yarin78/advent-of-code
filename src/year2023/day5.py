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

seeds = get_ints(sections[0][0])

mappers = []

for section in sections[1:]:
    cur_mapper = []
    for mapper in section[1:]:
        (dest, src, count) = get_ints(mapper)
        cur_mapper.append((dest, src, count))

    mappers.append(cur_mapper)

INF = 1000000000000

def map_it(cur):
    global mappers
    next_change = INF
    for mapper in mappers:
        did_map = False
        for (dest, src, count) in mapper:
            if cur >= src and cur < src + count:
                next_change = min(next_change, src + count - cur)
                cur = dest + cur - src
                did_map = True
                break
        if not did_map:
            closest = INF
            for (dest, src, count) in mapper:
                if src > cur:
                    closest = min(closest, src - cur)
            next_change = min(next_change, closest)

    return cur, next_change

print("Part 1:", min(map_it(c) for c in seeds)[0])

best = INF
for seed, seed_len in pair_up(seeds):
    c = seed
    while c < seed + seed_len:
        location, next_change = map_it(c)
        best = min(best, location)
        c += next_change

print("Part 2:", best)
