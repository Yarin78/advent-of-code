from functools import cache
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

num_key_to_coords = {
    '7' : (0,0),
    '8' : (1,0),
    '9' : (2,0),
    '4': (0,1),
    '5': (1,1),
    '6': (2,1),
    '1': (0,2),
    '2': (1,2),
    '3': (2,2),
    '0': (1,3),
    'A': (2, 3),
}

dir_key_pad_coords ={
    '^': (1,0),
    'v': (1,1),
    '<': (0,1),
    '>': (2,1),
    'A': (2,0),
}

def keypad_way(a, b, coords, invalid_coord):
    x1,y1 = coords[a]
    x2,y2 = coords[b]
    if x1==x2 and y1==y2:
        return [""]

    horz = ">" * (x2-x1) if x2 > x1 else "<" * (x1-x2)
    vert = "v" * (y2-y1) if y2 > y1 else "^" * (y1-y2)

    if x1 == x2:
        return [vert]
    if y1 == y2:
        return [horz]

    def is_valid(s):
        x,y = x1,y1
        for c in s:
            if c == ">":
                x += 1
            elif c == "<":
                x -= 1
            elif c == "v":
                y += 1
            elif c == "^":
                y -= 1
            if (x,y) == invalid_coord:
                return False
        assert (x,y) == (x2,y2)
        return True

    res = []
    if is_valid(horz+vert):
        res.append(horz+vert)
    if is_valid(vert+horz):
        res.append(vert+horz)

    return res

@cache
def num_keypad_way(a, b):
    return keypad_way(a, b, num_key_to_coords, (0,3))

@cache
def dir_keypad_way(a, b):
    return keypad_way(a, b, dir_key_pad_coords, (0,0))


def solve(code: str, num_robots: int):

    @cache
    def press(c: str, rob: int, cur: str):
        if rob == num_robots:
            return 1
        ways = num_keypad_way(cur, c) if rob == 0 else dir_keypad_way(cur, c)

        ans = []
        for way in ways:
            cc = 'A'
            num_presses = 0
            for w in way:
                num_presses += press(w, rob+1, cc)
                cc = w
            num_presses += press('A', rob+1, cc)
            ans.append(num_presses)

        return min(ans)

    cnt = 0
    cur = 'A'
    for c in code:
        cnt += press(c, 0, cur)
        cur = c
    return cnt


ans = 0
for line in lines:
    ans += solve(line, 26) * int(line[:-1])

print(ans)
