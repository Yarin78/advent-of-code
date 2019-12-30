import sys
from collections import defaultdict
from yal import util
from intcode import intcode
from queue import Queue
from aocd import data, submit

prog = intcode.Program(data)
#prog.log_info()

prog.write(1, 12)
prog.write(2, 2)
prog.run()

print(prog.read(0))
print()

prog.log_warn()

for noun in range(100):
    for verb in range(100):
        prog.reset()
        prog.write(1, noun)
        prog.write(2, verb)

        prog.run()
        if prog.read(0) == 19690720:
            print(100*noun + verb)


# submit(cnt, part="a", day=2, year=2019)
