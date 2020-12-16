import sys
from yal.util import *

lines = [line.strip() for line in sys.stdin.readlines()]
num_ranges = lines.index('')
ticket_line = lines.index('your ticket:') + 1

ranges = {}
for i in range(num_ranges):
    values = intify(tokenize(lines[i]))
    field = lines[i][0:lines[i].find(':')]
    ranges[field] = [(values[-5], values[-4]), (values[-2], values[-1])]

your_ticket = get_ints(lines[ticket_line])

poss = [set(ranges.keys()) for i in range(num_ranges)]

tickets = [get_ints(lines[i]) for i in range(ticket_line+3, len(lines))]

def candidate_fields(v):
    return set(name for name, r in ranges.items() if (v >= r[0][0] and v <= r[0][1]) or (v >= r[1][0] and v <= r[1][1]))

ans1 = 0
for ticket in [your_ticket, *tickets]:
    ans1 += sum(v for v in ticket if len(candidate_fields(v)) == 0)
    if all(len(candidate_fields(v)) > 0 for v in ticket):
        for k, v in enumerate(ticket):
            poss[k] = poss[k].intersection(candidate_fields(v))

ans2 = 1
fields_left = set(ranges.keys())
while len(fields_left) > 0:
    i = next(k for k in range(0, num_ranges) if len(poss[k].intersection(fields_left)) == 1)
    field = list(poss[i].intersection(fields_left))[0]
    fields_left.remove(field)
    if field.startswith('departure'):
        ans2 *= your_ticket[i]

print(ans1, ans2)
