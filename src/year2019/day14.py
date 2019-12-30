import math
import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from aocd import data, submit

lines = data.strip().split('\n')

req = {}  # Complete list of dependencies and quantities required to produce each chemical
g = {}    # Dependency graph
for line in lines:
    reaction = pair_up(intify(tokenize(line)))
    deps, (target_quant, target_id) = reaction[0:-1], reaction[-1]

    req[target_id] = (target_quant, deps)
    g[target_id] = [dep[1] for dep in deps]

order = topological_sort(g)
order.reverse()  # Process the reactions in backward order

def ore_required(fuel_demand):
    global order, req
    demand = defaultdict(int)
    demand['FUEL'] = fuel_demand
    for id in order:
        if id == 'ORE':
            return demand[id]
        (quant, deps) = req[id]
        required_amount = int(math.ceil(demand[id] / quant))
        #print('need %d %s, must produce %d times receipt %s' % (hm[output], output, a, req[output]))
        for (dep_quant, dep_id) in deps:
            demand[dep_id] += dep_quant*required_amount

print(ore_required(1))

target = 1000000000000
lo = 0
hi = target
while lo < hi:
    x = (lo+hi)//2
    if ore_required(x) > target:
        hi = x
    else:
        lo = x+1

print(lo-1)
