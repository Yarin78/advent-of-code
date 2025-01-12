from functools import cache
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
# sections = split_lines(lines)

@cache
def count(value, left):
    if left == 0:
        return 1
    if value == 0:
        return count(1, left-1)
    if len(str(value)) % 2 == 0:
        s = str(value)
        return count(int(s[:len(s)//2]), left-1) + count(int(s[len(s)//2:]), left-1)
    return count(value*2024, left-1)

stones = get_ints(lines[0])

print(sum(count(s, 25) for s in stones))
print(sum(count(s, 75) for s in stones))

