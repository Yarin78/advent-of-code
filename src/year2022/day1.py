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
segments = split_lines(lines)

calories = [sum(map(int, seg)) for seg in segments]
print(max(calories))

calories.sort(reverse=True)
print(sum(calories[0:3]))

