import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from aocd import data, submit

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
lines = data.strip().split('\n')

#with open("day7-sample.in", "r") as f:
#    lines = f.readlines()
# intlines = [int(x) for x in lines]
ans = ans2 = 0
g = {}
for line in lines:
    line = line.strip()
    parts = line.split(' contain ')
    parent = parts[0]
    parent = parent.replace("bags", "")
    parent = parent.strip()
    children = parts[1].split(", ")
    ch = []
    for child in children:
        if child == "no other bags.":
            continue
        parts = child.split(' ', 1)
        cnt = int(parts[0])
        v=parts[1]
        v = v.replace("bags.", "")
        v = v.replace("bag.", "")
        v = v.replace("bags", "")
        v = v.replace("bag", "")
        v = v.strip()

        #print(cnt, v)
        #if v == "shiny gold":
        #    print(line)
        ch.append((cnt, v))
    g[parent] = ch
    #print(children)

def expand(current, has):
    has.add(current)
    for (k, v) in g[current]:
        expand(v, has)

print(g)

# for k in g.keys():
#     if k=="shiny gold":
#         continue
#     has=set()
#     expand(k, has)
#     if "shiny gold" in has:
#         print(k)
#         ans += 1

bag_cnt = defaultdict(int)

def expand2(mult, current):
    bag_cnt[current] += mult
    for (k,v) in g[current]:
        expand2(mult * k, v)


expand2(1, "shiny gold")

print(bag_cnt)
print(sum(bag_cnt.values())-1)
# print(ans)
# submit(ans, part="a", day=7, year=2020)
# submit(ans2, part="b", day=7, year=2020)
