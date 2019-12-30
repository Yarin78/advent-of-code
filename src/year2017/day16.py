import sys
from collections import defaultdict
from lib import util
from queue import Queue
from aocd import data, submit

# data='''
# s1
# x3/4
# pe/b
# '''


lines = data.strip().split(',')
s = 'abcdefghijklmnop'
perm = list(range(len(s)))

for dances in range(10):
    for line in lines:
        if line[0] == 's':
            x = int(line[1:])
            s = s[len(s)-x:] + s[:len(s)-x]
            if dances == 0:
                perm = perm[len(perm)-x:] + perm[:len(perm)-x]
        elif line[0] == 'x':
            [p,q] = util.get_ints(line)
            if p > q:
                tmp = p
                p = q
                q = tmp
            s = s[0:p] + s[q] + s[p+1:q] + s[p] + s[q+1:]
            if dances == 0:
                perm = perm[0:p] + [perm[q]] + perm[p+1:q] + [perm[p]] + perm[q+1:]
        elif line[0] == 'p':
            x = line[1]
            y = line[3]
            s = s.replace(x, 'X').replace(y, x).replace('X', y)
    print('dance %d: %s' % (dances+1, s))
    #if dances == 0:
    #    perm = [ord(c) - 97 for c in s]

def apply_perm(p, pp):
    q = [-1] * len(p)
    for i in range(len(q)):
        q[i] = p[pp[i]]
        #q.append(pp[p[i]])
    return q

def conv(p):
    return ''.join([chr(c+97) for c in p])

p = apply_perm(perm, perm)
q = apply_perm(p, p)

#print(conv(perm))
#print(conv(p))
#print(conv(q))
print(perm)
print(p)

#submit(s, part="a", day=16, year=2017)
