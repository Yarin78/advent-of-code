import sys
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

COLORS = ["blue","red","green"]
part1 = 0
part2 = 0
for row in lines:
    parts = multi_split(row, [':', ';', ',', ' '])
    game_id = int(parts[0][0][0][1])
    min_needed = defaultdict(int)

    all_set_ok = True
    for set_list in parts[1]:
        color_cnt = defaultdict(int)
        for pair in set_list:
            color = pair[1]
            cnt = int(pair[0])
            assert color in COLORS
            color_cnt[color] += cnt

        for c in COLORS:
            if color_cnt[c] > min_needed[c]:
                min_needed[c] = color_cnt[c]
        if color_cnt["red"] > 12 or color_cnt["green"] > 13 or color_cnt["blue"] > 14:
            all_set_ok = False
    if all_set_ok:
        part1 += game_id

    part2 += min_needed["blue"] * min_needed["red"] * min_needed["green"]

print(part1)
print(part2)
