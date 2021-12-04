import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
lines = [line.strip() for line in sys.stdin.readlines()]

# data = [int(x) for x in lines]
t = 0
depth = 0
aim = 0

for line in lines:
    (d, cnt) = tokenize(line)
    if d == "forward":
        t += int(cnt)
        depth += aim*int(cnt)
    elif d == "down":
        aim += int(cnt)
    elif d == "up":
        aim -= int(cnt)

print(t, depth)
print(t * depth)
