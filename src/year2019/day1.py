import sys
from collections import defaultdict
from yal import util
from queue import Queue
from aocd import data, submit

lines = data.strip().split('\n')

mass = 0
for line in lines:
    fuel = int(line)
    extra = fuel // 3 - 2
    mass += extra
    while extra > 0:
        extra_fuel = extra // 3 - 2
        if extra_fuel >= 0:
            mass += extra_fuel
        extra = extra_fuel

#submit(mass, part="a", day=1, year=2019)
#submit(mass, part="b", day=1, year=2019)
