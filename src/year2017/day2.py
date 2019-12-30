import sys
from lib import util

sum1 = 0
sum2 = 0
for line in sys.stdin.readlines():
    v = util.get_ints(line)
    sum1 += max(v) - min(v)
    for i in range(len(v)):
        for j in range(len(v)):
            if i != j and v[i] % v[j] == 0:
                sum2 += v[i]/v[j]
print(sum1)
print(sum2)
