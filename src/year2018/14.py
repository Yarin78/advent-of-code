score = [3,7]
e1 = 0
e2 = 1
#days = 846601
#days = 2018
#days = 100000000

haystack = [5,1,5,8,9]
haystack = [8,4,6,6,0,1]

while True:
    tot = score[e1] + score[e2]
    if tot >= 10:
        score.append(tot/10)
        if score[-len(haystack):] == haystack:
            break
    score.append(tot%10)
    if score[-len(haystack):] == haystack:
        break
    e1 = (e1 + 1 + score[e1]) % len(score)
    e2 = (e2 + 1 + score[e2]) % len(score)

#ans = ''.join(map(lambda x: str(x), score[days:days+10]))
#print ans

s = ''.join(map(lambda x: str(x), score))

print s.index(''.join(map(lambda x:str(x), haystack)))
