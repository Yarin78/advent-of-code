import sys
from collections import defaultdict
from lib import util

scanners = []
for line in sys.stdin.readlines():
    [d, r] = util.get_ints(line)
    scanners.append((d, r))

scanners.sort(key=lambda x: x[1])

#print(scanners)

delay = 0
while True:
    cost = 0
    caught = False
    for (d, r) in scanners:
        cycle_len = r+r-2
        if (d + delay) % cycle_len == 0:
            cost += d*r
            caught = True
            if delay > 0:
                break
    if delay == 0:
        print(cost)
    if not caught:
        print(delay)
        break
    delay += 1
