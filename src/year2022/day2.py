import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

lines = [line.strip() for line in sys.stdin.readlines()]

part1=0
part2=0

for line in lines:
    they = ord(line[0])-ord('A')
    you = ord(line[2])-ord('X')

    part1 += you+1 + (you-they+1)%3*3
    you = (you+they+2) % 3
    part2 += you+1 + (you-they+1)%3*3



print(part1, part2)
