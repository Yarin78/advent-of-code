import sys

class Unit:
    def __init__(self, y, x, type):
        self.x = x
        self.y = y
        self.type = type
        self.hp = 200

    def __repr__(self):
        return '(%d,%d,%c,%d)' % (self.x, self.y, self.type,self.hp)

    def __lt__(self, other):
        return self.coord() < other.coord()

    def coord(self):
        return (self.y, self.x)


map = [] # or . or Unit
units_alive = []
elves_left = 0
goblins_left = 0

directions = [(0,-1), (-1, 0), (1,0), (0,1)]

for line in sys.stdin.readlines():
    s = []
    for c in line.strip():
        if c == '#' or c == '.':
            s.append(c)
        else:
            u = Unit(len(map), len(s), c)
            units_alive.append(u)
            s.append(u)
            if c == 'E':
                elves_left += 1
            else:
                goblins_left += 1
    map.append(s)

def show():
    global map
    for line in map:
        t = ''
        for c in line:
            if type(c)==str:
                sys.stdout.write(c)
            else:
                sys.stdout.write(c.type)
                if len(t) > 0:
                    t += ', '
                t += '%c(%d)' % (c.type, c.hp)
        print '   %s' % t
    print


def adjacent_with(x, y, c):
    global map
    for (dx,dy) in directions:
        if type(map[y+dy][x+dx]) != str and map[y+dy][x+dx].type == c:
            return True
    return False

def bfs(start, targets):
    global map
    dist = []
    for i in range(len(map)):
        dist.append([9999] * len(map[0]))
    q = [start]
    dist[start[0]][start[1]] = 0
    ptr = 0
    while ptr < len(q):
        cur = q[ptr]
        ptr += 1
        if cur in targets:
            return dist
        for (dx,dy) in directions:
            nx = cur[1]+dx
            ny = cur[0]+dy
            if dist[ny][nx] == 9999 and map[ny][nx] == '.':
                dist[ny][nx] = dist[cur[0]][cur[1]] + 1
                q.append((ny,nx))

    return dist

elves_started = elves_left

# 48790
GOBLIN_POWER = 3
ELVES_POWER = 13

print 'Initially:'
show()

rounds = 0
while True:
    units_alive.sort()

    for unit in units_alive:
        if unit.hp <= 0:
            continue
        if elves_left == 0 or goblins_left == 0:
            print 'Combat is over!'
            print '%d elves died' % (elves_started - elves_left)

            hp_left = 0
            for u in units_alive:
                if u.hp >= 0:
                    hp_left += u.hp
            print 'Finished rounds %d, HP left %d, score %d' % (rounds, hp_left, rounds*hp_left)

            exit(1)
        opponent = 'E' if unit.type == 'G' else 'G'

        print 'Unit %s turn' % unit

        if adjacent_with(unit.x, unit.y, opponent):
            print ' no move necessary'
            pass
        else:
            target_squares = set()
            for enemy in units_alive:
                if enemy.hp > 0 and enemy.type == opponent:
                    for (dx,dy) in directions:
                        if map[enemy.y+dy][enemy.x+dx] == '.':
                            target_squares.add((enemy.y+dy, enemy.x+dx))

            print ' %d target squares' % len(target_squares)

            # Should move
            dist_map = bfs((unit.y, unit.x), target_squares)
            #print dist_map
            #exit(1)

            best = 9999
            target_square = None
            for (y,x) in sorted(list(target_squares)):
                if dist_map[y][x] < best:
                    best = dist_map[y][x]
                    target_square = (y,x)

            if not target_square:
                print ' no target square reachable'
            else:
                print ' planning to get to %d,%d, distance %d' % (target_square[1], target_square[0], best)
                dist_map = bfs(target_square, (unit.y, unit.x))
                best = 1e9
                new_sq = None
                for (dx,dy) in directions:
                    if dist_map[unit.y+dy][unit.x+dx] < best:
                        best = dist_map[unit.y+dy][unit.x+dx]
                        new_sq = (unit.y+dy, unit.x+dx)
                if not new_sq:
                    print 'oops'
                    exit(1)
                print ' moving to %d,%d' % (new_sq[1], new_sq[0])
                map[unit.y][unit.x] = '.'
                unit.x = new_sq[1]
                unit.y = new_sq[0]
                map[unit.y][unit.x] = unit

        best_hp = 1000
        aunit = None
        for (dx,dy) in directions:
            nx = unit.x+dx
            ny = unit.y+dy
            if type(map[ny][nx]) != str and map[ny][nx].type == opponent and map[ny][nx].hp < best_hp:
                aunit = map[ny][nx]
                best_hp = aunit.hp

        if not aunit:
            print ' none to attack'
        else:
            print ' attacking unit %s' % aunit
            attack_power = ELVES_POWER if unit.type == 'E' else GOBLIN_POWER
            aunit.hp -= attack_power
            if aunit.hp < 0:
                print ' unit dies!'
                if aunit.type == 'E':
                    elves_left -= 1
                else:
                    goblins_left -= 1
                map[aunit.y][aunit.x] = '.'


    rounds += 1
    print 'After %d rounds:' % rounds
    show()
