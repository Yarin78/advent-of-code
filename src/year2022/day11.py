import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *
from dataclasses import dataclass

lines = [line.strip() for line in sys.stdin.readlines()]
# Split input into an array of array of lines, split by empty line
sections = split_lines(lines)

@dataclass
class Monkey:
    items: List[int]
    op: str
    op_val: str
    test: int
    true_monkey: int
    false_monkey: int
    inspects: int

monkeys = []
for lines in sections:
    ix = get_ints(lines[0])[0]
    items = get_ints(lines[1])
    op = lines[2].split(' ')
    div=get_ints(lines[3])[0]
    m1=get_ints(lines[4])[0]
    m2=get_ints(lines[5])[0]

    monkeys.append(Monkey(items, op[-2], op[-1], div, m1, m2, 0))

MOD = 1
for m in monkeys:
    print(m)
    MOD *= m.test

round = 0
n = len(monkeys)
while round < 10000:
    for i in range(n):
        m: Monkey = monkeys[i]
        m.inspects += len(m.items)
        for j in range(len(m.items)):
            w = m.items[j]

            assert is_int(m.op_val ) or m.op_val=="old"
            assert m.true_monkey != i and m.false_monkey != i

            if m.op == '+':
                w += int(m.op_val) if is_int(m.op_val) else w
            elif m.op == '*':
                w *= int(m.op_val) if is_int(m.op_val) else w
            else:
                assert False
            # w //= 3  # part 1
            w %= MOD

            target = m.true_monkey if w % m.test == 0 else m.false_monkey
            monkeys[target].items.append(w)

        m.items = []

    round += 1

    if round % 1000 == 0:
        for i, m in enumerate(monkeys):
            print(f"Monkey {i}: {str(m.items)}")
        print()

monkeys.sort(key = lambda m: m.inspects, reverse=True)
print(monkeys[0].inspects*monkeys[1].inspects)
