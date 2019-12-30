import sys
from collections import defaultdict
from yal import util, geo2d, grid
from yal.geo2d import Point
from queue import Queue
from aocd import data, submit

# Cleaned up version, see day3.org.py for original version

lines = data.strip().split('\n')
#prog = intcode.Program(data)

m = {}
steps = [{}, {}]
closest = None
best = 999999999

for line_no in range(2):
    line = lines[line_no]
    parts = line.split(',')
    cur = Point(0,0)
    t = 0
    for j in range(len(parts)):
        s = parts[j]

        delta = grid.DIRECTION_MAP[s[0]]
        part_len = int(s[1:])
        for i in range(part_len):
            cur += delta
            t += 1
            if cur not in steps[line_no]:
                steps[line_no][cur] = t

            if j < len(parts)-1 or i < part_len -1:
                if line_no == 1 and cur in m and m[cur] == 1:
                    dist = abs(cur.x)+abs(cur.y)
                    if closest is None or dist < closest:
                        closest = dist
                    best = min(best, steps[0][cur] + steps[1][cur])

            m[cur] = line_no+1

print(closest)
print(best)

#submit(best, part="b", day=3, year=2019)
