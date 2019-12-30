import sys
from collections import defaultdict

START = (0,0)
ptr = 1
expr = sys.stdin.readline().strip()

map = defaultdict(set)

directions = {'E': (1,0), 'W': (-1,0), 'N': (0,-1), 'S': (0,1)}
inverse = {'E':'W', 'W':'E', 'N':'S', 'S':'N'}

def explore(coords):
    global ptr, expr, map
    end_coords = set()

    cur = set(coords)

    while True:
        c = expr[ptr]
        ptr += 1

        if c == ')' or c == '$':
            end_coords.update(cur)
            break
        elif c == '(':
            cur = explore(cur)
        elif c == '|':
            end_coords.update(cur)
            cur = set(coords)
        else:
            next = set()
            for (x,y) in cur:
                map[(x,y)].add(c)
                (dx,dy) = directions[c]
                nx = x+dx
                ny = y+dy
                map[(nx,ny)].add(inverse[c])
                next.add((nx,ny))
            cur = next

    return end_coords

explore(set([START]))

q = []
head = 0
q.append(START)
dist = {START: 0}
cnt=0
while head < len(q):
    cur = q[head]
    print 'At (%d,%d), distance %d' % (cur[0], cur[1], dist[cur])
    if dist[cur] >= 1000:
        cnt+=1
    head += 1
    for dir in map[cur]:
        dxy = directions[dir]
        next = (cur[0]+dxy[0], cur[1]+dxy[1])
        if next not in dist:
            dist[next] = dist[cur] + 1
            q.append(next)

print cnt
