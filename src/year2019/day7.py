import sys
from collections import defaultdict
from yal import util
from queue import Queue
from yal.geo2d import *
from intcode.intcode import *
from aocd import data, submit
from itertools import permutations

class PatchedProgram(Program):

    def intercept(self):
        # m0009 = self.input()          #   21: IN (9)
        # m0009 += 3                    #   23: ADD #3, (9), (9)
        # m0009 *= 3                    #   27: MUL #3, (9), (9)
        # m0009 += 5                    #   31: ADD (9), #5, (9)
        # self.output(m0009)            #   35: OUT (9)
        # self.halted = True
        # return     #   37: HALT

        if self.ip == 21:
            self.output((self.input() + 3) * 3 + 5)
            self.halted = True
            return True
        return False

prog = [PatchedProgram(data.strip(), i) for i in range(5)]

for part in range(2):
    best = 0
    for perm in permutations(range(5*part, 5*part+5)):
        pipes = [Queue() for p in prog]
        for i in range(5):
            prog[i].reset()
            prog[i].init_io(pipes[i], pipes[(i+1)%5])
            pipes[i].put(perm[i])
        pipes[0].put(0)
        threaded_executor(prog)

        best = max(best, prog[4].last_out)

    print(best)
