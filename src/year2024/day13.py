import sys
from dataclasses import dataclass
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

# Make sure ~/.config/aocd/token is correct! (Application tab -> Cookies)
# scanner = Scanner(sys.stdin)
lines = [line.strip() for line in sys.stdin.readlines()]
# Split input into an array of array of lines, split by empty line
sections = split_lines(lines)

ans = 0
for i, section in enumerate(sections):
    ax, ay = get_ints(section[0])
    bx, by = get_ints(section[1])
    tx, ty = get_ints(section[2])

    tx += 10000000000000
    ty += 10000000000000

    bcnt = (tx*ay-ax*ty) // (bx*ay-by*ax)
    acnt = (tx - bcnt * bx) // ax
    # acnt = (tx*by-bx*ty) // (bx*ay-by*ax)
    if ax*acnt+bx*bcnt == tx and ay*acnt+by*bcnt == ty and acnt >= 0 and bcnt >= 0:
        cost = acnt * 3 + bcnt
        print(f"Section {i} has solution with cost {cost}")
        ans += cost

    # best_cost = -1
    # for acnt in range(10001):
    #     bcnt1 = (tx - ax * acnt) // bx
    #     bcnt2 = (ty - ay * acnt) // by
    #     if bcnt1 >= 0 and bcnt1 == bcnt2 and ax*acnt+bx*bcnt1 == tx and ay*acnt+by*bcnt1 == ty:
    #         cost = acnt * 3 + bcnt1
    #         print(f"Section {i} has solution with cost {cost}")
    #         if best_cost < 0 or cost < best_cost:
    #             best_cost = cost

    # if best_cost >= 0:
    #     ans += best_cost

print(ans)
