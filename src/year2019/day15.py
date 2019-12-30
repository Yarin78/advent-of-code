import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.grid import *
from intcode.intcode import *
from aocd import data, submit

lines = data.strip().split('\n')
prog = Program(data)

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
            status = prog.run_until_next_io(feed_input=[dir+1])

            if status:
                if status == 2:
                    goal = new_pos
                search(new_pos)
                status = prog.run_until_next_io(feed_input=[OPP_DIR[dir]+1])
                assert status
            else:
                map[new_pos] = '#'


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
