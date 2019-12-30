import sys
import re
import itertools
from collections import defaultdict

input = sys.stdin
input = open('year2016/day6.in')

pos = [''] * 8
for line in input:
    line = line.strip()
    for i in range(len(line)):
        pos[i] += line[i]

pw = ''
for s in pos:
    d = defaultdict(int)
    for c in s:
        d[c] += 1
    m = min([(k,v) for k,v in d.items()], key=lambda x:x[1])
    print(m)
    pw += m[0]

print(pw)


