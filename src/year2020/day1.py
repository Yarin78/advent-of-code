import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from aocd import data, submit

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
#with open("day1.in", "r") as f:
#    lines = f.readlines()
ans = 0
lines = data.strip().split('\n')
ints = [int(x) for x in lines]
for x in ints:
    for y in ints:
        for z in ints:
            if x+y+z==2020:
                ans=x*y*z
print(ans)
# submit(ans, part="a", day=1, year=2020)
#submit(ans, part="b", day=1, year=2020)
