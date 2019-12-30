import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from intcode.intcode import *
from aocd import data, submit

lines = data.split('\n')
#with open("day20.input.txt") as f:
#    lines = f.readlines()

ysize = len(lines)-4
xsize = len(lines[2])-2
print(xsize, ysize)

g = {}
portals = {}
for y in range(ysize):
    for x in range(xsize):
        p = Point(x,y)
        if lines[y+2][x+2] != '.':
            continue
        neighbors = []
        for d in DIRECTIONS:
            np = p+d
            if np.x+2 < len(lines[np.y+2]):
                c = lines[np.y+2][np.x+2]
                if c >= 'A' and c <= 'Z':
                    nnp = np + d
                    cc = lines[nnp.y+2][nnp.x+2]
                    if d.x < 0 or d.y < 0:
                        tmp = c
                        c = cc
                        cc = tmp
                    qp = nnp+d
                    # Rough check, got a lot of off-by-on errors here
                    if qp.x < 0 or qp.y < 0 or qp.x >= xsize or qp.y >= ysize:
                        inner = 0
                    else:
                        inner = 1
                    lbl = '%c%c' % (c, cc)
                    #print(p, lbl, inner)
                    if lbl == 'AA':
                        start = p
                    elif lbl == 'ZZ':
                        goal = p
                    else:
                        if lbl not in portals:
                            portals[lbl] = [None, None]
                        assert portals[lbl][0 if inner else 1] is None
                        portals[lbl][0 if inner else 1] = p

            if np.x >= 0 and np.y >= 0 and np.x < xsize and np.y<ysize:
                if lines[np.y+2][np.x+2] == '.':
                    neighbors.append(np)


        g[p] = neighbors

lvl_diff = {}
for lbl, ps in portals.items():
    lvl_diff[(ps[0], ps[1])] = 1
    lvl_diff[(ps[1], ps[0])] = -1
    #print(lbl, ps)
    g[ps[0]].append(ps[1])
    g[ps[1]].append(ps[0])


dist = bfs(g, start)
print(dist[goal])

dist = {}  # node -> distance
dist_rev = {}
q = Queue()
q.put((start, 0))
q.put((goal, 0))
dist[(start, 0)] = 0
dist_rev[(goal, 0)] = 0
while not q.empty():
    (current, cur_lvl) = q.get()
    forward_steps = dist.get((current, cur_lvl))
    backward_steps = dist_rev.get((current, cur_lvl))
    if forward_steps is not None and backward_steps is not None:
        print(forward_steps + backward_steps)
        break
    for neighbor in g.get(current, []):
        next_lvl = cur_lvl
        if (current, neighbor) in lvl_diff:
            next_lvl = cur_lvl + lvl_diff[(current, neighbor)]
        if next_lvl >= 0:
            np = (neighbor, next_lvl)

            if forward_steps is not None:
                if np not in dist:
                    dist[np] = forward_steps + 1
                    q.put(np)
            else:
                if np not in dist_rev:
                    dist_rev[np] = backward_steps + 1
                    q.put(np)

print('# visited states', len(dist))
