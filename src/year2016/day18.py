import sys
import re
import itertools
import hashlib
from collections import defaultdict
from lib.util import get_ints
from heapq import *
from lib.geo2d import *

NO_ROWS = 400000
#NO_ROWS = 10

input = '.^^^^^.^^.^^^.^...^..^^.^.^..^^^^^^^^^^..^...^^.^..^^^^..^^^^...^.^.^^^^^^^^....^..^^^^^^.^^^.^^^.^^'
#input = '.^^.^.^^^^'

last = input
cnt = len(input.replace('^', ''))

for row in range(1,NO_ROWS):
    s = ''
    for i in range(len(last)):
        left = (last[i-1] if i > 0 else '.') == '^'
        center = last[i] == '^'
        right = (last[i+1] if i + 1 < len(last) else '.') == '^'
        trap = False
        if left and center and not right:
            trap = True
        elif center and right and not left:
            trap = True
        elif left and not center and not right:
            trap = True
        elif right and not center and not left:
            trap = True
        s += '^' if trap else '.'
        if not trap:
            cnt += 1
    last = s

print(cnt)
