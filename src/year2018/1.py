import sys

seen = set()

total = 0
delta = map(lambda x: int(x.strip()), sys.stdin.readlines())

while True:
    for d in delta:
        if total in seen:
            print total
            exit(0)
        seen.add(total)
        total += d
