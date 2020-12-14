import sys
from yal.util import *

lines = [line.strip() for line in sys.stdin.readlines()]
mask = 0
and_mask = 0
or_mask = 0
mem1 = {}
mem2 = {}

def go(addr, value, mask, bit):
    if bit == 36:
        mem2[addr] = value
    elif mask[35-bit] == '0':
        go(addr, value, mask, bit+1)
    elif mask[35-bit] == '1':
        go(addr | (1<<bit), value, mask, bit+1)
    else:
        go(addr | (1<<bit), value, mask, bit+1)
        go((addr | (1<<bit))-(1<<bit), value, mask, bit+1)

for line in lines:
    if line.startswith("mask"):
        mask = line[7:]
        and_mask = 0
        or_mask = 0
        for i in range(36):
            if mask[35-i] != '0':
                and_mask |= (1<<i)
            if mask[35-i] == '1':
                or_mask |= (1<<i)
    else:
        (_, addr, value) = intify(tokenize(line))
        mem1[addr] = (value & and_mask) | or_mask
        go(addr, value, mask, 0)


print(sum(mem1.values()))
print(sum(mem2.values()))
