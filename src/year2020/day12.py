import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from vm.vm import *

DIRS={'E': Point(1,0), 'W': Point(-1,0), 'N': Point(0,1), 'S': Point(0,-1)}

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
lines = [line.strip() for line in sys.stdin.readlines()]

def part1(lines):
    cur = Point(0,0)
    dir = Point(1, 0)
    for line in lines:
        steps=int(line[1:])
        d = line[0]
        if d == 'F':
            cur += dir*steps
        elif d in 'LR':
            c = steps//90
            if d == 'R':
                c = 4-c
            while c > 0:
                dir = Point(-dir.y, dir.x)
                c -= 1
        else:
            cur += DIRS[d] * steps

    return cur


def part2(lines):
    cur = Point(0,0)
    wp = Point(10, 1)
    for line in lines:
        steps=int(line[1:])
        d = line[0]
        if d == 'F':
            cur += wp*steps
        elif d in 'LR':
            c = steps//90
            if d == 'R':
                c = 4-c
            while c > 0:
                wp = Point(-wp.y, wp.x)
                c -= 1
        else:
            wp += DIRS[d] * steps

    return cur


cur = part1(lines)
print(cur, abs(cur.x)+abs(cur.y))
cur = part2(lines)
print(cur, abs(cur.x)+abs(cur.y))
