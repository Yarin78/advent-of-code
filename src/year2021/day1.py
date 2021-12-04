import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
lines = [line.strip() for line in sys.stdin.readlines()]

data = [int(x) for x in lines]
cnt = 0
last = 0
for i in range(len(data)):
    if i < 2:
        continue
    a = data[i] + data[i-1] + data[i-2]
    print(a)
    if a > last and last > 0:
        cnt += 1
    last = a

print(cnt)
