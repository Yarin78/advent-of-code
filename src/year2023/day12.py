import sys
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *
from functools import cache

lines = [line.strip() for line in sys.stdin.readlines()]

pattern = ""
groups = []

# cur_group_size = 0 still in a damager group
# cur_group_size = -1 last was '.'
@cache
def count_conditions(pos, cur_group_size, next_group_ix):
    global pattern, groups
    if pos == len(pattern):
        return cur_group_size <= 0 and next_group_ix == len(groups)

    cnt = 0
    for c in ('.', '#'):
        if pattern[pos] == '?' or pattern[pos] == c:
            if c == '.':
                if cur_group_size <= 0:
                    cnt += count_conditions(pos+1, -1, next_group_ix)
            else:
                if cur_group_size > 0:
                    cnt += count_conditions(pos+1, cur_group_size-1, next_group_ix)
                elif cur_group_size < 0 and next_group_ix < len(groups):
                    cnt += count_conditions(pos+1, groups[next_group_ix]-1, next_group_ix+1)

    return cnt

part1 = 0
part2 = 0
for line in lines:
    pattern, counts = line.split(' ')
    groups = get_ints(counts)

    count_conditions.cache_clear()
    part1 += count_conditions(0, -1, 0)

    pattern = f"{pattern}?{pattern}?{pattern}?{pattern}?{pattern}"
    groups = [*groups, *groups, *groups, *groups, *groups]

    count_conditions.cache_clear()
    part2 += count_conditions(0, -1, 0)

print(part1)
print(part2)
