import sys
import heapq

tx = 12
ty = 763
depth = 7740
mod = 20183

#tx = 10
#ty = 10
#depth = 510

MAX_X = tx*2
MAX_Y = ty*2

erosion = []
types = []
for y in range(0,MAX_Y):
    erosion.append([])
    s = ''
    for x in range(0,MAX_X):
        if (x==0 and y==0) or (x == tx and y == ty):
            g = 0
        elif y == 0:
            g = x * 16807
        elif x == 0:
            g = y * 48271
        else:
            g = erosion[y-1][x] * erosion[y][x-1]
        erosion[y].append((g + depth) % mod)
        if erosion[y][x] % 3 == 0:
            s += '.'
        elif erosion[y][x] % 3 == 1:
            s += '='
        else:
            s += '|'
    types.append(s)

risk = 0
for y in range(0,ty+1):
    line = types[y]
    for x in range(0,tx+1):
        if line[x] == '=':
            risk += 1
        elif line[x] == '|':
            risk += 2

INF = 999999
dist = []
for y in range(MAX_Y):
    dist.append([])
    for x in range(MAX_X):
        dist[y].append([INF] * 3)

# 0 = torch
# 1 = climbing
# 2 = neither
MAX_ANS = MAX_X*MAX_Y*10

dy = [1,0,-1,0]
dx = [0,1,0,-1]
q = [(0,0,0)]
distq = []
distq.append((0,0,0,0))

def allowed(x,y):
    global types
    if types[y][x] == '.':
        return [0,1]
    if types[y][x] == '=':
        return [1,2]
    return [0,2]

while len(distq) > 0:
    (cdist, x, y, tool) = heapq.heappop(distq)

    if cdist > dist[y][x][tool]:
        continue

    #print 'At %d,%d, tool=%d, dist=%d' % (x,y,tool, cdist)
    if x == tx and y == ty and tool == 0:
        print 'DONE after %d minutes!' % cdist
        exit(0)

    for d in range(0,4):
        nx = x+dx[d]
        ny = y+dy[d]

        if nx >= 0 and ny >= 0 and nx < MAX_X and ny < MAX_Y and tool in allowed(nx,ny):
            if cdist + 1 < dist[ny][nx][tool]:
                dist[ny][nx][tool] = cdist + 1
                heapq.heappush(distq, (cdist+1, nx, ny, tool))

    for nt in range(0,3):
        if nt in allowed(x,y) and cdist + 7 < dist[y][x][nt]:
            dist[y][x][nt] = cdist + 7
            heapq.heappush(distq, (cdist+7, x, y, nt))

print 'No solution!?'
