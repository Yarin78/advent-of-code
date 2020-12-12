import sys
a = sorted(int(s) for s in sys.stdin)
p = [c-b for b, c in zip([0, *a], [*a, max(a)+3])]
c = {0:1}
for i in [*a, max(a)+3]:
    c[i] = sum(c[j] if i-4 < j < i else 0 for j in [0, *a])
print(p.count(1)*p.count(3), max(c.values()))
