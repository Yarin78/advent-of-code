import sys
from dataclasses import dataclass
from queue import Queue
from collections import defaultdict
from itertools import permutations, combinations
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

# data = [int(x) for x in lines]
ans = ans2 = 0

rules = defaultdict(list)
for rule in sections[0]:
    a, b = get_ints(rule)
    rules[a].append(b)

for update in sections[1]:
    ok = True
    v = get_ints(update)
    for i, j in combinations(v, 2):
        if i in rules[j]:
            ok = False
    if ok:
        ans += v[len(v) // 2]
    else:
        graph = {}
        for a in v:
            graph[a] = list(filter(lambda x: x in v, rules[a]))
        order = topological_sort(graph)
        ans2 += order[len(order) // 2]

print(ans)
print(ans2)
