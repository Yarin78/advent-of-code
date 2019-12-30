import sys
cnt = 0
cnt2 = 0
for line in sys.stdin.readlines():
    words = line.strip().split(' ')
    if len(set(words)) == len(words):
        cnt += 1
    words = [''.join(sorted(w)) for w in words]
    if len(set(words)) == len(words):
        cnt2 += 1
print(cnt)
print(cnt2)
