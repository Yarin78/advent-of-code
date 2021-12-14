import sys
from queue import Queue
from collections import defaultdict
from itertools import combinations, permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
# scanner = Scanner(sys.stdin)
lines = [line.strip() for line in sys.stdin.readlines()]

cur = lines[0] + "z"

mapper = {}
for line in lines[2:]:
    src, dest = tokenize(line)
    mapper[src[0] + src[1]] = [src[0] + dest[0], dest[0] + src[1]]

pair_cnt = defaultdict(int)
for i in range(len(cur)-1):
    pair_cnt[cur[i:i+2]] += 1

for steps in range(40):
    new_pair_cnt = defaultdict(int)
    for k,v in pair_cnt.items():
        replace = mapper[k] if k in mapper else [k]
        for new_pair in replace:
            new_pair_cnt[new_pair] += v

    pair_cnt= new_pair_cnt

counter = defaultdict(int)
for pair, cnt in pair_cnt.items():
    counter[pair[0]] += cnt

counter = list(sorted([(v, k) for k,v in counter.items()]))

print(counter[-1][0] - counter[0][0])


