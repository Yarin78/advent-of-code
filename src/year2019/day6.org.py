import sys
from collections import defaultdict
from lib import util
from queue import Queue
from lib.geo2d import *
from lib.intcode import *
from aocd import data, submit

# Make sure AOC_SESSION is updated! (Chrome inspector -> Application tab -> session)


lines = data.strip().split('\n')

parent = {}
children = {}
for line in lines:
    [a,b] = line.split(')')
    parent[b] = a
    if a not in children:
        children[a] = []
    children[a].append(b)

tot_count = 0

def traverse(cur, depth):
    global tot_count
    tot_count += depth
    if cur in children:
        for c in children[cur]:
            traverse(c, depth+1)

traverse('COM', 0)


#prog = intcode.Program(data)
print(tot_count)
# submit(?, part="a", day=6, year=2019)
# submit(?, part="b", day=6, year=2019)

def chain(cur, l):
    l.append(cur)
    if cur in parent:
        chain(parent[cur], l)

yc=[]
sc=[]
chain('YOU', yc)
chain('SAN', sc)

dist={}
c=0
for y in yc:
    dist[y] = c
    c += 1

c = 0
for s in sc:
    if s in dist:
        print(dist[s] + c - 2)
        exit()
    c += 1


