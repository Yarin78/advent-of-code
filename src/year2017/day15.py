import sys
from collections import defaultdict
from lib import util
from queue import Queue
from aocd import data, submit

lines = data.split('\n')
a = util.get_ints(lines[0])[0]
b = util.get_ints(lines[1])[0]

#a = 65
#b = 8921

af = 16807
bf = 48271
MOD = 2147483647
cnt = 0

for i in range(5000000):
    a = a * af % MOD
    while a % 4 != 0:
        a = a * af % MOD
    b = b * bf % MOD
    while b % 8 != 0:
        b = b * bf % MOD
    if a & 65535 == b & 65535:
        cnt += 1
    if i % 100000 == 0:
        print(i)

print(cnt)

submit(cnt, part="b", day=15, year=2017)
