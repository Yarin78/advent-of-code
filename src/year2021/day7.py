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
data = get_ints(lines[0])

best = 9999999999999
a=min(data)
b=max(data)
print(a,b)
for x in range(a,b+1):
    cost = 0
    for y in data:
        n = abs(y-x)
        cost += n*(n+1)//2

    if cost < best:
        best = cost

print(best)
