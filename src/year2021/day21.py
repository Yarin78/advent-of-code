import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

SAMPLE = 0
if SAMPLE:
    P1 = 4
    P2 = 8
else:
    P1 = 7
    P2 = 8

LEN = 10
next_die = 1
players = [P1-1,P2-1]
score = [0,0]
turn = 0
num_rolls = 0
while score[0] < 1000 and score[1] < 1000:
    cur = players[turn]
    for t in range(3):
        num_rolls += 1
        cur = (cur + next_die) % LEN
        next_die = next_die + 1
        if next_die > 100:
            next_die = 1
    score[turn] += cur + 1
    players[turn] = cur
    turn = 1- turn
    print(score[0], score[1])


print(players)

print("RES", min(score[0],score[1]) * num_rolls)
