import re
from queue import Queue

_integer_pattern = re.compile("-?[0-9]+")

def get_ints(line):
    return [int(m) for m in _integer_pattern.findall(line)]


def bfs(graph, start):
    '''Performs a BFS search in a graph and returns the distans to all nodes visited.'''
    dist = {}  # node -> distance
    q = Queue()
    q.put(start)
    dist[start] = 0
    while not q.empty():
        current = q.get()
        steps = dist[current]
        for neighbor in graph.get(current, []):
            if neighbor not in dist:
                dist[neighbor] = steps + 1
                q.put(neighbor)
    return dist
