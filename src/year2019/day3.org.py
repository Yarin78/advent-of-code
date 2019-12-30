import sys
from collections import defaultdict
from lib import util, intcode, geo2d
from lib.geo2d import Point
from queue import Queue
from aocd import data, submit

#data = '''R75,D30,R83,U83,L12,D49,R71,U7,L72
#U62,R66,U55,R34,D71,R55,D58,R83'''

#data = '''R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
#U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'''

lines = data.strip().split('\n')
#prog = intcode.Program(data)

m = {}
steps = [{}, {}]
closest = None
best = 999999999

for line_no in range(2):
    line = lines[line_no]
    v=line.split(',')
    cur = Point(0,0)
    t = 0
    #print()
    for si in range(len(v)):
        s = v[si]
        #print(s)

        d = s[0]
        leng = int(s[1:])
        if d == 'R':
            delta = Point(1,0)
        elif d == 'U':
            delta = Point(0,-1)
        elif d == 'L':
            delta = Point(-1,0)
        else:
            delta = Point(0,1)
        for i in range(leng):
            cur.x += delta.x
            cur.y += delta.y
            t += 1
            if (cur.x, cur.y) not in steps[line_no]:
                steps[line_no][(cur.x, cur.y)] = t

            #print(cur.x, cur.y)
            if  si < len(v)-1 or i < leng -1:
                if line_no == 1 and (cur.x, cur.y) in m and m[(cur.x, cur.y)] == 1:
                    dist = abs(cur.x)+abs(cur.y)
                    #print('crossing at %d, %d' % (cur.x, cur.y))
                    if closest is None or dist < closest:
                        closest = dist
                    best = min(best, steps[0][(cur.x, cur.y)] + steps[1][(cur.x, cur.y)])

            m[(cur.x, cur.y)] = line_no+1
    #break

print(closest)
print(best)
#print(m[Point(3,-3)])
#print(m)

submit(best, part="b", day=3, year=2019)
