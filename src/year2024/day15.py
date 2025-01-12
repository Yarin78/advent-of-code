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

movements = "".join(sections[1])

# grid = Grid(sections[0])
# cur = grid.find('@')[0]
# grid[cur] = '.'

DIRS = {
    '^': NORTH,
    '>': EAST,
    '<': WEST,
    'v': SOUTH
}

# for c in movements:
#     d = DIRS[c]

#     p = cur
#     while grid[p+d] == 'O':
#         p += d
#     if grid[p+d] == '#':
#         continue
#     assert grid[p+d] == '.'

#     while p != cur:
#         grid[p+d] = 'O'
#         p -= d
#     grid[p+d] = '.'
#     cur += d

# ans = 0
# for p in grid.find('O'):
#     ans += p.y * 100 + p. x
# print(ans)

tmp_grid = Grid(sections[0])
grid = Grid.empty(tmp_grid.xsize * 2, tmp_grid.ysize, '.')
for p in tmp_grid.all_points():
    if tmp_grid[p] == 'O':
        grid[p.y, p.x*2] = '['
        grid[p.y, p.x*2+1] = ']'
    elif tmp_grid[p] == '@':
        grid[p.y, p.x*2] = '@'
    elif tmp_grid[p] == '#':
        grid[p.y, p.x*2] = '#'
        grid[p.y, p.x*2+1] = '#'

cur = grid.find('@')[0]
grid[cur] = '.'

# grid.show()

for c in movements:
    print(f"Move {c}:")
    d = DIRS[c]

    if d in (WEST, EAST):
        p = cur
        while grid[p+d] in '[]':
            p += d
        if grid[p+d] == '#':
            continue
        assert grid[p+d] == '.'

        while p != cur:
            grid[p+d] = grid[p]
            p -= d
        grid[p+d] = '.'
        cur += d
    else:
        affected = {cur+d}
        possible = True
        if grid[cur+d] == '#':
            possible = False
        q = Queue()
        q.put(cur+d)
        while not q.empty():
            p = q.get()
            if grid[p] in '[]' and p+d not in affected:
                affected.add(p+d)
                q.put(p+d)
            if grid[p] == '[' and p+EAST not in affected:
                affected.add(p + EAST)
                q.put(p+EAST)
            if grid[p] == ']' and p+WEST not in affected:
                affected.add(p + WEST)
                q.put(p+WEST)

        affected = sorted(affected, key=lambda p: p.y if d == NORTH else -p.y)
        # print("Affected:", affected)
        for p in affected:
            if grid[p] in '[]' and grid[p+d] == '#':
                possible = False

        if possible:
            for sq in affected:
                if grid[sq] in '[]':
                    assert grid[sq+d] == '.'
                    grid[sq+d] = grid[sq]
                    grid[sq] = '.'
            cur += d

    # grid[cur] = '@'
    # grid.show()
    # grid[cur] = '.'

ans = 0
for p in grid.find('['):
    ans += p.y * 100 + p. x
print(ans)
