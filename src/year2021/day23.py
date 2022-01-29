from dataclasses import dataclass
import sys
import heapq
from typing import Tuple, List

from yal.graph import dijkstra2

MAX_ROOM_Y = 3

@dataclass(frozen=True, eq=True)
class Pos:
    hallx: int # 0-10  or -1
    roomx: int  # 0-3
    roomy: int  # 0-3, 0=closest to hallway

    def __lt__(self, other):
        # Ensure further down comes first
        if self.roomy != other.roomy:
            return self.roomy > other.roomy
        if self.hallx != other.hallx:
            return self.hallx < other.hallx
        return self.roomx < other.roomx

    def state(self):
        if self.hallx >= 0:
            return f"H{self.hallx}"
        return f"{self.roomx}{self.roomy}"

@dataclass(frozen=True, eq=True)
class AmpPos:
    amp: int  # 0-3
    pos: Pos

    def __lt__(self, other):
        if self.amp != other.amp:
            return self.amp < other.amp
        return self.pos < other.pos

    def __str__(self):
        return f"{chr(65+self.amp)}{self.pos.state()}"

def amp_move_cost(c:int):
    return 10**c

def room_to_hallx(room:int):
    assert room >= 0 and room < 4
    return 2 + room*2
    
@dataclass(frozen=True)
class State:
    amp_pos: List[AmpPos]

    def __lt__(self, other):
        return True

    def encode(self):
        return ",".join([str(ap) for ap in self.amp_pos])

    def show(self):
        grid_org = [
            "#############",
            "#...........#",
            "###.#.#.#.###",
            "  #.#.#.#.#  ",
            "  #.#.#.#.#  ",
            "  #.#.#.#.#  ",
            "  #########  "
        ]
        grid = [[c for c in s] for s in grid_org]
        
        for ap in self.amp_pos:
            if ap.pos.hallx >= 0:
                grid[1][ap.pos.hallx+1] = chr(65 + ap.amp)
            else:
                grid[ap.pos.roomy+2][ap.pos.roomx*2+3] = chr(65 + ap.amp)
        
        grid = ["".join(row) for row in grid]
        for row in grid:
            print(row)
        print()


    def room_available(self, room) -> int:
        # Which row in this room should I go to?
        # 0 = closest to hallway, MAX_ROOM_Y = furthest in
        # Returns -1 if room is full _or_ if some non-correct amp is in this room        
        ytaken = set()
        for ap in self.amp_pos:
            if ap.pos.roomx == room:
                if ap.amp != room:
                    return -1  # wrong amp in this room
                ytaken.add(ap.pos.roomy)
            
        y = MAX_ROOM_Y
        while y in ytaken:
            y -= 1
        return y

    def is_room_xy_available(self, roomx, roomy):
        return not any(ap.pos.roomx == roomx and ap.pos.roomy == roomy for ap in self.amp_pos)
    
    def hallway_empty(self, x1, x2):
        # Return true if hallway is empty between x1 and x2 (inclusive)
        for ap in self.amp_pos:
            if ap.pos.hallx >= x1 and ap.pos.hallx <= x2:
                return False
        return True

    def move(self, old_pos, new_pos):
        new_amp_pos = [ap if ap.pos != old_pos else AmpPos(ap.amp, new_pos) for ap in self.amp_pos]
        new_amp_pos = list(sorted(new_amp_pos))
        return State(new_amp_pos)

    def is_done(self):
        return all(ap.pos.roomx == ap.amp for ap in self.amp_pos)

    def approx(self):
        cost = 0
        ap_left = {0: 3, 1: 3, 2: 3, 3: 3}
        for ap in self.amp_pos:
            if ap.pos.roomx >= 0:
                xdif = abs(ap.amp - ap.pos.roomx) * 2                
            else:
                xdif = abs(room_to_hallx(ap.amp) - ap.pos.hallx)
            cost += xdif * amp_move_cost(ap.amp)

            if ap.amp == ap.pos.roomx:
                if ap.pos.roomy == ap_left[ap.amp]:
                    ap_left[ap.amp] -= 1

        for amp, left in ap_left.items():            
            moves = (left+1)*(left+2)//2
            cost += amp_move_cost(amp) * moves
            
        return cost

    def neighbors(self) -> List[Tuple["State", int]]:
        new_states = []
        for ap in self.amp_pos:
            amp = ap.amp
            pos = ap.pos
            if pos.hallx >= 0:
                # Must move into its room
                targetx = room_to_hallx(amp)
                # Check if hallway is blocked
                if targetx > pos.hallx and not self.hallway_empty(pos.hallx+1, targetx):
                    continue
                if targetx < pos.hallx and not self.hallway_empty(targetx, pos.hallx-1):
                    continue

                cost = amp_move_cost(amp) * abs(targetx-pos.hallx)
                target_room = amp
                # Check if room is available
                targety = self.room_available(target_room)
                
                if targety >= 0:
                    # Move into the room
                    cost += (targety + 1) * amp_move_cost(amp)
                    new_states.append((self.move(pos, Pos(-1, target_room, targety)), cost))
                
            elif pos.roomx >= 0:
                if pos.roomy == 0 or self.is_room_xy_available(pos.roomx, pos.roomy-1):
                    # Is in the hallway position of a room, move into hallway
                    for hx in range(11):
                        if hx in (2,4,6,8): # never stop outside room
                            continue
                        room_x = room_to_hallx(pos.roomx)
                        if hx < room_x and not self.hallway_empty(hx, room_x):
                            continue
                        if hx > room_x and not self.hallway_empty(room_x, hx):
                            continue
                        cost = amp_move_cost(amp) * (abs(room_x-hx) + (pos.roomy + 1))
                        new_states.append((self.move(pos, Pos(hx, -1, -1)), cost))
        
        return new_states

def parse_input(lines):
    d = []
    for y in range(MAX_ROOM_Y+1):
        for x in range(4):
            c = lines[y+2][x*2+3]
            pos = Pos(-1, x, y)
            d.append(AmpPos(ord(c) - 65, pos))

    d = list(sorted(d))
    return State(d)


# def search(start: State):
#     dist = {}
#     q = []

#     def add(node: State, d: int):
#         nonlocal dist, q
#         node_encoded = node.encode()
#         if node_encoded not in dist or d < dist[node_encoded]:
#             dist[node_encoded] = d            
#             heapq.heappush(q, (d+node.approx(), d, node))

#     visited = 0
#     add(start, 0)
#     while len(q):
#         visited += 1
#         (_, cur_dist, cur) = heapq.heappop(q)
#         if cur.is_done():
#             print("Num states visited", visited)
#             print("Num states stored", len(dist))
#             return cur_dist
#         if cur_dist == dist[cur.encode()]:            
#             for x, d in cur.neighbors():
#                 add(x, cur_dist + d)
    
lines = [line.strip() for line in sys.stdin.readlines()]

start = parse_input(lines)

#print("total cost", search(start))
print("cost", dijkstra2(
        start, 
        lambda cur: cur.neighbors(), 
        done_func=lambda cur: cur.is_done(), 
        hash_func=lambda cur: cur.encode(),
        approx_func=lambda cur: cur.approx()))
