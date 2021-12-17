import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

# target area: x=281..311, y=-74..-54

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
# scanner = Scanner(sys.stdin)
lines = [line.strip() for line in sys.stdin.readlines()]

sample = 0

if sample:
    TARGET_MIN_X = 20
    TARGET_MAX_X = 30
    TARGET_MIN_Y = -10
    TARGET_MAX_Y = -5
else:
    TARGET_MIN_X = 281
    TARGET_MAX_X = 311
    TARGET_MIN_Y = -74
    TARGET_MAX_Y = -54


target_height = TARGET_MAX_Y - TARGET_MIN_Y + 1

max_y = -999
num_y = 0
yvals = set()
min_y_vel = 0
max_y_vel = 0

for yvel_start in range(-100, 100):
    y = 0
    yvel = yvel_start
    hy = yvel_start
    while y >= TARGET_MIN_Y:
        hy = max(hy, y)
        within_y = y >= TARGET_MIN_Y and y <= TARGET_MAX_Y
        # print(y, y >= TARGET_MIN_Y and y <= TARGET_MAX_Y)
        y += yvel
        yvel -= 1
        if within_y:
            min_y_vel = min(min_y_vel, yvel_start)
            max_y_vel = max(max_y_vel, yvel_start)
            max_y = max(max_y, hy)
            yvals.add(yvel_start)
            break


print("heighest", max_y)
print("min_y_vel, max_y_vel", min_y_vel, max_y_vel)
min_x_vel = 1000
max_x_vel = -1000
cnt = 0
for yvel_start in yvals:
    for xvel_start in range(-100, 1000):
        x = 0
        y = 0
        yvel = yvel_start
        xvel = xvel_start
        while y >= TARGET_MIN_Y:
            within_x = x >= TARGET_MIN_X and x <= TARGET_MAX_X
            within_y = y >= TARGET_MIN_Y and y <= TARGET_MAX_Y
            x += xvel
            y += yvel
            if xvel > 0:
                xvel -= 1
            if xvel < 0:
                xvel += 1
            yvel -= 1
            if within_y and within_x:
                #print(yvel_start, xvel_start)
                min_x_vel = min(min_x_vel, xvel_start)
                max_x_vel = max(max_x_vel, xvel_start)
                cnt += 1
                break

# not 419
print("min_x_vel, max_x_vel", min_x_vel, max_x_vel)
print("ANSWER", cnt)
