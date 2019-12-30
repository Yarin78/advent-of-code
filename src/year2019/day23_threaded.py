import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from lib.util import *
from lib.graph import *
from lib.geo2d import *
from lib.intcode import *
from aocd import data, submit


queues = []
blocked = [False] * 50
nat_mem = None
last_y = 0

class Receiver(BaseInput):
    def __init__(self, nic):
        self.nic = nic

    def get(self):
        global queues, blocked
        blocked[self.nic] = True
        value = queues[self.nic].get()
        blocked[self.nic] = False
        return value

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
    q.put(-1)
    queues.append(q)
    progs.append(prog)

def NAT():
    global nat_mem, blocked, queues, last_y
    while True:
        if all(blocked[i] and queues[i].empty() for i in range(50)):
            print('blocked', nat_mem)
            if nat_mem:
                (x,y) = nat_mem
                queues[0].put(x)
                queues[0].put(y)
                if y == last_y:
                    print('done', y)
                    exit(0)
                last_y = y


t = threading.Thread(target=NAT)
t.start()
threaded_executor(progs)
t.join()
