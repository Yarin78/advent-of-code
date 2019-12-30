import sys

data = map(lambda s: s.strip(), sys.stdin.readlines())

xsize = len(data[0])
ysize = len(data)

hash_iter_map = {}

MAX_ITER = 1000000000

no_iter = 0
while no_iter < MAX_ITER:
    no_iter += 1
    new_data = []
    tot_tree = 0
    tot_lumber = 0
    for y in range(ysize):
        cur = ''
        for x in range(xsize):
            num_open = 0
            num_tree = 0
            num_lumber = 0
            for dx in range(x-1,x+2):
                for dy in range(y-1,y+2):
                    if dx >= 0 and dy >= 0 and dx < xsize and dy < ysize and (dx != x or dy != y):
                        c = data[dy][dx]
                        if c == '#':
                            num_lumber += 1
                        elif c == '|':
                            num_tree += 1

            c = data[y][x]
            if c == '.' and num_tree >= 3:
                c = '|'
            elif c == '|' and num_lumber >= 3:
                c = '#'
            elif c == '#' and not (num_lumber >= 1 and num_tree >= 1):
                c = '.'
            cur += c
            if c == '|':
                tot_tree += 1
            elif c == '#':
                tot_lumber += 1

        new_data.append(cur)

    data = new_data
    h = hash(','.join(data))
    if h in hash_iter_map and no_iter < 1000:
        print 'Iteration %d is a repeat of iteration %d' % (hash_iter_map[h], no_iter)
        delta = no_iter - hash_iter_map[h]
        no_iter += (MAX_ITER / delta) * delta
        while no_iter >= MAX_ITER:
            no_iter -= delta

    hash_iter_map[h] = no_iter

    print '%d iterations, hash = %d' % (no_iter, h)

    #for line in data:
    #    print line
    #print


print '%d iterations' % no_iter
print
for line in data:
    print line
print

print tot_tree * tot_lumber
