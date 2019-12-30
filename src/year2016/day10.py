import sys
import re
import itertools
from collections import defaultdict
from lib.util import get_ints

input = sys.stdin
input = open('year2016/day10.in')
#input = open('year2016/day10.sample.in')

bots = defaultdict(list) # id -> list
bot_instr = {}
output = {}

for line in input.readlines():
    data = get_ints(line)
    if line.startswith('value'):
        bots[data[1]].append(data[0])
    else:
        c1 = line[line.index('low to')+7][0]
        c2 = line[line.index('high to')+8][0]
        bot_instr[data[0]] = ((c1,data[1]), (c2,data[2]))

while True:
    actions = [id for id,contents in bots.items() if len(contents) == 2]
    if not len(actions):
        break
    for id in actions:
        contents = bots[id]
        lo = min(contents[0], contents[1])
        hi = max(contents[0], contents[1])
        if lo == 17 and hi == 61:
            print('BOT ID %d' % id)
        ((c1, t1), (c2,t2)) = bot_instr[id]
        print('bot %d gives %d to %c%d and %d to %c%d' % (id, lo, c1, t1, hi, c2, t2))
        if c1 == 'b':
            bots[t1].append(lo)
        else:
            output[t1] = lo
        if c2 == 'b':
            bots[t2].append(hi)
        else:
            output[t2] = hi
        bots[id] = []

print(output[0]*output[1]*output[2])
