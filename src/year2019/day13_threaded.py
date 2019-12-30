from queue import Queue
from lib.util import *
from lib.geo2d import *
from lib.intcode import *
from aocd import data


map = {}

lines = data.strip().split('\n')
prog = Program(data)
t = prog.start_async()
while t.is_alive():
    x = prog._output.get()
    y = prog._output.get()
    tile = prog._output.get()
    map[Point(x,y)] = tile
t.join()

print_array(gridify_sparse_map(map))

print("%d block tiles" % list(map.values()).count(2))

prog.reset()
prog.mem[0] = 2

t = prog.start_async()

# TODO: This doesn't work, need to know if someone is waiting reading from input

score = 0
ballx = 0
paddlex = 0
while t.is_alive():
    x = prog._output.get()
    #if prog.halted:
    #    break
    if x is None:
        prog._input.put(sign(ballx - paddlex))
        continue
    y = prog._output.get()
    tile = prog._output.get()
    if x < 0 and y == 0:
        score = tile
        print('score %d' % score)
    elif tile == 4:
        ballx = x
    elif tile == 3:
        paddlex = x
t.join()
print(score)
