import sys
import re
import itertools
import hashlib
from collections import defaultdict
from lib.util import get_ints

def checksum(data):
    while len(data) % 2 == 0:
        s = ''
        for i in range(0, len(data), 2):
            s = s + ('1' if data[i] == data[i+1] else '0')
        data = s
    return data


#state = '10000'
#disk_size = 20

state = '00111101111101000'
disk_size = 35651584

while len(state) < disk_size:
    cpy = list(state)
    cpy.reverse()
    cpy = ['1' if x == '0' else '0' for x in cpy]
    state = state + '0' + ''.join(cpy)

#print(state)

state = state[0:disk_size]
print(checksum(state))
