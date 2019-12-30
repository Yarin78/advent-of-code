import sys
from collections import defaultdict
from lib import util
from queue import Queue
from lib.geo2d import *
from lib.intcode import *
from aocd import data, submit

# Make sure AOC_SESSION is updated! (Chrome inspector -> Application tab -> session)

#data = '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'
#data = '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'

lines = data.strip().split('\n')
prog = []

for i in range(5):
    prog.append(Program(data, i))

def go(perm, cur):
    if cur == 5:
        inp = 0
        q = []
        for i in range(5):
            qq = Queue()
            qq.put(perm[i])
            q.append(qq)
        for i in range(5):
            prog[i].reset()
            prog[i].init_io(q[i], q[(i+1)%5])
        q[0].put(0)

        parallel_executor(prog)
        return prog[4].last_out

    best = 0
    for i in range(5, 10):
        ok = True
        for j in range(cur):
            if perm[j] == i:
                ok = False
        if ok:
            perm[cur] = i
            best = max(best, go(perm, cur+1))

    return best

perm=[0]*5
best=go(perm, 0)
print(best)

# submit(?, part="a", day=7, year=2019)
# submit(?, part="b", day=7, year=2019)
