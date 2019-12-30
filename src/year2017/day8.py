import sys
from collections import defaultdict

regs = defaultdict(int)

def condition(reg, op, value):
    return eval('%s %s %s' % (regs[reg], op, value))

most = 0
for line in sys.stdin.readlines():
    parts = line.strip().split(' ')
    if condition(parts[4], parts[5], parts[6]):
        sign = 1 if parts[1] == 'inc' else -1
        regs[parts[0]] += sign * int(parts[2])
    most = max(most, int(max(regs.values())))


print(max(regs.values()))
print(most)
