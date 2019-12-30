import sys
import re
import itertools
from collections import defaultdict
from lib.util import get_ints
from heapq import *

input = sys.stdin
input = open('year2016/day10.in')
#input = open('year2016/day10.sample.in')

#start = [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0] # elevator, five generators, five chips
start = [0,  0, 0, 0, 0, 0, 0, 0,   1, 0, 1, 0, 0, 0, 0] # elevator, five generators, five chips
#start = [0, 1, 2, 0, 0]

TYPES = (len(start) - 1) // 2

def encode(state):
    h = 0
    for i in state:
        h = h * 4 + i
    return h

def is_valid(state):
    global TYPES
    floor = [False] * TYPES
    for i in range(TYPES):
        floor[state[i+1]] = True
    for i in range(TYPES):
        if state[1+TYPES+i] != state[1+i] and floor[state[1+TYPES+i]]:
            return False
    return True

def normalize(state):
    pairs = []
    for i in range(TYPES):
        pairs.append((state[1+i], state[1+i+TYPES]))
    pairs.sort()
    new_state = [0] * len(state)
    new_state[0] = state[0]
    for i in range(TYPES):
        new_state[1+i] = pairs[i][0]
        new_state[1+i+TYPES] = pairs[i][1]
    return new_state


def estimate(state):
    #return sum([3-x for x in state[1:]]) // 2
    return 0

start = normalize(start)
q = []
visited = set()
heappush(q, (estimate(start), 0, start))
dups = 0
print('start estimate = ', estimate(start))

while True:
    (_, dist, current) = heappop(q)
    h = encode(current)
    if h in visited:
        dups += 1
        continue
    visited.add(h)
    #print('%2d: At %s' % (dist, current))
    if all([x == 3 for x in current]):
        print('Done in %d steps' % dist)
        print('%d states visited, %d duplicates' % (len(visited), dups))
        break

    floor = current[0]
    candidates = [i for i in range(len(current)) if current[i] == floor]

    for i in candidates:
        for j in candidates:
            if j <= i:
                continue
            for dir in [-1,1]:
                new_floor = floor+dir
                if new_floor >= 0 and new_floor < 4:
                    state = current[:]
                    state[0] = new_floor
                    if i > 0:
                        state[i] = new_floor
                    if j > 0:
                        state[j] = new_floor
                    state = normalize(state)
                    h = encode(state)
                    if h not in visited and is_valid(state):
                        heappush(q, (dist+1+estimate(state), dist+1, state))


