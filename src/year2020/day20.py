import sys
import math
from yal.geo2d import Point
from yal.tiles import *

lines = [line.strip() for line in sys.stdin.readlines()]

NUM_TILES = len(lines) // 12
SQUARE_SIZE = int(math.sqrt(NUM_TILES))

tiles = {int(lines[i*12][5:-1]): Tile(lines[i*12+1:i*12+11], id=int(lines[i*12][5:-1])).all_rotations_and_flips() for i in range(NUM_TILES)}

left_borders = set((tid, t) for tid, trot in tiles.items() for t in trot if not any(tiles_match_left_right(x, t) for xid, xrot in tiles.items() for x in xrot if xid != tid))
right_borders = set((tid, t) for tid, trot in tiles.items() for t in trot if not any(tiles_match_left_right(t, x) for xid, xrot in tiles.items() for x in xrot if xid != tid))
top_borders = set((tid, t) for tid, trot in tiles.items() for t in trot if not any(tiles_match_up_down(x, t) for xid, xrot in tiles.items() for x in xrot if xid != tid))
bottom_borders = set((tid, t) for tid, trot in tiles.items() for t in trot if not any(tiles_match_up_down(t, x) for xid, xrot in tiles.items() for x in xrot if xid != tid))

corner_ids = list(set(id for id, _ in left_borders.intersection(top_borders)))
# Part 1
print(corner_ids[0] * corner_ids[1] * corner_ids[2] * corner_ids[3])

# Part 2
puzzle = {}  # Point -> Tile
tile_ids_left = set(tiles.keys())

def build_puzzle(x, y):
    if y == SQUARE_SIZE:
        return True
    if x == SQUARE_SIZE:
        return build_puzzle(0, y+1)

    for tile_id in list(tile_ids_left):
        tile_ids_left.remove(tile_id)
        for t in tiles[tile_id]:
            if x == 0 and (tile_id, t) not in left_borders:
                continue
            if x == SQUARE_SIZE-1 and (tile_id, t) not in right_borders:
                continue
            if y == 0 and (tile_id, t) not in top_borders:
                continue
            if y == SQUARE_SIZE-1 and (tile_id, t) not in bottom_borders:
                continue
            if x > 0 and not tiles_match_left_right(puzzle[Point(x-1, y)], t):
                continue
            if y > 0 and not tiles_match_up_down(puzzle[Point(x, y-1)], t):
                continue
            puzzle[Point(x, y)] = t
            if build_puzzle(x+1, y):
                return True
        tile_ids_left.add(tile_id)

build_puzzle(0,0)

final_map = Tile(["".join([puzzle[Point(col, row)].data[y][1:9] for col in range(SQUARE_SIZE)]) for row in range(SQUARE_SIZE) for y in range(1,9)])

monster = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   "]


monster_coords = [Point(x, y) for y in range(len(monster)) for x in range(len(monster[y])) if monster[y][x] == '#']

for rotated_map in final_map.all_rotations_and_flips():
    points = set(rotated_map.points("#"))
    monster_points = set()
    for offset_y in range(rotated_map.ysize):
        for offset_x in range(rotated_map.xsize):
            offset_monster = set(p + Point(offset_x, offset_y) for p in monster_coords)
            if offset_monster.issubset(points):
                monster_points.update(offset_monster)

    if monster_points:
        print(len(points) - len(monster_points))
