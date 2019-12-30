import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from lib.util import *
from lib.graph import *
from lib.geo2d import *
from lib.intcode import *
from aocd import data, submit
from lib.mod_prime import *


lines = data.strip().split('\n')
lines.reverse()

# What card ends up in position pos after applying a single iteration of shuffling?
# We figure this out by applying the instructions in reverse, tracking only our card
def apply_shuffle_reverse(pos, n):
    global lines
    for line in lines:
        if line == "deal into new stack":
            pos = n-1-pos
        elif line.startswith("cut"):
            cut = int(line[4:])
            pos += cut
            if pos >= n:
                pos -= n
            elif pos < 0:
                pos += n
        else:
            assert line.startswith("deal with increment")
            incr = int(line[20:])
            j = pos
            # Could probably be done by some equation, but incr is thankfully always small
            while j % incr != 0:
                j += n
            pos = j // incr

    return pos


# The input
pos = 2020
m = 101741582076661
n = 119315717514047

# The evaluation of apply_shuffle_reverse will be in format
# X, X+Y, X+2*Y, X+3*Y, X+4*Y etc
# No idea why!
# Figure out X and Y (start & diff)

p1 = apply_shuffle_reverse(0, n)
p2 = apply_shuffle_reverse(1, n)

shuffle = {0: (p1, (p1-p2)%n)}

# Now, use the formula for applying one iteration twice to get the formula for two iterations
# Keep repeating to get all powers of two
# Then we can quickly apply the shuffling for an arbitrary number of iterations
# fast by looking at the bits

# Apply shuffling times number of iterations
def apply_shuffle_reverse_times(pos, n, times):
    power = 0
    while times > 0:
        if times % 2:
            (start, diff) = shuffle[power]
            pos = (start - diff*pos) % n

        power += 1
        times //= 2
    return pos

last_pos = 0
power = 1
while power < 100:
    # Apply formula twice to get start and diff for the next power of two
    for i in range(2):
        p = apply_shuffle_reverse_times(i, n, 2**(power-1))
        p = apply_shuffle_reverse_times(p, n, 2**(power-1))
        if i:
            diff = (last_pos-p) % n
        elif i == 0:
            start = p
        last_pos = p
    shuffle[power] = (start,diff)
    power += 1

print(apply_shuffle_reverse_times(pos, n, m))
