import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from vm.vm import *
from aocd import data, submit

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
lines = data.strip().split('\n')
#with open("day8-sample.in", "r") as f:
#    lines = f.readlines()

prog = Program(lines)

while prog.instr_count[prog.ip] == 0:
    prog.step()

print(prog.acc)

for i in range(len(lines)):
    org = lines[i]
    if lines[i].startswith("nop"):
        lines[i] = lines[i].replace("nop", "jmp")
    elif lines[i].startswith("jmp"):
        lines[i] = lines[i].replace("jmp", "nop")

    prog = Program(lines)
    prog.run(steps=len(lines)+1)
    if prog.ip == len(lines):
        print(prog.acc)

    lines[i] = org
