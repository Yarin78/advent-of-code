import sys
from collections import deque

def get_score(deck):
    return sum(c * i for i, c in enumerate(reversed(deck), 1))

def play_game(p1, p2):
    seen = set()
    while p1 and p2:
        key = (tuple(p1), tuple(p2))
        if key in seen:
            return 1
        seen.add(key)
        c1, c2 = p1.popleft(), p2.popleft()
        if len(p1) >= c1 and len(p2) >= c2:
            score = play_game(deque(list(p1)[:c1]), deque(list(p2)[:c2]))
        else:
            score = c1 - c2

        p1.extend([c1, c2] if score > 0 else [])
        p2.extend([c2, c1] if score < 0 else [])

    return get_score(p1) - get_score(p2)

p1, p2 = sys.stdin.read().split('\n\n')
print(abs(play_game(deque(map(int, p1[10:].split())), deque(map(int, p2[10:].split())))))
