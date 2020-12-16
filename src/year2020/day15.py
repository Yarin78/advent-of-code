import sys

data = [int(s) for s in sys.stdin.read().split(',')]

def solve(n):
    last = {}
    for i in range(n):
        num = data[i] if i < len(data) else next_num
        next_num = 0 if num not in last else i - last[num]
        last[num] = i
    return num

print(solve(2020), solve(30000000))
