import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

# Make sure ~/.config/aocd/token is correct! (Application tab -> Cookies)
# scanner = Scanner(sys.stdin)
lines = [line.strip() for line in sys.stdin.readlines()]
# Split input into an array of array of lines, split by empty line
sections = split_lines(lines)

graph = {}

anodes = set()
znodes = set()

for line in sections[1]:
    tokens = tokenize(line)
    graph[tokens[0]] = [tokens[1], tokens[2]]

    for t in tokens:
        if t.endswith("A"):
            anodes.add(t)
        if t.endswith("Z"):
            znodes.add(t)

dirs = sections[0][0]
anode_steps = []

# Not working

anodes = ["AAA"]
znodes = ["ZZZ"]

for cur in anodes:
    steps = 0
    seen = set()
    while True:
        state = (cur, steps%len(dirs))
        if state in seen:
            break
        seen.add(state)
        nextcur=[]
        dir = 0 if steps % len(dirs) == 0 else 1
        cur = graph[cur][dir]
        steps += 1
    steps -= 2
    anode_steps.append(steps)

print(math.lcm(*anode_steps))
