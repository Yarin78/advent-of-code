import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from intcode.intcode import *
from aocd import data, submit

lines = data.strip().split('\n')
prog = Program(data)
prog.run()

#prog = Program(data)
#prog.run([2])
