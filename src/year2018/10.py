import sys

stars = []

for line in sys.stdin.readlines():
    # position=<-10351, -10360> velocity=< 1,  1>
    sx = int(line[10:16])
    sy = int(line[18:24])
    dx = int(line[36:38])
    dy = int(line[40:42])
    stars.append((sx,sy,dx,dy))


def min_diff(stars, time):
    minx = 99999999
    miny = 99999999
    maxx = -minx
    maxy = -miny
    for (sx,sy,dx,dy) in stars:
        x = sx+dx*time
        y = sy+dy*time
        minx=min(minx,x)
        maxx=max(maxx,x)
        miny=min(miny,y)
        maxy=max(maxy,y)

    return min(maxx-minx, maxy-miny)

def show(stars, time):
    minx = 99999999
    miny = 99999999
    maxx = -minx
    maxy = -miny
    for (sx,sy,dx,dy) in stars:
        x = sx+dx*time
        y = sy+dy*time
        minx=min(minx,x)
        maxx=max(maxx,x)
        miny=min(miny,y)
        maxy=max(maxy,y)

    res = []
    for y in range(miny, maxy+1):
        res.append(['.'] * (maxx-minx+1))

    for (sx,sy,dx,dy) in stars:
        x = sx+dx*time
        y = sy+dy*time
        res[y-miny][x-minx] = '#'

    for line in res:
        print ''.join(line)

best = 999999
for t in xrange(0, 1): #20000):
    m = min_diff(stars,t)
    if m < best:
        best = m
        bt = t
    #print '%d %d' % (t, m)

#print bt
show(stars, 10476)

