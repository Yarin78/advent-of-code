import sys
import re
import itertools
import hashlib
from collections import defaultdict
from lib.util import get_ints

def swap(pw, a, b):
    tmp = pw[a]
    pw[a] = pw[b]
    pw[b] = tmp

def reverse(pw, a, b):
    sub = pw[a:b+1]
    sub.reverse()
    pw = pw[:a] + sub + pw[b+1:]
    return pw


def scramble(pw, instructions):
    for line in instructions:
        parts = line.split(' ')

        if line.startswith('swap position'):
            swap(pw, int(parts[2]), int(parts[5]))
        elif line.startswith('swap letter'):
            swap(pw, pw.index(parts[2]), pw.index(parts[5]))
        elif line.startswith('reverse positions'):
            pw = reverse(pw, int(parts[2]), int(parts[4]))
        elif line.startswith('rotate left'):
            cnt = int(parts[2])
            pw = pw[cnt:] + pw[:cnt]
        elif line.startswith('rotate right'):
            cnt = int(parts[2])
            pw = pw[-cnt:] + pw[:-cnt]
        elif line.startswith('move position'):
            a = int(parts[2])
            b = int(parts[5])
            tmp = pw[a]
            pw = pw[:a] + pw[a+1:]
            pw = pw[:b] + [tmp] + pw[b:]
        elif line.startswith('rotate based'):
            let = parts[6]
            ix = pw.index(let)
            rot = (1+ix + (1 if ix >= 4 else 0)) % len(pw)
            pw = pw[-rot:] + pw[:-rot]
        else:
            raise Exception('oops')

    return ''.join(pw)


input = sys.stdin
input = open('year2016/day21.in')
#input = open('year2016/day21.sample.in')

instructions = [line.strip() for line in input.readlines()]

#print(scramble(list('abcdefgh'), instructions))

for perm in itertools.permutations(list('abcdefgh')):
    if scramble(list(perm), instructions) == 'fbgdceah':
        print(''.join(perm))

