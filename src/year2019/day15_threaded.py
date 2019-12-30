import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from lib.util import *
from lib.graph import *
from lib.geo2d import *
from lib.intcode import *
from aocd import data, submit

lines = data.strip().split('\n')

map = {}
goal = None

DIRS = [NORTH, SOUTH, WEST, EAST]
OPP_DIR = [1,0,3,2]

def search(pos):
    global map,goal,prog
    map[pos] = '.'
    for dir in range(4):
        new_pos = pos+DIRS[dir]
        if new_pos not in map:
            prog._input.put(dir+1)
            status = prog._output.get()

            if status:
                if status == 2:
                    goal = new_pos
                search(new_pos)
                prog._input.put(OPP_DIR[dir]+1)
                status = prog._output.get()
                assert status
            else:
                map[new_pos] = '#'


prog = Program(data)
prog.init_io(Queue(), Queue())
t = prog.start_async(daemon=True)
start = Point(0,0)
search(start)
map[start] = 'S'
map[goal] = 'G'

print_array(gridify_sparse_map(map))

def node_conv(p, c):
    global goal, start
    if c == 'G':
        goal = p
    if c == 'S':
        start = p
    return c in '.GS'

g = grid_graph(gridify_sparse_map(map), is_node=node_conv)

dist = bfs(g, start)

print(dist[goal])

dist = bfs(g, goal)

print(max(dist.values()))
