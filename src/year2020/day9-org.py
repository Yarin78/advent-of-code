import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from vm.vm import *
from aocd import data, submit

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
lines = data.strip().split('\n')
#with open("dayx-sample.in", "r") as f:
#    lines = f.readlines()
# prog = Program(lines)

intlines = [int(x) for x in lines]
ans = ans2 = 0
for i in range(len(intlines)):
    sums=set()
    for j in range(25):
        for k in range(25):
            if j != k and i-j-1>= 0 and i-k-1 >= 0:
                sums.add(intlines[i-j-1]+intlines[i-k-1])
    if i >= 25 and intlines[i] not in sums:
        print(intlines[i])
        exit(0)

print(ans)
# submit(ans, part="a", day=CHANGE, year=2020)
# submit(ans2, part="b", day=CHANGE, year=2020)
