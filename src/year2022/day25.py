import sys

digits = "=-012"

def conv(s):
    global digits
    val = 0
    for c in s:
        val = val * 5 + digits.find(c) - 2
    return val

tot = 0
for line in sys.stdin.readlines():
    tot += conv(line.strip())

lo = 0
hi = 999999999999999999
while lo < hi:
    x = (lo+hi) // 2
    y = x
    s = ""
    while y:
        s = digits[y%5] + s
        y = y //5
    cs = conv(s)
    if cs < tot:
        lo = x+1
    elif cs > tot:
        hi = x
    else:
        print(s.lstrip('0'))
        hi = x
    