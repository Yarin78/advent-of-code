import sys
from functools import lru_cache

r, m = sys.stdin.read().split('\n\n')
a = {int(line.split(':')[0]): line[-2] if '"' in line else [list(map(int, s.strip().split(' '))) for s in line.split(':')[1].split('|')] for line in r.split('\n')}

@lru_cache(maxsize=None)
def match(n, msg, p=0, q=0):
    return msg == a[n] if isinstance(a[n], str) else False if p >= len(a[n]) else not msg if q == len(a[n][p]) else not q and match(n, msg, p+1, 0) or any(match(a[n][p][q], msg[:i]) and match(n, msg[i:], p, q+1) for i in range(len(msg)+1))

print(sum(match(0, s) for s in m.split()))
print(match.cache_info())
