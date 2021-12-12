import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
# scanner = Scanner(sys.stdin)
lines = [line.strip() for line in sys.stdin.readlines()]

def is_small_cave(s):
    return s == s.lower()

graph = defaultdict(lambda: list())
for line in lines:
    a,b = line.split('-')
    graph[a].append(b)
    graph[b].append(a)

def dfs(current, visited, dup):
    if current=="end":
        return 1
    if current=="start" and visited[current]==1:
        return 0

    cnt = 0
    if is_small_cave(current):
        if visited[current] == 2:
            return 0
        if visited[current] == 1 and dup:
            return 0
        visited[current] += 1
        for neighbor in graph[current]:
            cnt += dfs(neighbor, visited, dup or visited[current]==2)
        visited[current] -= 1
    else:
        for neighbor in graph[current]:
            cnt += dfs(neighbor, visited, dup)

    return cnt


visited = defaultdict(int)
tot = dfs("start", visited, False)
print(tot)

