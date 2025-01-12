import sys
from dataclasses import dataclass
from queue import Queue
from collections import defaultdict
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

MOD = 16777216

ans = 0
bananas = defaultdict(int)

for line in lines:
    b = {}

    secret = int(line)
    seq = [secret % 10]
    for i in range(2000):
        secret = secret ^ (secret * 64) % MOD
        secret = secret ^ (secret // 32) % MOD
        secret = secret ^ (secret * 2048) % MOD

        seq.append(secret % 10)
        if len(seq) >= 5:
            diff = (seq[1] - seq[0], seq[2] - seq[1], seq[3] -seq[2], seq[4] - seq[3])
            if diff not in b:
                b[diff] = seq[4]

            seq = seq[1:]

    for k, v in b.items():
        bananas[k] += v

print(max(bananas.values()))

