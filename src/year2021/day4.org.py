import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
lines = [line.strip() for line in sys.stdin.readlines()]

numbers = list(map(int, lines[0].split(",")))
boards = []
row = 2
while row < len(lines):
    b = init_matrix(5, 5)
    for y in range(5):
        b[y] = list(map(int, tokenize(lines[row+y])))
    row += 6
    boards.append(b)

n = len(boards)

def board_won(b):
    for y in range(5):
        row_cnt = 0
        for x in range(5):
            if b[y][x] == -1:
                row_cnt += 1
        if row_cnt == 5:
            return True

    for x in range(5):
        col_cnt = 0
        for y in range(5):
            if b[y][x] == -1:
                col_cnt += 1
        if col_cnt == 5:
            return True

    return False

won = set()
for num in numbers:
    print("draw ", num)
    for i in range(n):
        if i in won:
            continue
        for y in range(5):
            for x in range(5):
                if boards[i][y][x] == num:
                    boards[i][y][x] = -1
        if board_won(boards[i]):
            won.add(i)
            print("WON ", i)
            if len(won) == n:
                sum = 0
                for y in range(5):
                    for x in range(5):
                        if boards[i][y][x] >= 0:
                            sum += boards[i][y][x]
                print(sum, num)
                print(sum * num)
                exit(0)
