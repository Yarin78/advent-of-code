import sys
from collections import defaultdict

two_cnt = 0
three_cnt = 0
for line in sys.stdin.readlines():
    cnt = defaultdict(int)
    for i in range(0, len(line.strip())):
        cnt[ord(line[i])] += 1
    if any([x == 2 for x in cnt.values()]):
        two_cnt += 1
    if any([x == 3 for x in cnt.values()]):
        three_cnt += 1

print '%d %d => %d' % (two_cnt, three_cnt, two_cnt * three_cnt)
