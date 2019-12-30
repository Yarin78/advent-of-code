import sys
import re
import itertools
from collections import defaultdict
from lib import util

input = sys.stdin
input = open('year2016/day9.in')
#input = open('year2016/day9.sample.in')

data = input.readline().strip()
data = data.replace(' ', '')

marker = re.compile(r"\(([0-9]+)x([0-9]+)\)")

def decompressed_length(data):
    global marker
    #print(data)
    m=marker.search(data)
    if not m:
        return len(data)
    (length,rep) = m.groups()
    replength = decompressed_length(data[m.end():m.end()+int(length)]) * int(rep)
    remaining = decompressed_length(data[m.end()+int(length):])
    return m.start() + replength + remaining

print(decompressed_length(data))
