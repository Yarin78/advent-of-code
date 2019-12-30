import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from intcode.intcode import *
from aocd import data, submit

lines = data.strip().split('\n')
#prog = Program(data)

def bio(ll):
    a = 0
    b = 1
    for y in range(5):
        for x in range(5):
            if ll[y][x] == '#':
                a += b
            b *= 2
    return a

seen = set()
while True:
    code = ''.join(lines)
    if code in seen:
        print(bio(lines))
        break
    seen.add(code)
    for line in lines:
        print(line)
    print()
    nl = []
    for y in range(5):
        s = ''
        for x in range(5):
            p = Point(x,y)
            cnt = 0

            for d in DIRECTIONS:
                np = p+d
                if np.x >= 0 and np.y >= 0 and np.x < 5 and np.y < 5:
                    if lines[np.y][np.x] == '#':
                        cnt += 1

            if lines[p.y][p.x] == '#':
                if cnt == 1:
                    s += '#'
                else:
                    s += '.'
            else:
                if cnt == 2 or cnt == 1:
                    s += '#'
                else:
                    s += '.'
        nl.append(s)
    lines = nl