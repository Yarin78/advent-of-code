import sys
from lib import util
from collections import defaultdict

val = defaultdict(lambda: defaultdict(int))
cur = 2
circuit = 1
val[0][0] = 1
while True:
    i = 0
    while cur <= (circuit*2+1)*(circuit*2+1):
        side_len = circuit * 2
        x = -1
        y = -1
        if i < side_len:
            x = circuit
            y = -circuit + 1 + i
        elif i < 2*side_len:
            x = circuit - i + side_len - 1
            y = circuit
        elif i < 3*side_len:
            x = -circuit
            y = circuit - (i - 2*side_len) - 1
        else:
            x = -circuit + i - side_len*3 + 1
            y = -circuit

        #if cur == 361527:
        #    print('dist =', abs(x)+abs(y))
        #    exit(0)
        value = 0
        for dx in range(-1,2):
            for dy in range(-1,2):
                value += val[y+dy][x+dx]
        val[y][x] = value
        # print(val[y][x])
        if value > 361527:
            print(value)
            exit(0)


        cur += 1
        i += 1

    circuit += 1
