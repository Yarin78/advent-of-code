import sys

data = [int(x) for x in sys.stdin.readlines()]

for i in range(25, len(data)):
    if data[i] not in [data[j] + data[k] for j in range(i-25, i) for k in range(i-25, j)]:
        needle = data[i]
        break

print(needle)

partial_sums = [0]
for i in range(len(data)):
    partial_sums.append(partial_sums[i] + data[i])

for i in range(len(data)):
    lo = i+2
    hi = len(partial_sums) + 1
    while lo < hi:
        x = (lo+hi)//2
        diff = partial_sums[x] - partial_sums[i]
        if diff < needle:
            lo = x + 1
        elif diff > needle:
            hi = x
        else:
            print(min(data[i:x]) + max(data[i:x]))
            exit(0)
