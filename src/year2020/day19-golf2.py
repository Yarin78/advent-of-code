import sys
from itertools import combinations
from functools import lru_cache

r, m = sys.stdin.read().split('\n\n')
a = {int(line.split(':')[0]): line[-2] if '"' in line else [list(map(int, s.strip().split(' '))) for s in line.split(':')[1].split('|')] for line in r.split('\n')}

@lru_cache(maxsize=None)
def match(n, msg):
    return msg == a[n] if isinstance(a[n], str) else any(all(match(x, msg[c[i-1] if i else 0:c[i] if i<len(c) else len(msg)]) for i, x in enumerate(rule)) for rule in a[n] for c in combinations(range(len(msg)+1), len(rule)-1))

print(sum(match(0, s) for s in m.split()))
print(match.cache_info())
