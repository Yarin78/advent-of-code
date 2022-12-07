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
lines = [line.strip() for line in sys.stdin.readlines()]
# Split input into an array of array of lines, split by empty line
# sections = split_lines(lines)

part1 = 0
for line in lines:
    n=len(line)
    rem = set(line[0:n//2]).intersection(line[n//2:])
    assert len(rem) == 1
    part1 += letter_value(list(rem)[0])+1

print(part1)

part2 = 0
for chunks in chunk(lines, 3):
    rem = set(chunks[0]).intersection(chunks[1]).intersection(chunks[2])
    assert len(rem) == 1
    part2 += letter_value(list(rem)[0])+1

print(part2)
