import sys
from collections import defaultdict

class Marble:
    def __init__(self, index):
        self.index = index
        self.next = None
        self.prev = None

ring = Marble(0)
ring.next = ring
ring.prev = ring
m0 = ring
current = ring

def show(start, current):
    m = start
    while True:
        if m == current:
            sys.stdout.write('(%d) ' % m.index)
        else:
            sys.stdout.write(' %d  ' % m.index)
        m = m.next
        if m == start:
            break
    print

NO_PLAYERS = 448
MAX_MARBLE = 71628*100

scores = defaultdict(int)
current_player = 1

for m in range(1,MAX_MARBLE + 1):
    if m % 23 == 0:
        scores[current_player] += m
        for i in range(7):
            current = current.prev
        scores[current_player] += current.index
        old_prev = current.prev
        current.prev.next = current.next
        current.next.prev = old_prev
        current = current.next
    else:
        p = current.next
        q = p.next

        nm = Marble(m)
        nm.prev = p
        nm.next = q
        p.next = nm
        q.prev = nm

        current = nm

    #show(m0, current)
    current_player += 1
    if current_player > NO_PLAYERS:
        current_player = 1

hiscore = 0
for player, score in scores.iteritems():
    print player, score
    if score > hiscore:
        hiscore = score
        best_player = player

print
print 'Elf %d wins with score %d' % (best_player, hiscore)

