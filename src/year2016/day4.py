import sys
import re
import itertools
from lib.util import get_ints

input = sys.stdin
input = open('year2016/day4.in')

p = re.compile("([a-z-]*)([0-9]+)\[([a-z]+)\]")
sum = 0
for line in input.readlines():
    m = p.match(line.strip())
    (encrypted, id, checksum) = m.groups()

    cnt = [(k, len(list(l))) for k,l in itertools.groupby(sorted(encrypted)) if k != '-']
    cnt.sort(key=lambda x: x[1], reverse=True)
    expected = ''.join([x[0] for x in cnt][0:5])
    #print(checksum, expected)
    if checksum == expected:
        sum += int(id)
        s = ''
        for c in encrypted:
            if c == '-':
                s += ' '
            else:
                s += chr((ord(c)-97+int(id))%26+97)
        print(s, id)

print(sum)
