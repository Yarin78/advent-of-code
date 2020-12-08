import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from aocd import data, submit

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
lines = data.strip().split('\n')
# intlines = [int(x) for x in lines]
ans = ans2 = 0

lines.append("")
mask1 = 0
mask2 = (1<<26)-1
for line in lines:
    if line == "":
        ans += count_bits(mask1)
        ans2 += count_bits(mask2)
        mask1 = 0
        mask2 = (1<<26)-1
    else:
        mask1 |= string_to_mask(line)
        mask2 &= string_to_mask(line)


print(ans, ans2)
# submit(ans, part="a", day=6, year=2020)
# submit(ans2, part="b", day=6, year=2020)
