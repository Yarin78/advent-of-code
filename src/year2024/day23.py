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
import networkx as nx

# Make sure ~/.config/aocd/token is correct! (Application tab -> Cookies)
# scanner = Scanner(sys.stdin)
lines = [line.strip() for line in sys.stdin.readlines()]
# Split input into an array of array of lines, split by empty line
# sections = split_lines(lines)

g = defaultdict(set)
all_comps = set()
G=nx.Graph()

for line in lines:
    a = line[0:2]
    b = line[3:5]
    g[a].add(b)
    g[b].add(a)
    all_comps.add(a)
    all_comps.add(b)
    G.add_edge(a, b)


cnt = 0
for ca, cb, cc in combinations(all_comps, 3):
    if ca[0] == 't' or cb[0] == 't' or cc[0] == 't':
        if cb in g[ca] and cc in g[ca] and cc in g[cb]:
            cnt += 1
print(cnt)

best = []
for c in nx.find_cliques(G):
    if len(c) > len(best):
        best = sorted(c)

print(','.join(best))
