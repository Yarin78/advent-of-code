import sys
from yal.io import *
from yal.graph import *

monkeys = {}
graph = {}

for line in sys.stdin.readlines():
    line = line.replace(":", "=")
    name = line[0:4]
    monkeys[name] = line
    graph[name] = [line[6:10], line[13:17]] if len(line) == 18 else []

order = topological_sort(graph)

exec("".join(monkeys[name] for name in order))
print("Part 1:", root)

monkeys["root"] = monkeys["root"][:11] + " - " + monkeys["root"][12:]

lo=-9999999999999999999
hi=-lo
while lo < hi:
    x = (lo+hi) // 2
    monkeys["humn"] = f"humn = {x}\n"
    exec("".join(monkeys[name] for name in order))
    if root == 0:
        print("Part 2:", x)
    # Swap direction in sample input
    if root >= 0:
        lo = x + 1
    else:
        hi = x
