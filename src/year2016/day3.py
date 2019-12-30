import sys
from lib.util import get_ints

input = sys.stdin
input = open('year2016/day3.in')

cnt = 0
lines = [get_ints(line) for line in input.readlines()]
for i in range(0, len(lines), 3):
    for j in range(3):
        (a,b,c) = (lines[i][j], lines[i+1][j], lines[i+2][j])
        #print(a,b,c)
        if a+b > c and a+c > b and b+c > a:
            cnt += 1

print(cnt)
