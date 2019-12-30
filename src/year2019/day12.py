import itertools

moon_pos = [16,4,17,13],[-8,10,-5,-3],[13,10,6,0]
moon_vel = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a%b)

def lcm(a, b):
    return a * b // gcd(a,b)

def sign(a):
    return 1 if a > 0 else (-1 if a < 0 else 0)

pos1000 = []
vel1000 = []
reps = []
for coord in range(3):
    t = 0
    seen = {}
    while True:
        state = tuple(moon_pos[coord] + moon_vel[coord])
        if state in seen:
            rep = t-seen[state]
            break
        seen[state] = t
        t += 1
        for (p1, p2) in itertools.combinations(range(4), 2):
            delta = moon_pos[coord][p1] - moon_pos[coord][p2]
            moon_vel[coord][p1] -= sign(delta)
            moon_vel[coord][p2] += sign(delta)

        for p in range(4):
            moon_pos[coord][p] += moon_vel[coord][p]
        if t == 1000:
            pos1000.append(list(moon_pos[coord]))
            vel1000.append(list(moon_vel[coord]))

    print('repeats after %d' % rep)
    reps.append(rep)

e = 0
for p in range(4):
    e1 = abs(pos1000[0][p])+abs(pos1000[1][p])+abs(pos1000[2][p])
    e2 = abs(vel1000[0][p])+abs(vel1000[1][p])+abs(vel1000[2][p])
    e += e1*e2

print(e)

print(lcm(lcm(reps[0], reps[1]), reps[2]))
