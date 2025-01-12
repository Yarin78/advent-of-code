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
# sections = split_lines(lines)

grid = Grid(lines)

antinodes = set()

for c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789':
    points = grid.find(c)
    for p, q in permutations(points, 2):
        delta = q - p
        d = math.gcd(delta.x, delta.y)
        delta = Point(delta.x//d, delta.y//d)

        cur = p
        while grid.is_within(cur):
            antinodes.add(cur)
            cur += delta
        cur = p
        while grid.is_within(cur):
            antinodes.add(cur)
            cur -= delta

        # if grid.is_within(p-delta):
        #     antinodes.add(p - delta)
        # if grid.is_within(q + delta):
        #     antinodes.add(q + delta)

print(len(antinodes))

