import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal import util
from yal.grid import *
from yal.graph import *
from yal.geo2d import *
from intcode.intcode import *
from aocd import data, submit

lines = data.strip().split('\n')

DIRECTIONS = [NORTH, EAST, SOUTH, WEST]

class Reader(BaseInput):
    def get(self):
        global dir, pos, map
        return map[pos]

class Writer:
    p = 0

    def put(self, v):
        global dir, pos, map
        if self.p == 0:
            map[pos] = v
            self.p = 1
        elif self.p == 1:
            if v == 0:
                dir = (dir+3)%4
            else:
                dir = (dir+1)%4
            pos += DIRECTIONS[dir]
            self.p = 0

prog = Program(data)

# Star 1
pos=Point(0,0)
dir=0

map = defaultdict(int)

prog.run(Reader(), Writer())

print(len(map))

# Star 2
pos=Point(0,0)
dir=0

map = defaultdict(int)
map[Point(0,0)] = 1

prog.reset()
prog.run(Reader(), Writer())

print_array(gridify_sparse_map(map))
