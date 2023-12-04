import sys
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
# sections = split_lines(lines)

# data = [int(x) for x in lines]
ans = 0

dignames = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

for line in lines:
    digits = []

    last = -1
    first = 100000
    firstdig = 0
    lastdig= 0


    for dig, s in enumerate(dignames):
        if s:
            a = line.find(s)
            b = line.rfind(s)

            if a >= 0 and a < first:
                first = a
                firstdig = dig
            if b >= 0 and b > last:
                last = b
                lastdig = dig

    for pos, c in enumerate(line):
        if c.isdigit() and pos < first:
            first = pos
            firstdig=int(c)
        if c.isdigit() and pos > last:
            last = pos
            lastdig=int(c)

    x = firstdig*10+lastdig
    ans += x

print(ans)
