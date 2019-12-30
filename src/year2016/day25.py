import sys
import re
import itertools
from collections import defaultdict
from lib.util import get_ints

input = sys.stdin
input = open('year2016/day25.in')

def simulate(code, a):
    ip = 0
    regs = [0] * 256
    regs[ord('a')] = a
    output = []
    while ip >= 0 and ip < len(code) and len(output) < 100:
        #print(ip, regs[97:101], code[ip])
        if code[ip][0] == 'nop':
            pass
        elif code[ip][0] == 'out':
            if code[ip][1].isalpha():
                value = regs[ord(code[ip][1])]
            else:
                value = int(code[ip][1])
            if value != len(output):
                print('Sending wrong value at pos ', len(output))
                return False
            output.append(value)
        elif code[ip][0] == 'add':
            if code[ip][2].isalpha():
                if code[ip][1].isalpha():
                    regs[ord(code[ip][2])] += regs[ord(code[ip][1])]
                else:
                    regs[ord(code[ip][2])] += int(code[ip][1])
        elif code[ip][0] == 'mul':
            if code[ip][2].isalpha():
                if code[ip][1].isalpha():
                    regs[ord(code[ip][2])] *= regs[ord(code[ip][1])]
                else:
                    regs[ord(code[ip][2])] *= int(code[ip][1])
        elif code[ip][0] == 'cpy':
            if code[ip][2].isalpha():
                if code[ip][1].isalpha():
                    regs[ord(code[ip][2])] = regs[ord(code[ip][1])]
                else:
                    regs[ord(code[ip][2])] = int(code[ip][1])
        elif code[ip][0] == 'inc':
            if code[ip][1].isalpha():
                regs[ord(code[ip][1])] += 1
        elif code[ip][0] == 'dec':
            if code[ip][1].isalpha():
                regs[ord(code[ip][1])] -= 1
        elif code[ip][0] == 'jnz':
            if not code[ip][2].isalpha():
                jmp_addr = ip + int(code[ip][2])
            else:
                jmp_addr = ip + regs[ord(code[ip][2])]

            if not code[ip][1].isalpha():
                if int(code[ip][1]):
                    ip = jmp_addr - 1
            elif regs[ord(code[ip][1])]:
                ip = jmp_addr - 1

        ip += 1

    if len(output) == 100:
        return True
    print('Program terminated!', regs[97:101])
    return False

code = [line.strip().split(' ') for line in input.readlines()]
a = 0
while True:
    print('a = ', a)
    if simulate(code, 0):
        break
    a += 1

print('Worked!')
