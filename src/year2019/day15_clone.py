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
prog = Program(data)
prog.init_io(Queue(), Queue())

map = {}
goal = None

DIRS = [NORTH, SOUTH, WEST, EAST]
OPP_DIR = [1,0,3,2]

def search(prog, pos):
    global map,goal
    map[pos] = '.'
    for dir in range(4):
        new_pos = pos+DIRS[dir]
        if new_pos not in map:
            cloned = prog.clone()

            status = cloned.run_until_next_io(feed_input=[dir+1])

            if status:
                if status == 2:
                    goal = new_pos
                search(cloned, new_pos)
            else:
                map[new_pos] = '#'


start = Point(0,0)
search(prog, start)
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
