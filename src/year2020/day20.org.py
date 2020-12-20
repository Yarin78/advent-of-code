import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from vm.vm import *

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
lines = [line.strip() for line in sys.stdin.readlines()]

N = len(lines) // 12
SQUARE_SIZE = 12 if N == 144 else 3

tiles = []
tile_ids = []
for i in range(N):
    tile_id = get_ints(lines[i*12])[0]
    tile_ids.append(tile_id)
    #for y in range(10):
    tiles.append(lines[i*12+1:i*12+11])

assert len(tiles[0]) == 10
assert len(tiles[0][0]) == 10
assert len(tiles) == len(tile_ids)

print("last tile id", tile_ids[-1])

def rotate_tile(data):
    new_data = []
    tile_size = len(data)
    for y in range(tile_size):
        s = ""
        for x in range(tile_size):
            s += data[tile_size-1-x][y]
        new_data.append(s)
    return new_data

def flip_tile(data):
    new_data = []
    tile_size = len(data)
    for y in range(tile_size):
        new_data.append(data[tile_size-1-y])
    return new_data

def show_tile(data):
    for y in range(10):
        print(data[y])

# for i in range(9):
#     show_tile(tiles[i])
#     print()
# exit(0)


for i in range(N):
    versions = []
    cur = tiles[i]
    for _ in range(4):
        versions.append(cur)
        cur = rotate_tile(cur)
    cur = flip_tile(cur)
    for _ in range(4):
        versions.append(cur)
        cur = rotate_tile(cur)
    tiles[i] = versions


tile_map = init_matrix(SQUARE_SIZE, SQUARE_SIZE)

# tile_id[tile_num] => int
# tile[tile_num][rotation][y][x] => char
# tile_map[y][x] => (0-8, 0-8)  (tile_num, version)

tiles_used = set()

def matches_left_right(lt, lv, rt, rv):
    for y in range(10):
        if tiles[lt][lv][y][9] != tiles[rt][rv][y][0]:
            return False
    return True

def matches_up_down(ut, uv, dt, dv):
    for x in range(10):
        if tiles[ut][uv][9][x] != tiles[dt][dv][0][x]:
            return False
    return True

def can_be_left_border(lt, lv):
    for i in range(N):
        if i == lt:
            continue
        for j in range(8):
            if matches_left_right(i, j, lt, lv):
                return False
    return True

def can_be_right_border(rt, rv):
    for i in range(N):
        if i == rt:
            continue
        for j in range(8):
            if matches_left_right(rt, rv, i, j):
                return False
    return True

def can_be_top_border(tt, tv):
    for i in range(N):
        if i == tt:
            continue
        for j in range(8):
            if matches_up_down(i, j, tt, tv):
                return False
    return True

def can_be_bottom_border(bt, bv):
    for i in range(N):
        if i == bt:
            continue
        for j in range(8):
            if matches_up_down(bt, bv, i, j):
                return False
    return True


left_borders = set()
right_borders = set()
top_borders = set()
bottom_borders = set()

for j in range(N):
    for v in range(8):
        if can_be_left_border(j, v):
            left_borders.add((j, v))
        if can_be_right_border(j, v):
            right_borders.add((j, v))
        if can_be_top_border(j, v):
            top_borders.add((j, v))
        if can_be_bottom_border(j, v):
            bottom_borders.add((j, v))


def build_map():
    res = []
    for row in range(SQUARE_SIZE):
        for y in range(1,9):
            s = ""
            for col in range(SQUARE_SIZE):
                t, v = tile_map[row][col]
                s += tiles[t][v][y][1:9]
            res.append(s)
    return res

def go(x, y):
    #print(x,y)
    if y == SQUARE_SIZE:
        for y in range(SQUARE_SIZE):
            for x in range(SQUARE_SIZE):
                assert x == 0 or matches_left_right(tile_map[y][x-1][0], tile_map[y][x-1][1], tile_map[y][x][0], tile_map[y][x][1])
                assert y == 0 or matches_up_down(tile_map[y-1][x][0], tile_map[y-1][x][1], tile_map[y][x][0], tile_map[y][x][1])
        #show_all()
        c1 = tile_ids[tile_map[0][0][0]]
        c2 = tile_ids[tile_map[0][SQUARE_SIZE-1][0]]
        c3 = tile_ids[tile_map[SQUARE_SIZE-1][0][0]]
        c4 = tile_ids[tile_map[SQUARE_SIZE-1][SQUARE_SIZE-1][0]]
        print(c1, c2, c3, c4, c1*c2*c3*c4)
        #exit(0)
        return True
    if x == SQUARE_SIZE:
        return go(0, y+1)

    for i in range(N):
        if i not in tiles_used:
            tiles_used.add(i)
            for rot in range(8):
                if x == 0 and (i, rot) not in left_borders:
                    continue
                if x == SQUARE_SIZE-1 and (i, rot) not in right_borders:
                    continue
                if y == 0 and (i, rot) not in top_borders:
                    continue
                if y == SQUARE_SIZE-1 and (i, rot) not in bottom_borders:
                    continue
                if x > 0 and not matches_left_right(tile_map[y][x-1][0], tile_map[y][x-1][1], i, rot):
                    continue
                if y > 0 and not matches_up_down(tile_map[y-1][x][0], tile_map[y-1][x][1], i, rot):
                    continue
                tile_map[y][x] = (i, rot)
                if go(x+1, y):
                    return True
            tiles_used.remove(i)

go(0,0)

monster = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   "]

res = build_map()
#res = flip_tile(res)
#m = rotate_tile(res)
m = res
# for s in m:
#     print(s)

mcoords = []

size = len(m)

for y in range(3):
    for x in range(len(monster[y])):
        if monster[y][x] == '#':
            mcoords.append((x, y))

sm_coords = set()

def rotate_coords(coords):
    rotated = []
    for (x,y) in coords:
        rotated.append((-y, x))
    return rotated

def flip_coords(coords):
    flipped = []
    for (x,y) in coords:
        flipped.append((-x, y))
    return flipped

rmcoords = []
for flip in range(2):
    for rot in range(4):
        rmcoords.append(mcoords[:])
        mcoords = rotate_coords(mcoords)
    mcoords = flip_coords(mcoords)

for mc in rmcoords:
    for oy in range(-30, size + 30):
        for ox in range(-30, size + 30):
            found = True
            for (x, y) in mc:
                if oy+y < 0 or oy+y>=size or ox+x < 0 or ox+x>=size or res[oy+y][ox+x] != '#':
                    found = False
            if found:
                for (x, y) in mc:
                    sm_coords.add((ox+x, oy+y))
                print(ox, oy)

tot = 0
for row in range(size):
    tot += res[row].count('#')
print(tot, len(sm_coords), tot - len(sm_coords))
