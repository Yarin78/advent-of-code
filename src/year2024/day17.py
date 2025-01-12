import sys
from dataclasses import dataclass
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

# Make sure ~/.config/aocd/token is correct! (Application tab -> Cookies)
# scanner = Scanner(sys.stdin)
lines = [line.strip() for line in sys.stdin.readlines()]

regs = [get_ints(line)[0] for line in lines[0:3]]

print(regs)

program = get_ints(lines[4])
ip = 0
output = []

while ip < len(program):
    print(regs)
    def combo(op):
        if op < 4:
            return op
        assert op != 7
        return regs[op-4]

    match program[ip]:
        case 0:
            regs[0] = regs[0] >> combo(program[ip+1])
            ip += 2
        case 1:
            regs[1] ^= program[ip+1]
            ip += 2
        case 2:
            regs[1] = combo(program[ip+1]) % 8
            ip += 2
        case 3:
            if regs[0] == 0:
                ip += 2
            else:
                ip = program[ip+1]
        case 4:
            regs[1] ^= regs[2]
            ip += 2
        case 5:
            output.append(combo(program[ip+1]) % 8)
            ip += 2
        case 6:
            regs[1] = regs[0] >> combo(program[ip+1])
            ip += 2
        case 7:
            regs[2] = regs[0] >> combo(program[ip+1])
            ip += 2

print(",".join(str(x) for x in output))
