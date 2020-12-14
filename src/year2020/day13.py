import sys
from yal.math import chinese_remainder

lines = [line.strip() for line in sys.stdin.readlines()]
d = {int(s): (int(s)-num) % int(s) for num, s in enumerate(lines[1].split(',')) if s != 'x'}
print(chinese_remainder(list(d.keys()), list(d.values())))
