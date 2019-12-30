import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from intcode.intcode import *
from aocd import data, submit

data = data.strip()
offset=int(data[0:7])

reps = 10000
data = data * reps

data=intify(list(data))
n=len(data)

for iter in range(100):
    print("iter %d" % (iter+1))
    for x in range(1, n//2):
        data[n-x-1] = (data[n-x] + data[n-x-1]) % 10
        if n-x-1 == offset:
            break

print (''.join([str(x) for x in data[offset:offset+8]]))
