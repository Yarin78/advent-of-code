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
prog = Program(data)

def run_springscript(code):
    prog.reset()
    prog.init_io(Queue(), Queue())
    print(prog.read_line())  # Input instructions:
    for line in code.strip().split('\n'):
        if line:
            prog.write_line(line)
    prog.run_until_halted()
    prog._output.get()
    print(prog.read_line())  # Walking
    print(prog.read_line())
    while not prog._output.empty():
        print(prog._output.get())

# part 1

springscript = '''
NOT A T
NOT B J
OR T J
NOT C T
OR T J
AND D J
WALK
'''

run_springscript(springscript)

# part 2

springscript = '''
OR E J
OR H J
AND D J
OR A T
AND B T
AND C T
NOT T T
AND T J
RUN
'''

run_springscript(springscript)
