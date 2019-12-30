import sys
import re
import itertools
import hashlib
from collections import defaultdict
from lib.util import get_ints
from heapq import *
from lib.geo2d import *

dmap = {
    NORTH: (0, 'U'),
    SOUTH: (1, 'D'),
    WEST: (2, 'L'),
    EAST: (3, 'R')
}

q = []
heappush(q, (0, Point(0,0), ''))

salt = 'udskfozm'

while len(q) > 0:
    (dist, pos, walked) = heappop(q)

    #print('%2d: %s %s' % (dist, pos, walked))

    if pos == Point(3,3):
        print('%4d %s' % (len(walked), walked))
        continue
        break

    md5 = hashlib.md5()
    md5.update(bytes(salt + walked, 'ascii'))
    digest = md5.hexdigest()
    #print('digest = %s '% digest)

    for d in DIRECTIONS:
        #print(d)
        npos = pos + d
        (dig_no, dig_c) = dmap[d]

        if npos.x >= 0 and npos.y >= 0 and npos.x < 4 and npos.y < 4 and ord(digest[dig_no]) >= ord('b'):
            heappush(q, (dist+1, npos, walked + dig_c))
