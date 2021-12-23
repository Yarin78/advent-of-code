from dataclasses import dataclass
import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

# hallway length 11

@dataclass(frozen=True, eq=True)
class Pos:
    hallx: int # 0-10  or -1
    room1: int  # 0-3  closest to hallway or -1
    room2: int  # 0-3

def amp_room(c:str):
    return ord(c)-65

def amp_move_cost(c:str):
    return 10**amp_room(c)

def room_to_hallx(room:int):
    assert room >= 0 and room < 4
    return 2 + room*2
    
@dataclass(frozen=True)
class State:
    a1: Pos
    a2: Pos
    b1: Pos
    b2: Pos
    c1: Pos
    c2: Pos
    d1: Pos
    d2: Pos

    def __lt__(self, other):
        return True

    def show(self):
        grid_org = [
            "#############",
            "#...........#",
            "###.#.#.#.###",
            "  #.#.#.#.#  ",
            "  #########  "
        ]
        grid = [[c for c in s] for s in grid_org]
        
        for amp, pos in self.get_amp_pos():
            if pos.hallx >= 0:
                grid[1][pos.hallx+1] = amp
            elif pos.room1 >= 0:
                grid[2][room_to_hallx(pos.room1)+1] = amp
            elif pos.room2 >= 0:
                grid[3][room_to_hallx(pos.room2)+1] = amp
        
        grid = ["".join(row) for row in grid]
        for row in grid:
            print(row)
        print()


    def get_amp_pos(self) -> List[Tuple[str, Pos]]:
        return [
            ("A", self.a1),
            ("A", self.a2),
            ("B", self.b1),
            ("B", self.b2),
            ("C", self.c1),
            ("C", self.c2),
            ("D", self.d1),
            ("D", self.d2),
        ]
    
    def is_room_empty(self, room) -> Tuple[bool, bool]:
        empty1 = True
        empty2 = True
        for _, pos in self.get_amp_pos():
            if pos.room1 == room:
                empty1 = False
            if pos.room2 == room:
                empty2 = False
        return empty1, empty2
    
    def is_room_halfway_done(self, room) -> bool:
        if room == 0:
            return self.a1.room2 == 0 or self.a2.room2 == 0
        if room == 1:
            return self.b1.room2 == 1 or self.b2.room2 == 1
        if room == 2:
            return self.c1.room2 == 2 or self.c2.room2 == 2
        if room == 3:
            return self.d1.room2 == 3 or self.d2.room2 == 3
        assert False

    def hallway_empty(self, x1, x2):
        # Return true if hallway is empty between x1 and x2 (inclusive)
        for amp, pos in self.get_amp_pos():
            if pos.hallx >= x1 and pos.hallx <= x2:
                return False
        return True

    def move(self, old_pos, new_pos):
        return State(
            self.a1 if old_pos != self.a1 else new_pos,
            self.a2 if old_pos != self.a2 else new_pos,
            self.b1 if old_pos != self.b1 else new_pos,
            self.b2 if old_pos != self.b2 else new_pos,
            self.c1 if old_pos != self.c1 else new_pos,
            self.c2 if old_pos != self.c2 else new_pos,
            self.d1 if old_pos != self.d1 else new_pos,
            self.d2 if old_pos != self.d2 else new_pos
        )

    def is_done(self):
        return (self.a1.room1 == 0 or self.a1.room2 == 0) and (self.a2.room1 == 0 or self.a2.room2 == 0) and (self.b1.room1 == 1 or self.b1.room2 == 1) and (self.b2.room1 == 1 or self.b2.room2 == 1) and (self.c1.room1 == 2 or self.c1.room2 == 2) and (self.c2.room1 == 2 or self.c2.room2 == 2) and (self.d1.room1 == 3 or self.d1.room2 == 3) and (self.d2.room1 == 3 or self.d2.room2 == 3)


    def neighbors(self) -> List[Tuple["State", int]]:
        new_states = []
        for amp, pos in self.get_amp_pos():
            #print(amp, pos)
            if pos.hallx >= 0:
                # Must move into its room
                targetx = room_to_hallx(amp_room(amp))
                # Check if hallway is blocked
                if targetx > pos.hallx and not self.hallway_empty(pos.hallx+1, targetx):
                    continue
                if targetx < pos.hallx and not self.hallway_empty(targetx, pos.hallx-1):
                    continue

                cost = amp_move_cost(amp) * abs(targetx-pos.hallx)
                target_room = amp_room(amp)
                # Check if room is available
                e1, e2 = self.is_room_empty(target_room)

                if e1 and e2:
                    # Move deepest into the room
                    cost += 2 * amp_move_cost(amp)
                    new_states.append((self.move(pos, Pos(-1, -1, target_room)), cost))
                elif e1 and self.is_room_halfway_done(target_room):
                    # Move to the hallway position
                    cost += amp_move_cost(amp)
                    new_states.append((self.move(pos, Pos(-1, target_room, -1)), cost))                                
                
            elif pos.room1 >= 0:
                # Is in the hallway position of a room, move into hallway
                # TODO: Not needed if right room and inner position is right, skip?
                for hx in range(11):
                    if hx in (2,4,6,8): # never stop outside room
                        continue
                    room_x = room_to_hallx(pos.room1)
                    if hx < room_x and not self.hallway_empty(hx, room_x):
                        continue
                    if hx > room_x and not self.hallway_empty(room_x, hx):
                        continue
                    cost = amp_move_cost(amp) * (abs(room_x-hx) + 1)
                    new_states.append((self.move(pos, Pos(hx, -1, -1)), cost))
            elif pos.room2 >= 0:
                if pos.room2 == amp_room(amp):
                    # Is in right room at bottom, in place, no move needed
                    continue
                blocked = False
                for _, ap in self.get_amp_pos():
                    if ap.room1 == pos.room2:
                        blocked = True
                if blocked:
                    # Something is blocking the hallway room position
                    continue
                for hx in range(11):
                    if hx in (2,4,6,8): # never stop outside room
                        continue
                    room_x = room_to_hallx(pos.room2)
                    if hx < room_x and not self.hallway_empty(hx, room_x):
                        continue
                    if hx > room_x and not self.hallway_empty(room_x, hx):
                        continue
                    cost = amp_move_cost(amp) * (abs(room_x-hx) + 2)
                    new_states.append((self.move(pos, Pos(hx, -1, -1)), cost))
        
        return new_states

def parse_input(lines):
    d = defaultdict(list)
    for y in range(2):
        for x in range(4):
            c = lines[y+2][x*2+3]
            pos = Pos(-1,-1,x) if y == 1 else Pos(-1, x, -1)
            d[c].append(pos)

    return State(d['A'][0], d['A'][1], d['B'][0], d['B'][1], d['C'][0], d['C'][1], d['D'][0], d['D'][1])


def search(start: State):
    dist = {}
    q = []

    def add(node, d):
        nonlocal dist, q
        if node not in dist or d < dist[node]:
            dist[node] = d
            heapq.heappush(q, (d, node))

    add(start, 0)
    while len(q):
        (cur_dist, cur) = heapq.heappop(q)
        #print(f"cost {cur_dist}")
        #cur.show()
        if cur.is_done():
            return cur_dist
        if cur_dist == dist[cur]:
            for x, d in cur.neighbors():
                add(x, cur_dist + d)



lines = [line.strip() for line in sys.stdin.readlines()]

start = parse_input(lines)

def debug(start: State):
    start = start.move(Pos(-1, 0, -1), Pos(0, -1, -1))
    start = start.move(Pos(-1, 1, -1), Pos(5, -1, -1))
    start.show()

    for state, cost in start.neighbors():
        print("COST =", cost)
        state.show()
        print()


print("total cost", search(start))

#debug(start)