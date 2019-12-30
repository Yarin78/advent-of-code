import sys
from queue import Queue
from collections import defaultdict
from lib import util

graph = {}

for line in sys.stdin.readlines():
    ints = util.get_ints(line)
    graph[ints[0]] = ints[1:]

seen = set()
groups = 0
for y in range(len(graph)):
    if y not in seen:
        groups += 1
        q = Queue()
        q.put(y)
        seen.add(y)
        while not q.empty():
            cur = q.get()
            for x in graph[cur]:
                if x not in seen:
                    q.put(x)
                    seen.add(x)

        if groups == 1:
            print(len(seen))

print(groups)
