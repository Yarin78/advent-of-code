import sys

nodes = {}

is_child = set()
for line in sys.stdin.readlines():
    line = line.replace(',', '').replace('(', '').replace(')', '').replace('-> ', '').strip()
    parts = line.split(' ')
    nodes[parts[0]] = (int(parts[1]), parts[2:])
    for x in nodes[parts[0]][1]:
        is_child.add(x)

for x in nodes.keys():
    if x not in is_child:
        root = x

def weight(name):
    s = nodes[name][0]
    w = -1
    childw = []
    e = []
    for child in nodes[name][1]:
        childw.append(weight(child))
        e.append(nodes[child][0])

    if len(childw) > 1:
        if sum(childw) != childw[0] * len(childw):
            print(name, childw)
            print(e)

    return s + sum(childw)


print('root = ', root)
weight(root)
