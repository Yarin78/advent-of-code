import sys
from collections import defaultdict
from queue import Queue
from yal.tree import Tree
from aocd import data, submit

# Cleaned up version; see day6.org.py for hacky submitted version

lines = data.strip().split('\n')

tree = Tree([line.split(')') for line in lines])

print(sum(tree.depth[c] for c in tree.children.keys()))

a1 = tree.all_ancestors('YOU')
a2 = tree.all_ancestors('SAN')

print(min([a1.index(c) + a2.index(c) for c in a1 if c in a2]))
