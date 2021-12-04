import sys

nums = list(enumerate(map(int,input().split(','))))
rev_nums = {k:v for v,k in nums}
lines = sys.stdin.readlines()
scores = []
r5 = range(5)
for i in range(0, len(lines), 6):
    board = [int(s[x*3:x*3+2]) for s in lines[i+1:i+6] for x in r5]
    d = min(min(max(rev_nums[board[y*5+x]] for x in r5) for y in r5), min(max(rev_nums[board[y*5+x]] for y in r5) for x in r5))
    scores.append((d, sum(v for v in board if rev_nums[v] > d)*nums[d][1]))

scores.sort()
print(scores[0][1], scores[-1][1])
