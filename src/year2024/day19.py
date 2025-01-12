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

patterns = [x.strip() for x in lines[0].split(',')]

@cache
def is_poss(s):
    if s == "":
        return 1
    sum = 0
    for p in patterns:
        if s.startswith(p):
            sum += is_poss(s[len(p):])
    return sum

ans = 0
for line in lines[2:]:
    ans += is_poss(line)
print(ans)