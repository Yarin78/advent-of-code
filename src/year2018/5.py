import sys

input = sys.stdin.readline().strip()

best = 999999
for remove in range(26):
    data = input.replace(chr(65+remove), '').replace(chr(97+remove), '')

    skip = False
    changed = True
    while changed:
        new_data = ''

        changed = False
        for x in range(len(data)):
            if skip:
                skip = False
                continue
            if x+1 == len(data) or abs(ord(data[x])-ord(data[x+1])) != 32:
                new_data += data[x]
            else:
                skip = True
                changed = True

        data = new_data

    print len(new_data)
    if len(new_data) < best:
        best = len(new_data)

print 'best = %d' % best

