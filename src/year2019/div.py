
def div(a, b):
    #if b == 1:
    #    return a
    lo = 1
    powers = [1]
    while powers[-1] < a:
        powers.append(powers[-1]*2)
    ptr = len(powers)-1
    while ptr >= 0:
        x = lo+powers[ptr]
        ptr -= 1
        if not (a < b*x):
            lo = x

    return lo

for a in range(0, 100):
    for b in range(1, a+1):
        assert div(a,b) == a//b, '%d/%d = %d, expected %d' % (a, b, div(a,b), a//b)
