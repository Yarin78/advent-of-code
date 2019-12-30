import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from lib import util
from lib.geo2d import *
from lib.intcode import *
from aocd import data, submit

lines = data.strip().split('\n')
line = lines[0]
layers = []
cur = 0
while cur < len(line):
    layers.append(line[cur:cur+25*6])
    cur += 25*6

most = 0
least = 999999
for layer in layers:
    zeros = layer.count('0')
    onestwos = layer.count('1')*layer.count('2')
    if zeros < least:
        least = zeros
        m = onestwos
    elif zeros == least:
        m = max(m, onestwos)


s = ''
for y in range(6):
    row = ''
    for x in range(25):
        i = 0
        while layers[i][y*25+x] == '2':
            i += 1
        if layers[i][y*25+x] == '0':
            row += '.'
        else:
            row += '#'
    print(row)
