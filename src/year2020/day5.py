import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from aocd import data, submit

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
seats = sorted([int(line.replace("B", "1").replace("R", "1").replace("L", "0").replace("F", "0"), 2) for line in open("day5.in", "r").readlines()])
print(seats[-1], [i for i in range(seats[0],seats[-1]) if i not in seats][0])
