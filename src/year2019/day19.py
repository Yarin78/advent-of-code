import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from intcode.intcode import *
from aocd import data, submit

lines = data.strip().split('\n')
prog = Program(data)
prog.init_io(Queue(), Queue())

def probe(x,y):
    global prog
    c = prog.run_until_next_io(feed_input=[x, y])
    prog.reset()
    return c

cnt = 0
for y in range(50):
    s = ''
    for x in range(50):
        if probe(x,y):
            s += '#'
            cnt += 1
        else:
            s += '.'
    print(s)

print(cnt)

y = 49
left = 33
right = 40
assert probe(left, y) and not probe(left-1,y)
assert probe(right, y) and not probe(right+1,y)

ranges = {}
while True:
    ranges[y] = (left, right)

    if y > 150:
        for x in range(left+99, right+1):
            (prev_left, prev_right) = ranges[y-99]
            if x-99 >= prev_left and x <= prev_right:
                x -= 99
                y -= 99
                print(x*10000+y)
                exit(0)

    y += 1
    while not probe(left, y):
        left += 1
    while probe(right+1,y):
        right += 1
