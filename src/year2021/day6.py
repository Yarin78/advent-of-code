import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.graph import *
from yal.geo2d import *

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
# scanner = Scanner(sys.stdin)
lines = [line.strip() for line in sys.stdin.readlines()]

timers = defaultdict(int)
for x in map(int, lines[0].split(',')):
    timers[x] += 1

day = 0
while day < 256:
    day += 1

    new_timers = defaultdict(int)
    for k,v in timers.items():
        k -= 1
        if k < 0:
            new_timers[6] += v
            new_timers[8] += v
        else:
            new_timers[k] += v
    timers = new_timers

print(sum(timers.values()))
