import sys

dir_chars = ">v<^"
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3
dirs = [(1,0), (0,1), (-1,0), (0,-1)] # right, down, left, up
cars = []
car_pos = set()

track = []
for line in sys.stdin.readlines():
    s = ""
    for x in range(len(line)-1):
        c = line[x]
        if c in dir_chars:
            dir = dir_chars.index(line[x])
            cars.append((len(track), x, dir, 0, 0))
            car_pos.add((len(track), x))
            c = '-' if dir % 2 == 0 else '|'
        s += c
    track.append(s)

ticks = 0

def show(track, cars):
    t = [list(line) for line in track]
    for (y,x,dir,turn) in cars:
        t[y][x] = dir_chars[dir]
    for line in t:
        print ''.join(line)
    print

#show(track, cars)

while len(car_pos) > 1:
    ticks += 1
    print 'Tick %d' % ticks
    cars.sort()

    for i in range(len(cars)):
        (y,x,dir,turn,crashed) = cars[i]
        if crashed:
            continue
        car_pos.remove((y,x))
        x += dirs[dir][0]
        y += dirs[dir][1]
        if (y,x) in car_pos:
            print 'Crash at %d,%d during tick %d' % (x,y,ticks)
            for j in range(len(cars)):
                if cars[j][0] == y and cars[j][1] == x:
                    cars[j] = (y,x,0,0,1)
            car_pos.remove((y,x))
            crashed=1
        else:
            car_pos.add((y,x))
        if track[y][x] == '\\':
            if dir == LEFT:
                dir = UP
            elif dir == DOWN:
                dir = RIGHT
            elif dir == RIGHT:
                dir = DOWN
            elif dir == UP:
                dir = LEFT
        elif track[y][x] == '/':
            if dir == LEFT:
                dir = DOWN
            elif dir == DOWN:
                dir = LEFT
            elif dir == RIGHT:
                dir = UP
            elif dir == UP:
                dir = RIGHT
        elif track[y][x] == '+':
            if turn == 0:
                dir = (dir + 3) % 4
            elif turn == 2:
                dir = (dir + 1) % 4
            turn = (turn + 1) % 3
        elif track[y][x] != '-' and track[y][x] != '|':
            print 'oops %d,%d %c' % (x,y,track[y][x])
            exit(1)
        cars[i] = (y,x,dir,turn,crashed)

    #show(track, cars)

print 'Cars left:'
for (y,x,dir,turn,crashed) in cars:
    if not crashed:
        print '%d,%d' % (x,y)
