import sys
from lib.geo2d import *

input = sys.stdin
input = open('year2016/day2.in')

dir_map = { 'U' : NORTH, 'L': WEST, 'R': EAST, 'D': SOUTH }
keypad = ["  1  ", " 234 ", "56789", " ABC ", "  D  "]
cur = Point(0,2)
for line in input.readlines():
    for c in line.strip():
        np = cur + dir_map[c]
        if np.x >= 0 and np.x < 5 and np.y >= 0 and np.y < 5 and keypad[np.y][np.x] != ' ':
            cur = np
    sys.stdout.write(keypad[cur.y][cur.x])

print()

