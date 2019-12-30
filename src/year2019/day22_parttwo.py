import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from intcode.intcode import *
from aocd import data, submit
from yal.mod_prime import *

lines = data.strip().split('\n')

# The input
pos = 2020
m = 101741582076661
n = 119315717514047

# all operations are on the formula ax+b, represented as a tuple (a,b)

def combine(op1, op2):
    (a1, b1) = op1
    (a2, b2) = op2
    return (a1*a2%n, (b1*a2+b2)%n)

def apply(op, x):
    (a, b) = op
    return (a*x+b) % n

def inverse(op):
    (a, b) = op
    c = calc_inverse(a, n)
    d = -b*c%n
    return (c,d)

shuffle = (1,0)
for line in lines:
    ints = get_ints(line)
    if not ints:
        op = (-1, n-1)  # new stack
    elif 'cut' in line:
        op = (1, -ints[0])  # cut
    else:
        op = (ints[0], 0)  # increment

    shuffle = combine(shuffle, op)

power_shuffle = inverse(shuffle)
cur = (1,0)

while m:
    if m % 2:
        cur = combine(cur, power_shuffle)
    m //= 2
    power_shuffle = combine(power_shuffle, power_shuffle)

print(apply(cur, pos))
