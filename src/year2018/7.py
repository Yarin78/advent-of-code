import sys

#Step A must be finished before step N can begin.

deps = {}

last_step = 0
for line in sys.stdin.readlines():
    p = ord(line[5])-65
    q = ord(line[36])-65
    if q > last_step:
        last_step = q

    if q not in deps:
        deps[q] = set()
    deps[q].add(p)


left = set(range(0, last_step+1))
work_left = {}
second = 0
NO_WORKERS = 5
BASE_TIME = 60

while len(left) > 0:
    for k in work_left.keys():
        work_left[k] -= 1
        if work_left[k] == 0:
            for t in deps.values():
                t.discard(k)
            left.remove(k)
            del work_left[k]

    for i in left:
        if len(work_left) >= NO_WORKERS:
            break
        if i in work_left:
            continue
        if i not in deps or len(deps[i]) == 0:
            work_left[i] = BASE_TIME + i + 1

    sys.stdout.write('%3d' % second)
    for k,v in work_left.iteritems():
        sys.stdout.write(' %c (%2d)  ' % (chr(k+65), v))
    print
    second += 1

print

