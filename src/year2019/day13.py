from queue import Queue
from yal.math import *
from yal.grid import *
from yal.geo2d import *
from intcode.intcode import *
from aocd import data


map = {}

lines = data.strip().split('\n')
prog = Program(data)

while True:
    x = prog.run_until_next_io()
    if x is None:
        break
    y = prog.run_until_next_io()
    tile = prog.run_until_next_io()
    map[Point(x,y)] = tile


print_array(gridify_sparse_map(map))

print("%d block tiles" % list(map.values()).count(2))

prog.reset()
prog.mem[0] = 2

score = 0
ballx = 0
paddlex = 0
while not prog.halted:
    x = prog.run_until_next_io()
    if prog.halted:
        break
    if x is None:
        prog.feed_input(sign(ballx - paddlex))
        continue
    y = prog.run_until_next_io()
    tile = prog.run_until_next_io()
    if x < 0 and y == 0:
        score = tile
    elif tile == 4:
        ballx = x
    elif tile == 3:
        paddlex = x

print(score)
