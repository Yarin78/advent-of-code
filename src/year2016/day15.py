import sys
import re
import itertools
import hashlib
from collections import defaultdict
from lib.util import get_ints

#discs = [(17,15), (3, 2), (19, 4), (13, 2), (7, 2), (5, 0)]
discs = [(17,15), (3, 2), (19, 4), (13, 2), (7, 2), (5, 0), (11,0)]
#discs = [(5, 4), (2, 1)]

for i in range(len(discs)):
    (cnt, cur) = discs[i]
    discs[i] = (cnt, (cur+i+1) % cnt)

print(discs)
tm = 0
while True:
    ok = True
    for (cnt, cur) in discs:
        if (cur + tm) % cnt != 0:
            ok = False
    if ok:
        print('Ok in time %d' % tm)
        break
    tm += 1
