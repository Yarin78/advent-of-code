import sys
from collections import defaultdict
from lib import util
from queue import Queue

def knot_hash(key):
    parts=[]
    for c in key:
        parts.append(ord(c))
    parts.extend([17,31,73,47,23])

    c = list(range(256))
    pos = 0
    skip_size = 0
    n = len(c)
    for r in range(64):
        for x in parts:
            nc = c[:]
            for i in range(x):
                nc[(pos+i)%n] = c[(pos+x-i-1)%n]
            pos += x + skip_size
            skip_size += 1
            c = nc

    res = []
    for b in range(16):
        x = 0
        for i in range(16):
            x ^= c[b*16+i]
        res.append(x)
    return res

#key = 'flqrgnkx'
key = 'xlqgujun'
dirs = [(1,0),(-1,0),(0,1),(0,-1)]
cnt = 0
grid = []
for row in range(128):
    res = knot_hash('%s-%d' % (key, row))
    s = ''
    for i in range(16):
        s += '{0:b}'.format(res[i]).zfill(8)
    grid.append(s)
    cnt += s.count('1')
print ('Used', cnt)

seen = set()
groups = 0
for y in range(128):
    for x in range(128):
        if grid[y][x] == '1' and (x,y) not in seen:
            groups += 1
            q = Queue()
            q.put((x,y))
            seen.add((x,y))
            while not q.empty():
                (cx,cy) = q.get()
                for (dx, dy) in dirs:
                    nx, ny = cx+dx, cy+dy
                    if ny >= 0 and nx >= 0 and ny < 128 and nx < 128 and grid[ny][nx] == '1' and (nx,ny) not in seen:
                        q.put((nx,ny))
                        seen.add((nx,ny))

print(groups)

