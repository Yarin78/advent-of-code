import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
# scanner = Scanner(sys.stdin)
lines = [line for line in sys.stdin.readlines()]
# Split input into an array of array of lines, split by empty line
# sections = split_lines(lines)

stacks = [[] for x in range(9)]

for i in range(8):
    for j in range(9):
        c = lines[7-i][j*4+1] if j*4+1<len(lines[7-i]) else ' '
        if c != ' ':
            stacks[j].append(c)

for line in lines[10:]:
    cnt, src, dest = get_ints(line)
    src -= 1
    dest -= 1
    # for x in range(cnt):
    #     c = stacks[src][-1]
    #     stacks[src].pop()
    #     stacks[dest].append(c)
    c = stacks[src][-cnt:]
    stacks[dest].extend(c)
    for i in range(cnt):
        stacks[src].pop()

    #for i in range(9):
    #    print(stacks[i])

s = ''
for i in range(9):
    s += stacks[i][-1]

print(s)