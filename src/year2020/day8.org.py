import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from aocd import data, submit

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
lines = data.strip().split('\n')
#with open("day8-sample.in", "r") as f:
#    lines = f.readlines()

def reaches_end(pc, acc):
    seen = set()
    while pc not in seen and pc < len(lines):
        # print("pc = ", pc)
        seen.add(pc)
        tokens = lines[pc].split(' ')
        i = tokens[0]
        if i == "acc":
            acc += int(tokens[1])
            pc += 1
        elif i == "jmp":
            pc += int(tokens[1])
        elif i == "nop":
            pc += 1
        else:
            assert False
    if pc == len(lines):
        return True, acc
    return False, acc

reach_end = set()
for pc in range(len(lines)):
    done, acc = reaches_end(pc, 0)
    if done:
        reach_end.add(pc)


pc = 0
acc = 0
changed = 0
while pc != len(lines):
    #print("at ", pc)
    tokens = lines[pc].split(' ')
    i = tokens[0]
    if i == "nop":
        print("wtf", acc)
        pass
    elif i == "jmp":
        if pc+1 in reach_end and changed == 0:
            print(f"modified instr at {pc} to nop")
            changed+=1
            print("changed")
            i = "nop"

    if i == "acc":
        acc += int(tokens[1])
        pc += 1
    elif i == "jmp":
        pc += int(tokens[1])
    elif i == "nop":
        pc += 1
    else:
        assert False

print(changed, acc)
