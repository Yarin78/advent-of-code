import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
lines = [line.strip() for line in sys.stdin.readlines()]

n = len(lines[0])

def iterate(lines, part):
    x = 0
    while len(lines) > 1:
        print(part, x)
        cnt0 = 0
        cnt1 = 0
        for line in lines:
            if line[x] == '1':
                cnt1 += 1
            else:
                cnt0 += 1

        new_lines = []
        for line in lines:
            if part == 1:
                if (cnt1 >= cnt0 and line[x] == '1') or (cnt0 > cnt1 and line[x] == '0'):
                    new_lines.append(line)

            if part == 2:
                if (cnt1 < cnt0 and line[x] == '1') or (cnt0 <= cnt1 and line[x] == '0'):
                    new_lines.append(line)

        lines = new_lines
        x += 1

    return lines[0]


a = iterate(lines, 1)
b = iterate(lines, 2)
a = int(a,2)
b = int(b,2)
print(a,b)
print(a*b)
