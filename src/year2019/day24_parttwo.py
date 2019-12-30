import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from intcode.intcode import *
from aocd import data, submit

lines = data.strip().split('\n')

empty = [".....", ".....",".....",".....","....."]

levels = [ empty[:], empty[:], lines, empty[:], empty[:]]
for minutes in range(200):
    print('minute', minutes)
    new_levels = [empty[:], empty[:]]
    num_bugs = 0
    for lvl in range(1, len(levels)-1):
        nl = []
        for y in range(5):
            s = ''
            for x in range(5):
                if x==2 and y == 2:
                    s += '.'
                    continue
                p = Point(x,y)
                cnt = 0

                for d in DIRECTIONS:
                    np = p+d
                    if np.x < 0:
                        cnt += levels[lvl-1][2][1] == '#'
                    elif np.x >= 5:
                        cnt += levels[lvl-1][2][3] == '#'
                    elif np.y < 0:
                        cnt += levels[lvl-1][1][2] == '#'
                    elif np.y >= 5:
                        cnt += levels[lvl-1][3][2] == '#'
                    elif np.y == 2 and np.x == 2:
                        if x == 1:
                            cnt += sum(levels[lvl+1][ny][0] == '#' for ny in range(5))
                        elif x == 3:
                            cnt += sum(levels[lvl+1][ny][4] == '#' for ny in range(5))
                        elif y == 1:
                            cnt += levels[lvl+1][0].count('#')
                        elif y == 3:
                            cnt += levels[lvl+1][4].count('#')
                        else:
                            assert False
                    else:
                        cnt += levels[lvl][np.y][np.x] == '#'

                if levels[lvl][p.y][p.x] == '#':
                    if cnt == 1:
                        s += '#'
                    else:
                        s += '.'
                else:
                    if cnt == 2 or cnt == 1:
                        s += '#'
                    else:
                        s += '.'
            num_bugs += s.count('#')

            nl.append(s)


        new_levels.append(nl)
    new_levels.append(empty[:])
    new_levels.append(empty[:])
    levels = new_levels

print(num_bugs)
