import sys
from queue import Queue
from lib.geo2d import *

coord_to_index = {}
index_to_coord = []

y = 0
start = 0
for line in sys.stdin.readlines():
    for x in range(len(line)):
        if line[x] in '.o':
            if line[x] == 'o':
                start += 2**len(index_to_coord)
            coord_to_index[Point(x,y)] = len(index_to_coord)
            index_to_coord.append(Point(x,y))

    y += 1

def show(state):
    x = 0
    y = 0
    line = ''
    for i in range(len(index_to_coord)):
        c = 'o' if ((2**i) & state) else '.'
        p = index_to_coord[i]
        while p.y > y:
            print(line)
            line = ''
            y += 1
            x = 0
        while p.x > x:
            line += ' '
            x += 1
        line += c
        x += 1
    print(line)


moves = []  # tuple of (mask, eq)
for p in coord_to_index:
    for d in DIRECTIONS:
        if p+d in coord_to_index and p+d+d in coord_to_index:
            mask = 2**coord_to_index[p]+2**coord_to_index[p+d]+2**coord_to_index[p+d+d]
            eq = 2**coord_to_index[p]+2**coord_to_index[p+d]
            moves.append((mask, eq))
print('%d moves available' % len(moves))

def bit_cnt(x):
    return 1 + bit_cnt(x&(x-1)) if x else 0

q = Queue()
#seen = {}  # move -> (mask, eq) made to reach this position
seen = set()
q.put(start)
seen.add(start)
pegs_left = -1
num_states = 0

while not q.empty():
    num_states += 1
    if num_states % 100000 == 0:
        print('%d states visited' % num_states)

    cur = q.get()
    if bit_cnt(cur) != pegs_left:
        pegs_left = bit_cnt(cur)
        print('%d pegs left (%d states to visit)' % (pegs_left, len(seen)))
        seen = set()

    has_moves = False
    for (mask, eq) in moves:
        if (cur & mask) == eq:
            has_moves = True
            pos = cur - eq + (mask-eq)
            if pos not in seen:
                #seen[pos] = (mask, eq)
                seen.add(pos)
                q.put(pos)
    #if not has_moves:
        #show(cur)
        #break


