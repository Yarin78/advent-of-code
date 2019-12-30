import sys
import re

p = re.compile('(.)=([0-9]*), (.)=([0-9]*)\.\.([0-9]*)')

MAX = 2000
MIN_X = MAX
MAX_X = 0
MIN_Y = MAX
MAX_Y = 0

map = []
for i in range(MAX):
    map.append(['.'] * MAX)

def set_wall(x, y):
    global map, MIN_X, MAX_X, MIN_Y, MAX_Y
    MIN_X = min(MIN_X, x)
    MAX_X = max(MAX_X, x)
    MIN_Y = min(MIN_Y, y)
    MAX_Y = max(MAX_Y, y)
    map[y][x] = '#'


for line in sys.stdin.readlines():
    m = p.match(line.strip())
    if not m:
        print 'Oops: %s' % line.strip()
        exit(1)

    g = m.groups()
    g1 = int(g[1])
    g3 = int(g[3])
    g4 = int(g[4])
    if g[0] == 'x':
        for y in range(g3, g4+1):
            set_wall(g1, y)
    else:
        for x in range(g3, g4+1):
            set_wall(x, g1)

def show_map():
    global map
    for y in range(MIN_Y, MAX_Y+1):
        for x in range(MIN_X-1, MAX_X+2):
            sys.stdout.write(map[y][x])
        print
    print


#show_map()

def fill(x, y):
    global map, MAX_Y
    #show_map()
    if y > MAX_Y:
        return False
    if map[y][x] == '|':
        return False
    if map[y][x] != '.':
        return True

    forever = False
    q = [x]
    ptr = 0
    while ptr < len(q):
        cx = q[ptr]
        ptr += 1

        map[y][cx] = '|'
        if fill(cx, y+1):
            if map[y][cx+1] == '.':
                q.append(cx+1)
            if map[y][cx-1] == '.':
                q.append(cx-1)
        else:
            forever = True

    if not forever:
        for cx in q:
            map[y][cx] = '~'

    return not forever



sys.setrecursionlimit(MAX+10)

fill(500, 0)

show_map()

cnt = 0
for y in range(MIN_Y, MAX_Y+1):
    for x in range(0, MAX):
        #if map[y][x] == '|' or map[y][x] == '~':
        if map[y][x] == '~':
            cnt += 1

print cnt
