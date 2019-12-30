import sys
import re
from collections import defaultdict

guard_sleep = defaultdict(int)
minute_count = {}

#[1518-11-01 00:00]
p = re.compile('\[(\d+)\-(\d+)\-(\d+) (\d+):(\d+)\]')
for line in sys.stdin.readlines():
    m = p.match(line)

    [year, month, day, hour, minute] = map(lambda x:int(x), list(m.groups()))
    line = line[19:]

    if 'begins shift' in line:
        guard_no = int(line.split(' ')[1][1:])
    elif 'falls asleep' in line:
        asleep = minute
    elif 'wakes up' in line:
        awake = minute
        guard_sleep[guard_no] += awake - asleep
        if guard_no not in minute_count:
            minute_count[guard_no] = [0] * 60
        for i in range(asleep, awake):
            minute_count[guard_no][i] += 1
    else:
        print 'oops'
        exit(1)

guard = max([(k,v) for k,v in guard_sleep.iteritems()], key=lambda x:x[1])[0]

best = 0
for i in range(0,60):
    if minute_count[guard][i] > best:
        best = minute_count[guard][i]
        minute_picked = i

print 'Guard %d sleeps most, most often on minute %d (%d times). Value: %d' % (guard, minute_picked, best, guard*minute_picked)

best = 0
for guard in minute_count.keys():
    for i in range(0,60):
        if minute_count[guard][i] > best:
            best = minute_count[guard][i]
            minute_picked = i
            guard_picked = guard

print 'Guard %d, minute %d (%d times), value %d' % (guard_picked, minute_picked, best, guard_picked * minute_picked)

