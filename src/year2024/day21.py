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


def dir_key_pad_left(cur):
    if cur == 0 or cur == 2:
        return None
    return cur - 1

def dir_key_pad_right(cur):
    if cur == 1 or cur == 4:
        return None
    return cur + 1

def dir_key_pad_up(cur):
    if cur < 3:
        return None
    return cur - 3

def dir_key_pad_down(cur):
    if cur >= 2:
        return None
    return cur + 3

def num_key_pad_left(cur):
    if cur in (7, 4, 1, 0):
        return None
    if cur == 10:
        return 0
    return cur - 1

def num_key_pad_right(cur):
    if cur in (9, 6, 3, 10):
        return None
    if cur == 0:
        return 10
    return cur + 1

def num_key_pad_up(cur):
    if cur in (7, 8, 9):
        return None
    if cur == 0:
        return 2
    if cur == 10:
        return 3
    return cur + 3

def num_key_pad_down(cur):
    if cur in (1, 0, 10):
        return None
    if cur == 2:
        return 0
    if cur == 3:
        return 10
    return cur - 3

def solve(code: str, num_robots):
    start_state = tuple([0, 10] + [1] * (num_robots-1))
    queue = Queue()
    seen = {}

    def add(state, steps):
        if state in seen:
            return
        seen[state] = steps
        queue.put(state)

    add(start_state, 0)
    while not queue.empty():
        cur_state = queue.get()
        cur_steps = seen[cur_state]

        # print(cur_state, cur_steps)
        if cur_state[0] == len(code):
            return cur_steps

        v = {
            "<": dir_key_pad_left(cur_state[num_robots]),
            ">": dir_key_pad_right(cur_state[num_robots]),
            "^": dir_key_pad_up(cur_state[num_robots]),
            "v": dir_key_pad_down(cur_state[num_robots])
        }
        for c, w in v.items():
            if w is not None:
                v = list(cur_state)
                v[-1] = w
                add(tuple(v), cur_steps+1)

        i = num_robots

        while i > 0:
            if i == 1:
                if (code[cur_state[0]] == 'A' and cur_state[1] == 10) or (code[cur_state[0]] != 'A' and cur_state[1] == int(code[cur_state[0]])):
                    v = list(cur_state)
                    v[0] += 1
                    add(tuple(v), cur_steps+1)
                break
            elif cur_state[i] != 1:
                match cur_state[i]:
                    case 0:
                        ns = dir_key_pad_up(cur_state[i-1]) if i  > 2 else num_key_pad_up(cur_state[i-1])
                    case 2:
                        ns = dir_key_pad_left(cur_state[i-1]) if i  > 2 else num_key_pad_left(cur_state[i-1])
                    case 3:
                        ns = dir_key_pad_down(cur_state[i-1]) if i  > 2 else num_key_pad_down(cur_state[i-1])
                    case 4:
                        ns = dir_key_pad_right(cur_state[i-1]) if i  > 2 else num_key_pad_right(cur_state[i-1])
                if ns is not None:
                    v = list(cur_state)
                    v[i-1] = ns
                    add(tuple(v), cur_steps+1)
                break
            else:
                i -= 1


        # if cur_state[3] != 1:
        #     match cur_state[3]:
        #         case 0:
        #             ns = dir_key_pad_up(cur_state[2])
        #         case 2:
        #             ns = dir_key_pad_left(cur_state[2])
        #         case 3:
        #             ns = dir_key_pad_down(cur_state[2])
        #         case 4:
        #             ns = dir_key_pad_right(cur_state[2])
        #     if ns is not None:
        #         add((cur_state[0], cur_state[1], ns, cur_state[3]), cur_steps+1)
        # elif cur_state[2] != 1:
        #     match cur_state[2]:
        #         case 0:
        #             ns = num_key_pad_up(cur_state[1])
        #         case 2:
        #             ns = num_key_pad_left(cur_state[1])
        #         case 3:
        #             ns = num_key_pad_down(cur_state[1])
        #         case 4:
        #             ns = num_key_pad_right(cur_state[1])
        #     if ns is not None:
        #         add((cur_state[0], ns, cur_state[2], cur_state[3]), cur_steps+1)
        # else:
        #     if (code[cur_state[0]] == 'A' and cur_state[1] == 10) or (code[cur_state[0]] != 'A' and cur_state[1] == int(code[cur_state[0]])):
        #         add((cur_state[0]+1, cur_state[1], cur_state[2], cur_state[3]), cur_steps+1)

    return -1

def simulate(seq: str):
    r1 = 10
    r2 = 1
    r3 = 1
    code = ""
    for c in seq:
        # print(f"Step {c}: {r1} {r2} {r3}")
        match c:
            case "<":
                r3 = dir_key_pad_left(r3)
            case ">":
                r3 = dir_key_pad_right(r3)
            case "^":
                r3 = dir_key_pad_up(r3)
            case "v":
                r3 = dir_key_pad_down(r3)
            case "A":
                match r3:
                    case 0:
                        r2 = dir_key_pad_up(r2)
                    case 2:
                        r2 = dir_key_pad_left(r2)
                    case 3:
                        r2 = dir_key_pad_down(r2)
                    case 4:
                        r2 = dir_key_pad_right(r2)
                    case 1:
                        match r2:
                            case 0:
                                r1 = num_key_pad_up(r1)
                            case 2:
                                r1 = num_key_pad_left(r1)
                            case 3:
                                r1 = num_key_pad_down(r1)
                            case 4:
                                r1 = num_key_pad_right(r1)
                            case 1:
                                code += "A" if r1 == 10 else str(r1)

        assert r1 is not None and r2 is not None and r3 is not None
    return code


ans = 0
for line in lines:
    for num_robots in range(2, 9):
        steps = solve(line, num_robots)
        print(f"{num_robots} robots requires {steps} steps)")
    ans += steps * int(line[:-1])
    print()

# print(simulate("<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"))
print(ans)