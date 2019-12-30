import sys
from collections import defaultdict
from lib import util
from queue import Queue
from aocd import data, submit

lines = data.strip().split('\n')

# submit(cnt, part="a", day=15, year=2017)

class Node:
    def __init__(self, value):
        self.value = value


cur = Node(0)
cur.next = cur
for i in range(50000000):
    for j in range(301):
        cur = cur.next
    t = Node(i+1)
    t.next = cur.next
    cur.next = t
    cur = t
    if i % 1000000 == 0:
        print(i)

while cur.value:
    cur = cur.next

print(cur.next.value)

