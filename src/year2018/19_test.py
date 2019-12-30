C = 1030
C = 10551430
factors = []
p = 2
Q = C
while p <= Q:
    if Q % p == 0:
        factors.append(p)
        Q /= p
    else:
        p += 1
if Q > 1:
    factors.append(Q)

print factors


2 * 5 * 1055143

2 * (5*1055143)
(2*5) * 1055143
(2*1055143) * 5

2
10
206
515
103
5
1
1030
