import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

lines = [line.strip() for line in sys.stdin.readlines()]

class Node:
    left: Optional["Node"]
    right: Optional["Node"]
    parent: Optional["Node"]
    literal: Optional[int]

    def is_leaf(self):
        return self.literal is not None

    def is_pair(self):
        return not self.is_leaf() and self.left.is_leaf() and self.right.is_leaf()

    def is_left_child(self):
        return self.parent is not None and self.parent.left == self

    def is_right_child(self):
        return self.parent is not None and self.parent.right == self

    def __init__(self, left, right, literal):
        self.left = left
        self.right = right
        self.literal = literal
        self.parent = None

    def __str__(self):
        if self.literal is not None:
            return str(self.literal)
        else:
            return '[%s,%s]' % (str(self.left), str(self.right))

    def __repr__(self):
        return str(self)

def parse(expr: str, pos: int=0) -> Tuple[Node, int]:
    if expr[pos] == '[':
        a, pos = parse(expr, pos+1)
        assert expr[pos] == ","
        b, pos = parse(expr, pos + 1)
        assert expr[pos] == "]"
        n = Node(a, b, None)
        a.parent = n
        b.parent = n
        return n, pos + 1
    else:
        value = int(expr[pos])
        return Node(None, None, value), pos +1


def next_node(node: Node):
    while node.is_right_child():
        node = node.parent
    if node.parent is None:
        return None  # there is no next node
    node = node.parent.right
    while node.left is not None:
        node = node.left
    return node

def previous_node(node: Node):
    while node.is_left_child():
        node = node.parent
    if node.parent is None:
        return None  # there is no previous node
    node = node.parent.left
    while node.right is not None:
        node = node.right
    return node


def explode(node: Node, depth: int):
    if node.is_pair() and depth >= 4:
        prev = previous_node(node)
        succ = next_node(node)
        if prev is not None:
            prev.literal += node.left.literal
        if succ is not None:
            succ.literal += node.right.literal
        new_node = Node(None, None, 0)
        new_node.parent = node.parent
        if node.is_left_child():
            node.parent.left = new_node
        else:
            assert node.is_right_child()
            node.parent.right = new_node
        return True
    elif not node.is_leaf():
        if explode(node.left, depth+1):
            return True
        return explode(node.right, depth+1)
    return False

def split(node: Node):
    if node.is_leaf():
        if node.literal >= 10:
            a = Node(None, None, node.literal // 2)
            b = Node(None, None, (node.literal+1) // 2)
            a.parent = node
            b.parent = node
            node.literal = None
            node.left = a
            node.right = b
            return True
        return False
    else:
        if split(node.left):
            return True
        return split(node.right)

def add(a: Node, b: Node):
    node = Node(a, b, None)
    a.parent = node
    b.parent = node

    while True:
        if explode(node, 0):
            continue
        if split(node):
            continue
        break
    return node

def magnitude(node: Node):
    if node.is_leaf():
        return node.literal
    return 3 * magnitude(node.left) + 2 * magnitude(node.right)

current = None

for line in lines:
    expr, _ = parse(line)
    if current is None:
        current = expr
    else:
        current = add(current, expr)

print(magnitude(current))

best = 0
for a in lines:
    for b in lines:
        if a == b:
            continue
        aexpr, _ = parse(a)
        bexpr, _ = parse(b)
        best = max(best, magnitude(add(aexpr,bexpr)))

print(best)
