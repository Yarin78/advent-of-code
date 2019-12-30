import sys

points = []
for line in sys.stdin.readlines():
    [x,y] = map(lambda x:int(x), line.split(','))
    points.append((x,y))

minx = min(points, key=lambda p:p[0])[0]
maxx = max(points, key=lambda p:p[0])[0]
miny = min(points, key=lambda p:p[1])[1]
maxy = max(points, key=lambda p:p[1])[1]

area = [0] * len(points)
infinite = set()
reg = 0
BOUNDS = 7

for y in range(miny-BOUNDS, maxy+BOUNDS):
    for x in range(minx-BOUNDS, maxx+BOUNDS):
        closest = 10000
        dist_sum = 0
        for p in range(len(points)):
            dist = abs(points[p][0]-x)+abs(points[p][1]-y)
            if dist < closest:
                closest = dist
                cp = p
                multiple = False
            elif dist == closest:
                multiple = True

            dist_sum += dist
        if not multiple:
            area[cp] += 1
        if y == miny-BOUNDS or y == maxy+BOUNDS-1 or x == minx-BOUNDS or x == maxx+BOUNDS-1:
            infinite.add(cp)
        if dist_sum <= 10000:
            reg += 1


all_finite = []
for i in range(len(area)):
    if i not in infinite:
        all_finite.append(area[i])

all_finite.sort()
print all_finite

print 'Region size = %d' % reg
