import sys
from collections import deque

p1, p2 = sys.stdin.read().split('\n\n')
player1 = deque(map(int, p1[10:].split()))
player2 = deque(map(int, p2[10:].split()))

def hash(d):
    return ",".join(map(str, list(d)))

def get_score(deck):
    return sum(c * (len(deck) - i) for i, c in enumerate(list(deck)))

def play_game(player1, player2):
    seen = set()
    while player1 and player2:
        key = f"{hash(player1)}+{hash(player2)}"
        if key in seen:
            return 1
        seen.add(key)
        c1, c2 = player1.popleft(), player2.popleft()
        if len(player1) >= c1 and len(player2) >= c2:
            score = play_game(deque(list(player1)[:c1]), deque(list(player2)[:c2]))
        else:
            score = c1 - c2

        player1.extend([c1, c2] if score > 0 else [])
        player2.extend([c2, c1] if score < 0 else [])

    return get_score(player1) - get_score(player2)

print(play_game(player1, player2))
