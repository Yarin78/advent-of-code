import sys
from collections import defaultdict
from yal import util
from queue import Queue
from yal.geo2d import *
from intcode.intcode import Program
from aocd import data, submit

# Make sure AOC_SESSION is updated! (Chrome inspector -> Application tab -> session)

lines = data.strip().split('\n')
#prog = Program(data)
[a,b] = util.get_ints(lines[0])
b=-b
print(a,b)
cnt = 0
for i in range(a,b+1):
    s = str(i)
    adj = False
    nondec = True
    j = 0
    while j < len(s):
        k = j
        while k+1 < len(s) and s[j] == s[k+1]:
            k+=1
        if k-j == 1:
            adj = True
        j = k+1

    for j in range(len(s)-1):
        if s[j+1] < s[j]:
            nondec = False

    if adj and nondec:
        cnt += 1

print(cnt)
#submit(cnt, part="a", day=4, year=2019)
# submit(?, part="b", day=4, year=2019)
