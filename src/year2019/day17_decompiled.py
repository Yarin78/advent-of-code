import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from lib.util import *
from lib.graph import *
from lib.geo2d import *
from lib.intcode import *
from aocd import data, submit
from day17_generated import DecompiledProgram

lines = data.strip().split('\n')
prog = DecompiledProgram()
prog.init_io(Queue(), Queue())
t = prog.start_async()

m = []
s = prog.read_line()
while s:
    for x in range(len(s)):
        if s[x] not in '#.':
            start = Point(x,len(m))
    m.append(s)
    s = prog.read_line()

summa = 0
ysize = len(m)
xsize = len(m[0])

print(xsize, ysize)
for y in range(ysize):
    for x in range(xsize):
        if x > 0 and y > 0 and x+1<xsize and y+1<ysize:
            p=Point(x,y)
            c = 1 if m[y][x] == '#' else 0
            for d in DIRECTIONS:
                np=p+d
                e = 1 if m[np.y][np.x] == '#' else 0
                c += e
            if c == 5:
                summa += x*y

print(summa)

output='R'
dirno=1
cur = start
cnt=0
while True:
    np = cur+DIRECTIONS[dirno]
    c = '.'
    if np.x >= 0 and np.y >= 0 and np.x<xsize and np.y<ysize:
        c = m[np.y][np.x]
    if c == '#':
        cur = np
        cnt += 1
    else:
        output+='.%d' % cnt
        cnt = 0
        np = cur+DIRECTIONS[(dirno+1)%4]
        if np.x >= 0 and np.y >= 0 and np.x<xsize and np.y<ysize and m[np.y][np.x] == '#':
            output+=',R'
            dirno = (dirno+1)%4
        else:
            np = cur+DIRECTIONS[(dirno+3)%4]
            if np.x >= 0 and np.y >= 0 and np.x<xsize and np.y<ysize and m[np.y][np.x] == '#':
                output+=',L'
                dirno = (dirno+3)%4
            else:
                print('Stopping at %d,%d' % (cur.x, cur.y))
                break

solution = output.split(',')
for alen in range(1,10):
    for blen in range(1,10):
        for clen in range(1,10):
            a = solution[0:alen]
            b = None
            c = None
            p = 'A'
            cur = alen
            fail = False
            while cur < len(solution) and not fail:
                if solution[cur:cur+alen] == a:
                    cur += alen
                    p += ',A'
                elif b and solution[cur:cur+blen] == b:
                    cur += blen
                    p += ',B'
                elif c and solution[cur:cur+clen] == c:
                    cur += clen
                    p += ',C'
                elif not b:
                    b = solution[cur:cur+blen]
                    cur += blen
                    p += ',B'
                elif not c:
                    c = solution[cur:cur+clen]
                    cur += clen
                    p += ',C'
                else:
                    fail = True
            if not fail:
                cand = [p,','.join(a).replace('.',','),','.join(b).replace('.',','),','.join(c).replace('.',','),"n"]
                for c in cand:
                    if len(c) > 20:
                        fail = True
                if not fail:
                    data = cand
                    print(data)


for line in data:
    prog.write_line(line)
try:
    while t.is_alive() or not prog._output.empty():
        print(prog.read_line())
except MachineHaltedException:
    pass

t.join()
