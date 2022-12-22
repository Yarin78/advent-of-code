import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
# scanner = Scanner(sys.stdin)
lines = [line for line in sys.stdin.readlines()]
xsize = 0

for line in lines[:-2]:
    xsize = max(xsize, len(line))

new_lines = []
for line in lines[:-2]:
    new_lines.append(line[:-1] + " " * (xsize - len(line)))

grid = Grid(new_lines)
dir = lines[-1]

x = 0
y = 0
while grid[y,x] == ' ':
    x += 1
# print(x,y)

step_len = get_ints(dir)
step_dir = []
for s in dir:
    if s in ('R', 'L'):
        step_dir.append(s)

SAMPLE = 0

CUBE_SIZE = 4 if SAMPLE else 50

DIRS = [RIGHT, DOWN, LEFT, UP]
dir = 0

def next_sq(cur, dir):
    new_cur = cur
    while True:
        new_cur += DIRS[dir]
        if new_cur.y < 0:
            new_cur = Point(new_cur.x, grid.ysize-1)
        if new_cur.y >= grid.ysize:
            new_cur = Point(new_cur.x, 0)
        if new_cur.x < 0:
            new_cur = Point(grid.xsize-1, new_cur.y)
        if new_cur.x >= grid.xsize:
            new_cur = Point(0, new_cur.y)
        if grid[new_cur] != ' ':
            break
    return new_cur, dir


SAMPLE_FACE_MAPPING = {

}

FACE_MAPPING = {
    (1, UP): (6, LEFT, 0),
    (1, LEFT): (4, LEFT, 1),
    (2, UP): (6, DOWN, 0),
    (2, RIGHT): (5, RIGHT, 1),
    (2, DOWN): (3, RIGHT, 0),
    (3, LEFT): (4, UP, 0),
    (3, RIGHT): (2, DOWN, 0),
    (4, UP): (3, LEFT, 0),
    (4, LEFT): (1, LEFT, 1),
    (5, DOWN): (6, RIGHT, 0),
    (5, RIGHT): (2, RIGHT, 1),
    (6, LEFT): (1, UP, 0),
    (6, DOWN): (2, UP, 0),
    (6, RIGHT): (5, DOWN, 0)
}

SAMPLE_FACE_COORDS = {
    1: Point(2,0),
    2: Point(0,1),
    3: Point(1,1),
    4: Point(2,1),
    5: Point(2,2),
    6: Point(3,2)
}

FACE_COORDS = {
    1: Point(1,0),
    2: Point(2,0),
    3: Point(1,1),
    4: Point(0,2),
    5: Point(1,2),
    6: Point(0,3)
}


def get_face(x, y):
    x = x % (CUBE_SIZE * 4)
    face_x = cur.x // CUBE_SIZE
    face_y = cur.y // CUBE_SIZE
    coords = SAMPLE_FACE_COORDS if SAMPLE else FACE_COORDS
    for face_num, face_coord in coords.items():
        if face_coord == Point(face_x, face_y):
            return face_num
    assert False

for (src_face, src_dir), (target_face, target_dir, inv) in FACE_MAPPING.items():
    rev_face, rev_dir, rev_inverse = FACE_MAPPING[(target_face, target_dir)]
    assert rev_face == src_face
    assert rev_dir == src_dir
    assert rev_inverse == inv


def next_sq2(cur, dir):
    face_mapping = SAMPLE_FACE_MAPPING if SAMPLE else FACE_MAPPING
    face_coords = SAMPLE_FACE_COORDS if SAMPLE else FACE_COORDS

    while True:
        new_cur = cur + DIRS[dir]
        if grid.is_within(new_cur) and grid[new_cur] != ' ':
            return new_cur, dir

        face = get_face(cur.x, cur.y)
        face_x = cur.x % CUBE_SIZE
        face_y = cur.y % CUBE_SIZE

        if not SAMPLE:
            new_face, entrance, inv = face_mapping[(face, DIRS[dir])]
            if DIRS[dir] in (UP, DOWN):
                i = face_x
            else:
                i = face_y
            if inv:
                i = CUBE_SIZE - 1 - i

            if entrance == LEFT:
                new_cur = Point(0, i)
                new_dir = 0
            elif entrance == RIGHT:
                new_cur = Point(CUBE_SIZE-1,i)
                new_dir = 2
            elif entrance == UP:
                new_cur = Point(i, 0)
                new_dir = 1
            elif entrance == DOWN:
                new_cur = Point(i,CUBE_SIZE-1)
                new_dir = 3
            else:
                assert False

            fp = face_coords[new_face]
            new_cur += Point(fp.x * CUBE_SIZE, fp.y * CUBE_SIZE)

            print(f"At {cur}, face {face}, going {DIRS[dir]}, reaching {new_cur} dir {DIRS[new_dir]}")
            return (new_cur, new_dir)

        else:
            # Hard coded the sample instead of using face_mappings
            if face == 4 and DIRS[dir] == RIGHT:
                new_cur = Point(CUBE_SIZE * 4 - 1 - face_y, CUBE_SIZE * 2)
                new_dir = 1
                print(f"At {cur}, face {face}, going {DIRS[dir]}, reaching {new_cur} dir {DIRS[new_dir]}")
                return (new_cur, new_dir)
            if face == 5 and DIRS[dir] == DOWN:
                new_cur = Point(CUBE_SIZE - 1 - face_x, CUBE_SIZE * 2 - 1)
                new_dir = 3
                print(f"At {cur}, face {face}, going {DIRS[dir]}, reaching {new_cur} dir {DIRS[new_dir]}")
                return (new_cur, new_dir)
            if face == 3 and DIRS[dir] == UP:
                new_cur = Point(CUBE_SIZE * 2, face_x)
                new_dir = 0
                print(f"At {cur}, face {face}, going {DIRS[dir]}, reaching {new_cur} dir {DIRS[new_dir]}")
                return (new_cur, new_dir)

        print(f"At {cur}, face {face}, going {DIRS[dir]}")
        assert False

plot = {}
cur = Point(x,y)
plot[cur] = dir
step_dir.append('.')
for len, dir_change in zip(step_len, step_dir):
    for _ in range(len):
        # new_cur, dir = next_sq(cur, dir)
        new_cur, new_dir = next_sq2(cur, dir)

        if grid[new_cur] == '.':
            cur = new_cur
            dir = new_dir
        else:
            # print(f"Block at {new_cur}")
            break

        print(f"At {cur}")
        plot[cur] = dir
    if dir_change == 'R':
        dir = (dir+1)%4
    elif dir_change == 'L':
        dir = (dir+3)%4

    plot[cur] = dir

# dirs = ">v<^"
# for y in range(grid.ysize):
#     s = ""
#     for x in range(grid.xsize):
#         if Point(x,y) in plot:
#             s += dirs[plot[Point(x,y)]]
#         else:
#             s += grid[y,x]
#     print(s)

# print()

print((cur.y+1) * 1000 + (cur.x+1) * 4 + dir)
