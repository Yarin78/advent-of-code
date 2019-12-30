import sys
import re
import itertools
from collections import defaultdict
from lib import util

input = sys.stdin
input = open('year2016/day8.in')
#input = open('year2016/day8.sample.in')

screen = [['.'] * 50 for x in range(6)]

for line in input.readlines():
    [a,b] = util.get_ints(line)
    if line.startswith('rect'):
        for y in range(b):
            for x in range(a):
                screen[y][x] = '#'
    elif line.startswith('rotate row'):
        screen[a] = screen[a][-b:] + screen[a][:-b]
    elif line.startswith('rotate col'):
        col = []
        for y in range(6):
            col.append(screen[(y+6-b)%6][a])
        for y in range(6):
            screen[y][a] = col[y]

cnt = 0
for line in screen:
    print(''.join(line))
    cnt += sum([1 for c in line if c=='#'])

print(cnt)
