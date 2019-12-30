import sys
from lib import util

#parts=map(lambda x: int(x), sys.stdin.readline().strip().split(','))
parts=[]
for c in sys.stdin.readline().strip():
    parts.append(ord(c))
parts.extend([17,31,73,47,23])

c = list(range(256))
pos = 0
skip_size = 0
n = len(c)
for r in range(64):
    for x in parts:
        nc = c[:]
        for i in range(x):
            nc[(pos+i)%n] = c[(pos+x-i-1)%n]
        pos += x + skip_size
        skip_size += 1
        c = nc

print(c[0] * c[1])
res = ''
for b in range(16):
    x = 0
    for i in range(16):
        x ^= c[b*16+i]
    res += '%02x' % x
print(res)
