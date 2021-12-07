d = list(sorted(map(int, input().split(','))))

def cost1(pos):
    return sum(abs(y-pos) for y in d)

def cost2(pos):
    return sum(abs(y-pos)*(abs(y-pos)+1)//2 for y in d)

n = len(d)
pos = (d[n//2] + d[n//2-1])//2
print(cost1(pos))

best = 999999999999
lo = 0
hi = max(d)
while lo <= hi:
    x1 = lo+(hi-lo)//3
    x2 = lo+(hi-lo)//3*2
    best = min(best, cost2(x1), cost2(x2))
    if cost2(x1) < cost2(x2):
        hi = x2
    else:
        lo = x1+1

print(best)
