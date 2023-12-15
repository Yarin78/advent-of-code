import sys
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

lines = [line.strip() for line in sys.stdin.readlines()]

part1 = 0
part2 = 0
boxes = [{} for _ in range(256)]

def hash_it(s):
    hash = 0
    for c in s:
        hash = (hash + ord(c)) * 17 % 256
    return hash

for s in lines[0].split(","):
    part1 += hash_it(s)

    if '=' in s:
        lens = s[:s.index('=')]
        box = hash_it(lens)
        lens, val = s.split('=')
        boxes[box][lens] = int(val)
    else:
        lens = s[:-1]
        box = hash_it(lens)
        if lens in boxes[box]:
            del boxes[box][lens]

print(part1)

part2 = sum((1+i) * (j + 1) * val for i, box in enumerate(boxes) for j, val in enumerate(box.values()))

print(part2)