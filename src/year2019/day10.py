import math
from aocd import data, submit


def flatten(l):
    return [item for sublist in l for item in sublist]

def normsqr(x, y):
    return x*x+y*y

lines = data.strip().split('\n')

asteroids = flatten([[(x,y) for x in range(len(lines[y])) if lines[y][x] == '#'] for y in range(len(lines))])

def unique_angles(asteroids, x,y):
    angles = {}  # angle -> closest
    for (tx,ty) in sorted(asteroids, key=lambda a: normsqr(a[0]-x,a[1]-y)):
        if tx!=x or ty!=y:
            angle = math.atan2(ty-y, tx-x)
            if ty-y < 0 and tx-x < 0:
                angle += 2*math.pi
            if angle not in angles:
                angles[angle] = (tx,ty)

    return sorted(angles.items())

best = max([len(unique_angles(asteroids, x,y)) for (x,y) in asteroids])

(sx, sy) = [(x,y) for (x,y) in asteroids if len(unique_angles(asteroids, x,y)) == best][0]

print (best, sx, sy)

cnt = 0
while True:
    for a, (x,y) in unique_angles(asteroids, sx, sy):
        cnt += 1
        asteroids.remove((x,y))
        if cnt == 200:
            print(a, x,y)
            exit(0)
