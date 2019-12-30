import sys
import re
import itertools
from collections import defaultdict
from lib.util import get_ints

input = sys.stdin
input = open('year2016/day23.in')
#input = open('year2016/day23.sample.in')

code = [line.strip().split(' ') for line in input.readlines()]
ip = 0
regs = [0] * 256
regs[ord('a')] = 12
while ip >= 0 and ip < len(code):
    #print(ip, regs[97:101], code[ip])
    if code[ip][0] == 'nop':
        pass
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
    elif code[ip][0] == 'tgl':
        if not code[ip][1].isalpha():
            tgl_addr = ip + int(code[ip][1])
        else:
            tgl_addr = ip + regs[ord(code[ip][1])]
        print('Toggling addr %d' % tgl_addr)
        if tgl_addr >= 0 and tgl_addr < len(code):

            if len(code[tgl_addr]) == 2:
                if code[tgl_addr][0] == 'inc':
                    code[tgl_addr][0] = 'dec'
                else:
                    code[tgl_addr][0] = 'inc'
            else:
                if code[tgl_addr][0] == 'jnz':
                    code[tgl_addr][0] = 'cpy'
                else:
                    code[tgl_addr][0] = 'jnz'

    ip += 1

print(regs[97:101])
