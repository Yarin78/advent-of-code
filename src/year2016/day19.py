import sys
import re
import itertools
import hashlib
from collections import defaultdict
from lib.util import get_ints

def josephus(n, k):
    # Returns value 1-indexed
    d = 1
    while (d <= (k - 1) * n):
        d = (k * d + k - 2) // (k - 1)
    return k * n + 1 - d

#print(josephus(3014603, 2))

class Node:
    def __init__(self, index):
        self.index = index


NODES = 3014603

nodes = []
for i in range(NODES):
    nodes.append(Node(i+1))

for i in range(NODES):
    nodes[i].prev = nodes[(i+NODES-1) % NODES]
    nodes[i].next = nodes[(i+1) % NODES]

left = NODES
current = nodes[NODES//2]
while left > 1:
    #print('Removing elf %d' % current.index)
    current.prev.next = current.next
    current.next.prev = current.prev
    if left % 2 == 0:
        current = current.next
    else:
        current = current.next.next
    left -= 1

print('Last one: %d' % current.index)
