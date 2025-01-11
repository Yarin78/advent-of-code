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
import re

# Make sure ~/.config/aocd/token is correct! (Application tab -> Cookies)
# scanner = Scanner(sys.stdin)
lines = [line.strip() for line in sys.stdin.readlines()]
# Split input into an array of array of lines, split by empty line
# sections = split_lines(lines)

# data = [int(x) for x in lines]

p = re.compile(r"mul\(([0-9]+),([0-9]+)\)|do\(\)|don't\(\)")

def sum_line(line):
    ans = 0
    cur = 0
    m = p.search(line, cur)
    exclude = False
    while m:
        print(m.group())
        if m.group() == "don't()":
            exclude = True
        elif m.group() == "do()":
            exclude = False
        else:
            a = int(m.groups()[0])
            b = int(m.groups()[1])
            if not exclude:
                ans += a*b

        cur = m.end()
        m = p.search(line, cur)

    return ans

# Not 30324235

ans = 0

s = ""
for line in lines:
    s += line

ans += sum_line(s)
print(ans)

# Not 111972528