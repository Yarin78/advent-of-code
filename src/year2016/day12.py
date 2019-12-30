import sys
import re
import itertools
from collections import defaultdict
from lib.util import get_ints

input = sys.stdin
input = open('year2016/day12.in')
#input = open('year2016/day12.sample.in')

code = [line.strip().split(' ') for line in input.readlines()]
ip = 0
regs = [0] * 256
regs[ord('c')] = 1
while ip >= 0 and ip < len(code):
    #print(ip, regs[97:101])
    if code[ip][0] == 'cpy':
        if code[ip][1].isalpha():
            regs[ord(code[ip][2])] = regs[ord(code[ip][1])]
        else:
            regs[ord(code[ip][2])] = int(code[ip][1])
    elif code[ip][0] == 'inc':
        regs[ord(code[ip][1])] += 1
    elif code[ip][0] == 'dec':
        regs[ord(code[ip][1])] -= 1
    elif code[ip][0] == 'jnz':
        if not code[ip][1].isalpha():
            if int(code[ip][1]):
                ip += int(code[ip][2]) - 1
        elif regs[ord(code[ip][1])]:
            ip += int(code[ip][2]) - 1
    ip += 1

print(regs[97:101])
