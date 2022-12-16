import sys
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

MAX_NODES = 60

graph = [[] for _ in range(MAX_NODES)]
pressure_at_node: List[int] = [0] * MAX_NODES
pressure_nodes: List[int] = [-1] * MAX_NODES
node_to_index: Dict[str, int] = {}

def lookup_node_index(node: str) -> int:
    global node_to_index
    if node in node_to_index:
        return node_to_index[node]
    node_to_index[node] = len(node_to_index)
    return node_to_index[node]

all_mask = 0
press_nodes = 0
for line in sys.stdin.readlines():
    pressure = get_ints(line)[0]
    parts = line.split(' ')
    src = lookup_node_index(parts[1])
    for target in parts[9:]:
        graph[src].append(lookup_node_index(target[0:2]))
    pressure_at_node[src] = pressure
    if pressure > 0:
        pressure_nodes[src] = press_nodes
        all_mask += 1 << press_nodes
        press_nodes += 1

n = len(node_to_index)
assert len(node_to_index) <= MAX_NODES

# Using custom cache is twice as fast, but still slow
# memo = [-1] * (all_mask+1) * MAX_NODES * 31

@functools.cache
def go(cur: int, time_left: int, release_mask: int):
    if release_mask == all_mask or time_left == 0:
        return 0
    #key = release_mask * MAX_NODES * 31 + time_left * MAX_NODES + cur
    #if memo[key] >= 0:
    #    return memo[key]

    best = 0
    if pressure_nodes[cur] >= 0 and ((1<<pressure_nodes[cur]) & release_mask) == 0:
        best = pressure_at_node[cur] * (time_left-1) + go(cur, time_left-1, release_mask + (1<<pressure_nodes[cur]))
    for e in graph[cur]:
        best = max(best, go(e, time_left-1, release_mask))
    #memo[key] = best

    return best


print("Part 1:", go(lookup_node_index("AA"), 30, 0))
print("Part 2:", max(go(lookup_node_index("AA"), 26, my_mask) + go(lookup_node_index("AA"), 26, all_mask - my_mask) for my_mask in range(all_mask+1)))
