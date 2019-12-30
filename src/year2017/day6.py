import sys
from lib import util

data = util.get_ints(sys.stdin.readline())
seen = {}
cnt = 0
while str(data) not in seen:
    seen[str(data)] = cnt
    cnt += 1
    x = data.index(max(data))
    y = data[x]
    data[x] = 0
    for i in range(y):
        data[(x+i+1) % len(data)] += 1

print(cnt)
print(cnt - seen[str(data)])

