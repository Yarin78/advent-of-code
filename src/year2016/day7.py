import sys
import re
import itertools
from collections import defaultdict

input = sys.stdin
input = open('year2016/day7.in')

def abba(s):
    for i in range(len(s)-3):
        if s[i] == s[i+3] and s[i+1] == s[i+2] and s[i] != s[i+1]:
            return True
    return False

cnt = 0
cnt2 = 0
for line in input.readlines():
    parts = line.strip().replace(']', '[').split('[')
    nope = False
    yup = False
    for i in range(len(parts)):
        if abba(parts[i]):
            if i % 2 == 0:
                yup = True
            else:
                nope = True
    if yup and not nope:
        #print(line.strip())
        cnt += 1

    ok = False
    for i in range(26):
        for j in range(26):
            if i != j:
                aba = '%c%c%c' % (chr(97+i), chr(97+j), chr(97+i))
                bab = '%c%c%c' % (chr(97+j), chr(97+i), chr(97+j))
                odd = False
                even = False
                for k in range(len(parts)):
                    if k % 2 == 0 and aba in parts[k]:
                        even = True
                    if k % 2 == 1 and bab in parts[k]:
                        odd = True
                if odd and even:
                    ok = True


    if ok:
        cnt2 += 1
        #print(line.strip())

print(cnt)
print(cnt2)
