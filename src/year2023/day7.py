import sys
from queue import Queue
from collections import Counter, defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

# Make sure ~/.config/aocd/token is correct! (Application tab -> Cookies)
# scanner = Scanner(sys.stdin)
lines = [line.strip() for line in sys.stdin.readlines()]
# Split input into an array of array of lines, split by empty line
# sections = split_lines(lines)

def card_val(c: str):
    if c == 'A':
        return 14
    if c == 'K':
        return 13
    if c == 'Q':
        return 12
    if c == 'J':
        return 1
    if c == 'T':
        return 10
    return ord(c) - 48

def score_hand(hand: str, org_hand: str):
    d = defaultdict(int)
    card_vals = tuple((card_val(c) for c in hand))
    org_card_vals = tuple((card_val(c) for c in org_hand))

    for c in hand:
        d[card_val(c)] += 1
    # max_count, cv_max = dict_max_value(d)
    # min_count, cv_min = dict_min_value(d)
    freq_cnt = defaultdict(int)
    for k, v in d.items():
        freq_cnt[v] += 1

    if freq_cnt[5] == 1:
        return (10, org_card_vals)
    if freq_cnt[4] == 1:
        return (9, org_card_vals)
    if freq_cnt[3] == 1 and freq_cnt[2] == 1:
        return (8, org_card_vals)
    if freq_cnt[3] == 1:
        return (7, org_card_vals)
    if freq_cnt[2] == 2:
        return (6, org_card_vals)
    if freq_cnt[2] == 1:
        return (5, org_card_vals)

    return (1, org_card_vals)

def replace_jokers(cur: str, hand: str, i: int, hands: List[str]):
    if i == 5:
        hands.append(cur)
        return
    if hand[i] != 'J':
        replace_jokers(cur + hand[i], hand, i+1, hands)
    else:
        for c in '23456789TQKA':
            replace_jokers(cur + c, hand, i+1, hands)


poker_hands = []
for line in lines:
    org_hand, value_str = line.split(' ')
    value = int(value_str)

    possible_hands = []
    replace_jokers("", org_hand, 0, possible_hands)

    # if len(possible_hands) > 1:
    #     print(possible_hands)

    best_joker_hands = [(score_hand(hand, org_hand), hand, value) for hand in possible_hands]
    best_joker_hands.sort()
    best_hand = best_joker_hands[-1]

    print(org_hand, best_hand)

    # poker_hands.append((score_hand(hand), hand, value))
    poker_hands.append(best_hand)



poker_hands.sort(reverse=False)

part1 = 0
for rank, (score, hand, value) in enumerate(poker_hands):
    print(f"{rank+1}: {score} {hand}")
    part1 += (rank+1) * value

print(part1)


# Not 253570697

# Not 253254392

253253225