import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from vm.vm import *

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
lines = [line.strip() for line in sys.stdin.readlines()]


order=[int(x) for x in lines[0]]
COUNT = len(order)

for move in range(100):
    p1 = order[1]
    p2 = order[2]
    p3 = order[3]
    dest = order[0] - 1
    if dest < 1:
        dest = 9
    while dest == p1 or dest == p2 or dest == p3:
        dest = dest - 1
        if dest < 1:
            dest = 9

    # print(order)
    # print('pick up: ', p1, p2, p3)
    # print('dest: ', dest)

    new_order = []
    i = 4
    while order[i] != dest:
        new_order.append(order[i])
        i += 1
    new_order.append(order[i])
    new_order.append(order[1])
    new_order.append(order[2])
    new_order.append(order[3])
    i += 1
    while i < COUNT:
        new_order.append(order[i])
        i += 1
    new_order.append(order[0])

    order = new_order

i = 0
while order[i] != 1:
    i += 1

s = ""
for j in range(COUNT):
    s += str(order[i])
    i = (i+1)%COUNT

print(s[1:])
