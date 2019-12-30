import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from intcode.intcode import *
from aocd import data, submit

queues = []
nat_mem = None
last_y = -1

class Receiver(BaseInput):
    def __init__(self, nic):
        self.nic = nic

    def get(self):
        global queues, last_y
        if queues[self.nic].empty():
            if self.nic == 0:
                for i in range(50):
                    if nat_mem and all(q.empty() for q in queues):
                        print(nat_mem)
                        if last_y == nat_mem[1]:
                            exit(0)
                        last_y = nat_mem[1]
                        queues[0].put(nat_mem[1])
                        return nat_mem[0]
            return -1
        return queues[self.nic].get()


class Sender:
    def __init__(self, nic):
        self.nic = nic
        self.state = 0
        self.target = 0

    def put(self, value):
        global queues, nat_mem
        if self.state == 0:
            self.target = value
            self.state += 1
        elif self.state == 1:
            self.x = value
            self.state += 1
        else:
            if self.target == 255:
                nat_mem = (self.x, value)
            else:
                queues[self.target].put(self.x)
                queues[self.target].put(value)
            self.state = 0

lines = data.strip().split('\n')
progs=[]
for i in range(50):
    prog = Program(data)
    prog.init_io(Receiver(i), Sender(i))
    q = Queue()
    q.put(i)
    queues.append(q)
    progs.append(prog)

parallel_executor(progs)

