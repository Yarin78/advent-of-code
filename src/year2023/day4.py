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

part1 = 0
part2 = 0

card_count = defaultdict(lambda: 1)
card_count[1] = 1

for line in lines:
    l1, l2 = line.split(':')
    card_no = get_ints(l1)[0]
    l3, l4 = l2.split('|')
    winning_cards = get_ints(l3)
    your_cards = set(get_ints(l4))

    matches = 0
    for c in winning_cards:
        if c in your_cards:
            matches += 1
    for i in range(matches):
        card_count[card_no+i+1] += card_count[card_no]

    if matches:
        part1 += 2**(matches - 1)
    part2 += card_count[card_no]

print(part1)
print(part2)
