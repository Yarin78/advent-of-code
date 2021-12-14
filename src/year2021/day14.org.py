import sys
from queue import Queue
from collections import defaultdict
from itertools import combinations, permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
# scanner = Scanner(sys.stdin)
lines = [line.strip() for line in sys.stdin.readlines()]

cur = lines[0]

mapper = {}
for line in lines[2:]:
    a, b = tokenize(line)
    #s = "" + a[0] + b[0] + a[1]
    s = "" + a[1] + b[0] + a[0]
    t = "" + a[1] + a[0]
    mapper[t] = s

print(mapper)

cur = cur[::-1]

def get_count(cur):
    cnt = defaultdict(int)
    for d in cur:
        cnt[d] += 1

    return list(sorted([(v, k) for k,v in cnt.items()]))

steps = 0
while steps < 10:
    #print(cur[::-1])
    #print(len(cur), get_count(cur))

    steps += 1

    i = 0
    build = ""
    while i+1 < len(cur):
        s = cur[i] + cur[i+1]
        #print("->", s)
        if s in mapper:
            build += mapper[s][:2]
        else:
            build += s[0]
        i += 1
    build += cur[i]

    cur = build

print(cur[::-1])

cnt2 = get_count(cur)
print(cnt2)

print(cnt2[-1][0] - cnt2[0][0])


