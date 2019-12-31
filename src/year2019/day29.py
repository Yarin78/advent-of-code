import sys
import random
from queue import Queue
from collections import defaultdict
from itertools import permutations
from intcode.intcode import *

data = sys.stdin.readline()

prog = Program(data)
#prog.log_info()
prog.init_io(Queue(), Queue())
print('Size: %d' % len(prog.mem))
#prog.show(0)
#exit(0)


inputs = []
for i in range(100):
    data = [random.randrange(1, 1000) for x in range(100)]
    inputs.append(data)


max_instr = 0
for data in inputs:
    prog.reset()
    prog._input.put(len(data))
    for x in data:
        prog._input.put(x)
    prog.run_until_halted()

    if prog.count > max_instr:
        max_instr=prog.count
    #print(prog.mem)

    output = []
    while not prog._output.empty():
        output.append(prog._output.get())
    #print(output)
    assert output == sorted(data), 'Got %s, expected %s' % (str(output), str(sorted(data)))
    print(len(data), prog.count)

#print(max_instr)

# 10 => 1400
# 100 => 23400
# 1000 => 326742
# 10000 => 4240582
