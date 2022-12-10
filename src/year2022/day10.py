import sys
from yal.util import *

lines = [line.strip() for line in sys.stdin.readlines()]

part1 = 0
cycle = 0
x = 1
pc = 0
v = []

display = ""

while pc < len(lines) or v:
    display += ".#"[cycle % 40 in (x-1, x, x+1)]
    cycle += 1
    part1 += cycle * x * ((cycle-20) % 40 == 0)

    if v:
        x += v[0]
        v = []
    else:
        v = get_ints(lines[pc])
        pc += 1

print(part1)
for i in range(6):
    print(display[40*i:40*i+40])
