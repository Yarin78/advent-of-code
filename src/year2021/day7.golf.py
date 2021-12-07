d = list(map(int, input().split(',')))

print(min(sum(abs(y-x) for y in d) for x in range(min(d), max(d))))
print(min(sum(abs(y-x)*(abs(y-x)+1)//2 for y in d) for x in range(min(d), max(d))))
