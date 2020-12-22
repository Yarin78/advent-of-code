import sys
from queue import Queue
from collections import defaultdict, deque
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from vm.vm import *

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
lines = [line.strip() for line in sys.stdin.readlines()]

player1 = deque()
player2 = deque()
pcnt = 0
for line in lines:
    if line.startswith("Player"):
        pcnt += 1
    elif line:
        card = int(line)
        if pcnt == 1:
            player1.append(card)
        else:
            player2.append(card)

#print(len(player1), player1)
#print(len(player2), player2)

def hash(d):
    return ",".join(map(str, list(d)))

next_game = 1

def play_game(player1, player2):
    global next_game
    game_no = next_game
    next_game += 1
    seen = set()
    round = 1
    while player1 and player2:
        #print(f"-- Round {round} (Game {game_no})")
        #print("P1 deck: ", player1)
        #print("P2 deck: ", player2)
        key = f"{hash(player1)}+{hash(player2)}"
        if key in seen:
            return 1, 0
        seen.add(key)
        c1 = player1.popleft()
        c2 = player2.popleft()
        #print("P1 plays ", c1)
        #print("P2 plays ", c2)
        if len(player1) >= c1 and len(player2) >= c2:
            #print("subgame")
            cp1 = deque(player1)
            cp2 = deque(player2)
            while len(cp1) > c1:
                cp1.pop()
            while len(cp2) > c2:
                cp2.pop()

            s1, s2 = play_game(cp1, cp2)
            p1w = s1 > s2
        else:
            p1w = c1 > c2

        if p1w:
            #print(f"Player 1 wins round {round} of game {game_no}!")
            player1.append(c1)
            player1.append(c2)
        else:
            #print(f"Player 2 wins round {round} of game {game_no}!")
            player2.append(c2)
            player2.append(c1)
        round += 1
        #print()

    return get_score(player1), get_score(player2)

def get_score(deck):
    sum = 0
    cur = 1
    while deck:
        sum += cur * deck.pop()
        cur += 1
    return sum


s1, s2 = play_game(player1, player2)

print(s1, s2)
