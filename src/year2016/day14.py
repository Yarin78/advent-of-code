import sys
import re
import itertools
import hashlib
from collections import defaultdict
from lib.util import get_ints

salt = 'ihaygndm'
#salt = 'abc'
hex = '0123456789abcdef'

keys = []
five_count = [[0] for i in range(16)]
digests = []
# five_count[digit][index] = number of hashes in range [0,index) containing the specified digit 5 times in a row

i = 0
while len(keys) < 64:
    digest = salt + str(i)
    for j in range(2017):
        md5 = hashlib.md5()
        md5.update(bytes(digest, encoding='ascii'))
        digest = md5.hexdigest()

    digests.append(digest)

    for digit in range(16):
        if digest.find(hex[digit] * 5) >= 0:
            five_count[digit].append(five_count[digit][-1] + 1)
        else:
            five_count[digit].append(five_count[digit][-1])

    if i >= 1000:
        digest = digests[i-1000]
        digit = -1
        for j in range(len(digest)-2):
            if digest[j] == digest[j+1] and digest[j] == digest[j+2]:
                digit = hex.find(digest[j])
                break

        if digit >= 0:
            #print('Triple %s found at index %d' % (hex[digit] * 3, i - 1000))
            if five_count[digit][i+1] - five_count[digit][i-999] > 0:
                keys.append(i - 1000)
                print('%d keys found (%d)' % (len(keys), i - 1000))

    i += 1
