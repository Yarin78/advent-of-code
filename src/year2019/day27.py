import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from lib.util import *
from lib.graph import *
from lib.geo2d import *
from lib.intcode import *

data = sys.stdin.readline()

prog = Program(data)
#prog.log_info()
prog.init_io(Queue(), Queue())
print('Size: %d' % len(prog.mem))
prog.show(0)
#exit(0)
prog._input.put(123)
while not prog.halted:
    s = prog.read_line()
    if s:
        print(s)
