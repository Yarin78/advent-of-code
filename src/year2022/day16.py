from collections import defaultdict
import sys
from functools import cache
from yal.util import *
from typing import List, Dict

MAX_NODES = 60

graph = [[] for _ in range(MAX_NODES)]
pressure_at_node: List[int] = [0] * MAX_NODES
pressure_nodes: List[int] = [-1] * MAX_NODES
node_to_index: Dict[str, int] = {}
dist: Dict[Tuple[int, int], int] = defaultdict(lambda: 99)
node_map: Dict[int, int] = {}

def lookup_node_index(node: str) -> int:
    global node_to_index
    if node in node_to_index:
        return node_to_index[node]
    node_to_index[node] = len(node_to_index)
    return node_to_index[node]

all_mask = 0
press_nodes = 0
relevant_nodes = []
for line in sys.stdin.readlines():
    pressure = get_ints(line)[0]
    parts = line.split(' ')
    src = lookup_node_index(parts[1])
    for target in parts[9:]:
        t = lookup_node_index(target[0:2])
        graph[src].append(t)
        dist[(t, src)] = 1

    pressure_at_node[src] = pressure
    if pressure > 0:
        pressure_nodes[src] = press_nodes
        all_mask += 1 << press_nodes
        node_map[press_nodes] = src
        press_nodes += 1
        relevant_nodes.append(src)


n = len(node_to_index)
assert len(node_to_index) <= MAX_NODES

# Floyd-warshall, slow but few lines to get distance between all nodes
for k in range(n):
    for i in range(n):
        for j in range(n):
            dist[(i,j)] = min(dist[(i,j)], dist[(i,k)] + dist[(k,j)])

@cache
def go(cur: int, time_left: int, left_mask: int):
    best = 0
    i = 0
    mask = 1
    while mask <= left_mask:
        if mask & left_mask:
            e = node_map[i]
            if time_left + 1 >= dist[(cur, e)]:
                next_time = time_left-dist[(cur, e)] - 1
                best = max(best, go(e, next_time, left_mask - mask) + next_time * pressure_at_node[e])
        i += 1
        mask *= 2

    return best


print("Part 1:", go(lookup_node_index("AA"), 30, all_mask))
print("Part 2:", max(go(lookup_node_index("AA"), 26, my_mask) + go(lookup_node_index("AA"), 26, all_mask - my_mask) for my_mask in range(all_mask+1)))
