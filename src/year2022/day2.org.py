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
lines = [line.strip() for line in sys.stdin.readlines()]
# Split input into an array of array of lines, split by empty line
# sections = split_lines(lines)

# data = [int(x) for x in lines]
ans = 0

def choice_score(c):
    if c == 'X': # rock
        return 1
    if c == 'Y': # paper
        return  2
    if c == 'Z': #sci
        return 3
    return 0

def win_score(you, they):
    if you == 'X' and they== 'A':
        return 3
    if you == 'Y' and they== 'B':
        return 3
    if you == 'Z' and they== 'C':
        return 3
    if you == 'X' and they== 'C':
        return 6
    if you == 'Y' and they =='A':
        return 6
    if you =='Z' and they == 'B':
        return 6
    return 0


for line in lines:
    they = line[0]
    you = line[2]

    if they=='A':
        if you=='X': # .they choose rock
            you='Z'
        elif you=='Y':
            you='X'
        else:
            you='Y'
    elif they=='B': # they choose paper
        if you=='X':
            you='X' # you choose rock
        elif you=='Y':
            you='Y' # you choose paper
        else:
            you='Z'
    elif they=='C': # they choose scissor
        if you=='X':
            you='Y'
        elif you=='Y':
            you='Z'
        else:
            you='X'

    ans += choice_score(you) + win_score(you, they)
    print(ans)



print(ans) # not 10,000