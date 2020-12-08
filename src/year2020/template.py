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
#with open("dayx-sample.in", "r") as f:
#    lines = f.readlines()

# intlines = [int(x) for x in lines]
ans = ans2 = 0

print(ans)
# submit(ans, part="a", day=CHANGE, year=2020)
# submit(ans2, part="b", day=CHANGE, year=2020)
