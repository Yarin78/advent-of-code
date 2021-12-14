import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

lines = [line.strip() for line in sys.stdin.readlines()]

matching = {
    '(': ')',
    '{': '}',
    '<': '>',
    '[': ']'
}

char_score={
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

char2_score={
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

score = 0
comp_score = []
for line in lines:
    stack = ""
    ill_char = None
    for c in line:
        if c in matching.keys():
            stack += c
        elif c in matching.values():
            assert len(stack)>0
            if matching[stack[-1]] == c:
                stack = stack[:-1]
            else:
                ill_char = c
                break
    if ill_char is not None:
        score += char_score[ill_char]
    else:
        lscore = 0
        for c in stack[::-1]:
            lscore *= 5
            lscore += char2_score[matching[c]]
        comp_score.append(lscore)



print(score)
comp_score=sorted(comp_score)
print(comp_score[len(comp_score)//2])
