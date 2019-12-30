import sys

boxes = [line.strip() for line in sys.stdin.readlines()]

for i in range(len(boxes)):
    for j in range(i+1,len(boxes)):
        b1 = boxes[i]
        b2 = boxes[j]
        s = ''
        err = 0
        for k in range(len(b1)):
            if b1[k] != b2[k]:
                err += 1
            else:
                s += b1[k]
        if err == 1:
            print s

