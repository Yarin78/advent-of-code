import sys
from dataclasses import dataclass
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

# Make sure ~/.config/aocd/token is correct! (Application tab -> Cookies)
# scanner = Scanner(sys.stdin)
lines = [line.strip() for line in sys.stdin.readlines()]
# Split input into an array of array of lines, split by empty line
sections = split_lines(lines)

keys = []
locks = []
ysize = 5

for section in sections:
    xsize = len(section[0])
    if section[0] == '#' * xsize:
        key = []
        for x in range(xsize):
            y = 0
            while section[y][x] != '.':
                y += 1
            key.append(y-1)
        keys.append(key)
    else:
        assert section[-1] == '#' * xsize
        lock = []
        for x in range(xsize):
            y = len(section) - 1
            while section[y][x] != '.':
                y -= 1
            lock.append(len(section) - y - 2)
        locks.append(lock)

print(keys)
print(locks)

ans = 0
for k in keys:
    for l in locks:
        ok = True
        for c in range(len(k)):
            if k[c] + l[c] > ysize:
                ok = False
        if ok:
            ans += 1
print(ans)
