import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations, dropwhile
from yal import util
from yal.geo2d import *
from aocd import data, submit

# Clean up version, see day8.org.py for original

lines = data.strip().split('\n')
layers = util.chunk(lines[0], 25*6)

min_zeros = min([x.count('0') for x in layers])
max_onetwo = max([x.count('1')*x.count('2') for x in layers if x.count('0') == min_zeros])

print(max_onetwo)

for y in range(6):
    print(''.join(['.#'[ord(''.join([layers[i][y*25+x] for i in range(100)]).replace('2', '')[0])-48] for x in range(25)]))
