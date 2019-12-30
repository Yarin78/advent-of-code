import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from lib import util
from lib.graph import *
from lib.geo2d import *
from lib.intcode import *
from aocd import data, submit

map = {}
score = 0
ballx = 0
paddlex = 0

class Reader(BaseInput):
    def get(self):
        if paddlex < ballx:
            return 1
        if paddlex > ballx:
            return -1
        return 0


class Writer:
    p = 0
    x = 0
    y = 0

    def put(self, v):
        global map,score, ballx, paddlex


        if self.p == 0:
            self.x = v
        elif self.p == 1:
            self.y = v
        else:
            if self.x==-1 and self.y==0:
                score = v
                #print('score = %d' % score)
            else:
                if v == 4:
                    #print('ball at %x,%x' % (self.x,self.y))
                    ballx = self.x
                    map[Point(self.x,self.y)] = 0
                elif v == 3:
                    #print('paddle at %x,%x' % (self.x,self.y))
                    paddlex = self.x
                    map[Point(self.x,self.y)] = 0
                else:
                    map[Point(self.x,self.y)] = v

        self.p = (self.p+1)%3

lines = data.strip().split('\n')
prog = Program(data)

prog.run(Reader(), Writer())

cnt = 0
for p,v in map.items():
    if v == 2:
        cnt += 1

util.print_array(util.gridify_sparse_map(map))

print("%d block tiles" % cnt)

prog.reset()
prog.mem[0] = 2
prog.run(Reader(), Writer())

print(score)
