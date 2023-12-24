import sys
import numpy as np
from sympy import solve, symbols
from dataclasses import dataclass
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo3d import *

# Make sure ~/.config/aocd/token is correct! (Application tab -> Cookies)
# scanner = Scanner(sys.stdin)
lines = [line.strip() for line in sys.stdin.readlines()]

hail = []
for line in lines:
    a, b = line.split("@")
    p = list(map(int, a.strip().split(", ")))
    q = list(map(int, b.strip().split(", ")))
    hail.append((Point(p[0], p[1], p[2]), Point(q[0], q[1], q[2])))
    # hail.append((Point(p[1], p[2], p[0]), Point(q[1], q[2], q[0])))
    # hail.append((Point(p[2], p[0], p[1]), Point(q[2], q[0], q[1])))

# MIN_BOUND = Point(7, 7)
# MAX_BOUND = Point(27, 27)

# MIN = 200000000000000
# MAX = 400000000000000
# MIN_BOUND = Point(MIN, MIN)
# MAX_BOUND = Point(MAX, MAX)

# EPSILON = 0

def intersect(h1, h2):
    p1 = h1[0]
    q1 = h1[1]
    p2 = h2[0]
    q2 = h2[1]
    A = p1.x
    B = p1.y
    C = q1.x
    D = q1.y
    E = p2.x
    F = p2.y
    G = q2.x
    H = q2.y

    d = C * H - G * D
    if d != 0:
        t1 = (H * (E - A) - G * (F - B)) / d
        t2 = (D * (E - A) - C * (F - B)) / d

        h1p = p1 + q1 * t1
        h2p = p2 + q2 * t2

        # print(h1p)
        if (
            t1 >= -EPSILON
            and t2 >= -EPSILON
            and h1p.x >= MIN_BOUND.x - EPSILON
            and h1p.y >= MIN_BOUND.y - EPSILON
            and h1p.x <= MAX_BOUND.x + EPSILON
            and h1p.y <= MAX_BOUND.y + EPSILON
        ):
            # print("cross")
            return 1
    return 0


# cnt = 0
# for i, h1 in enumerate(hail):
#     for j, h2 in enumerate(hail):
#         if i >= j:
#             continue
#         cnt += intersect(h1, h2)
#
# print(cnt)


N = 5

def solvex(xv):
    A = []
    B = []
    for i, (p, q) in enumerate(hail[:N]):
        B.append(-p.x)
        xrow = [-1] + [0] * N
        xrow[1+i] = q.x-xv
        A.append(xrow)

    print(A)
    print(B)
    X, residuals, rank, s = np.linalg.lstsq(A, B)
    print(X)
    int_diffs = [abs(a - round(a)) for a in X]
    if all(x < 1e-5 for x in int_diffs):
        return X
    else:
        return None


def solvexy(xv, yv):
    A = []
    B = []
    for i, (p, q) in enumerate(hail[:N]):
        B.append(-p.x)
        B.append(-p.y)
        xrow = [-1, 0] + [0] * N
        yrow = [0, -1] + [0] * N
        xrow[2+i] = q.x-xv
        yrow[2+i] = q.y-yv
        A.append(xrow)
        A.append(yrow)

    # print(A)
    # print(B)
    X, residuals, rank, s = np.linalg.lstsq(A, B)

    int_diffs = [abs(a - round(a)) for a in X]
    if all(x < 1e-5 for x in int_diffs):
        # print(X)
        return X
    else:
        return None


def solvexyz(xv, yv, zv):
    A = []
    B = []
    for i, (p, q) in enumerate(hail[:N]):
        B.append(-p.x)
        B.append(-p.y)
        B.append(-p.z)
        xrow = [-1, 0, 0] + [0] * N
        yrow = [0, -1, 0] + [0] * N
        zrow = [0, 0, -1] + [0] * N
        xrow[3+i] = q.x-xv
        yrow[3+i] = q.y-yv
        zrow[3+i] = q.z-zv
        A.append(xrow)
        A.append(yrow)
        A.append(zrow)

    # print(A)
    # print(B)
    X, residuals, rank, s = np.linalg.lstsq(A, B)
    int_diffs = [abs(a - round(a)) for a in X]
    print(X)
    if all(x < 1e-5 for x in int_diffs):

        return X
    else:
        return None


# solvexy(-3, 1)

# solvexyz(-3, 1, 2)

# solvexyz(330, -94, 53)


# BOUND = 2000

# for xv in range(-BOUND, BOUND):
#     # print(f"xv={xv}")
#     for yv in range(-BOUND, BOUND):
#         for zv in range(-BOUND, BOUND):
#             X = solvexyz(xv, yv, zv)
#             if X is not None:
#                 print(X)


# for xv in range(-BOUND, BOUND):
#     print(f"xv={xv}")
#     for yv in range(-BOUND, BOUND):
#         X = solvexy(xv, yv)
#         if X is not None:
#             print(X)
#             exit(0)

# for xv in range(-BOUND, BOUND):
#     # print(f"xv={xv}")
#     X = solvex(xv)
#     if X is not None:
#         print(X)

x0, y0, z0, xv, yv, zv, t1, t2, t3 = symbols('x0 y0 z0 xv yv zv t1 t2 t3')
equations = []
for (p, q), t in zip(hail[:3], [t1, t2, t3]):
    equations.append(p.x + q.x*t - (x0 + xv*t))
    equations.append(p.y + q.y*t - (y0 + yv*t))
    equations.append(p.z + q.z*t - (z0 + zv*t))

res = solve(equations, x0, y0, z0, xv, yv, zv, t1, t2, t3, dict=True)[0]
print(res[x0] + res[y0] + res[z0])

