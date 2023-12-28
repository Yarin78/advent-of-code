import sys
from sympy import solve, symbols, Eq
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo3d import *

lines = [line.strip() for line in sys.stdin.readlines()]

hail: List[Tuple[Point, Point]] = []
for line in lines:
    a, b = line.split("@")
    p = list(map(int, a.strip().split(", ")))
    q = list(map(int, b.strip().split(", ")))
    hail.append((Point(p[0], p[1], p[2]), Point(q[0], q[1], q[2])))


MIN = 200000000000000
MAX = 400000000000000
MIN_BOUND = Point(MIN, MIN, MIN)
MAX_BOUND = Point(MAX, MAX, MAX)

# p1.x + t1 * q1.x = p2.x + t2 * q2.x
# p1.y + t1 * q1.y = p2.y + t2 * q2.y
p1x, p1y, q1x, q1y, p2x, p2y, q2x, q2y, t1, t2 = symbols('p1x p1y q1x q1y p2x p2y q2x q2y t1 t2')

solution = solve([
    Eq(p1x + t1 * q1x, p2x + t2 * q2x),
    Eq(p1y + t1 * q1y, p2y + t2 * q2y)], [t1, t2], as_dict=True)

print(solution[t1], solution[t2])
# (-p1x*q2y + p1y*q2x + p2x*q2y - p2y*q2x)/(q1x*q2y - q1y*q2x)
# (-p1x*q1y + p1y*q1x + p2x*q1y - p2y*q1x)/(q1x*q2y - q1y*q2x)
# Using solution[t1].subs(...) below works but is very slow.
# Much faster to inline the expression above

def intersect(p1: Point, q1: Point, p2: Point, q2: Point):
    det = q1.x*q2.y - q1.y*q2.x
    if det:
        t1 = (-p1.x*q2.y + p1.y*q2.x + p2.x*q2.y - p2.y*q2.x)/det
        t2 = (-p1.x*q1.y + p1.y*q1.x + p2.x*q1.y - p2.y*q1.x)/det
        hp = p1 + q1 * t1

        if (
            t1 >= 0
            and t2 >= 0
            and hp.x >= MIN_BOUND.x
            and hp.y >= MIN_BOUND.y
            and hp.x <= MAX_BOUND.x
            and hp.y <= MAX_BOUND.y
        ):
            return 1
    return 0


print(sum(intersect(h1[0], h1[1], h2[0], h2[1]) for h1,h2 in itertools.combinations(hail, 2)))


x0, y0, z0, xv, yv, zv, t1, t2, t3 = symbols('x0 y0 z0 xv yv zv t1 t2 t3')
equations = []
for (p, q), t in zip(hail[:3], [t1, t2, t3]):
    equations.append(p.x + q.x*t - (x0 + xv*t))
    equations.append(p.y + q.y*t - (y0 + yv*t))
    equations.append(p.z + q.z*t - (z0 + zv*t))

res = solve(equations, x0, y0, z0, xv, yv, zv, t1, t2, t3, dict=True)[0]
print(res[x0] + res[y0] + res[z0])
