import hashlib

salt = 'abbhdwsy'
pw = [-1]*8
i = 0
left = 8
while left > 0:
    m = hashlib.md5(bytes('%s%d' % (salt, i), 'ascii'))
    d = m.hexdigest()
    if d[0:5] == '00000':
        if d[5] >= '0' and d[5] < '8':
            pos = int(d[5])
            if pw[pos] == -1:
                pw[pos] = d[6]
                left -= 1
                print(pw)
    i += 1

print(''.join(pw))
