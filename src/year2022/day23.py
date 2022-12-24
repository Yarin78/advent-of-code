import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

lines = [line.strip() for line in sys.stdin.readlines()]

elves = set()
for y,line in enumerate(lines):
    for x, s in enumerate(line):
        if s == '#':
            elves.add(Point(x,y))

prop_dirs = [
    ([NORTH, NORTH_EAST, NORTH_WEST], NORTH),
    ([SOUTH, SOUTH_EAST, SOUTH_WEST], SOUTH),
    ([WEST, NORTH_WEST, SOUTH_WEST], WEST),
    ([EAST, NORTH_EAST, SOUTH_EAST], EAST),
]

def show(elves):
    minx = min(elf.x for elf in elves)
    maxx = max(elf.x for elf in elves)
    miny = min(elf.y for elf in elves)
    maxy = max(elf.y for elf in elves)
    for y in range(miny, maxy+1):
        s = ""
        for x in range(minx, maxx+1):
            if Point(x,y) in elves:
                s += '#'
            else:
                s += '.'
        print(s)
    print()

round = 0
while True:
    #show(elves)
    prev_elves = set(elves)
    proposed_squares = defaultdict(int)
    prop_elf_sq = {}

    for elf in prev_elves:
        propose = False
        for dir in DIRECTIONS_INCL_DIAGONALS:
            if elf+dir in elves:
                propose = True

        if propose:
            prop_sq = None
            for i in range(4):
                check_dirs, move_dir = prop_dirs[(i+round)%4]
                has_elf = False
                for cd in check_dirs:
                    if elf+cd in prev_elves:
                        has_elf = True
                if not has_elf:
                    prop_sq = elf + move_dir
                    break

            if prop_sq:
                #print(f"Elf at {elf} propose move to {prop_sq}")
                proposed_squares[prop_sq] += 1
                prop_elf_sq[elf] = prop_sq

    moved = False
    elves = set()
    for elf in prev_elves:
        if elf not in prop_elf_sq:
            elves.add(elf)
        else:
            if proposed_squares[prop_elf_sq[elf]] == 1:
                elves.add(prop_elf_sq[elf])
                moved = True
            else:
                elves.add(elf)

    if not moved:
        break
    round += 1
    if round == 10:
        minx = min(elf.x for elf in elves)
        maxx = max(elf.x for elf in elves)
        miny = min(elf.y for elf in elves)
        maxy = max(elf.y for elf in elves)

        print("Part 1:", (maxx-minx+1) * (maxy-miny+1) - len(elves))


#show(elves)

print("Part 2:", round+1)