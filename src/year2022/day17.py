import sys
from yal.util import *
from yal.geo2d import *

jetpattern = sys.stdin.readline().strip()

ROCKS = [
    [Point(0,0), Point(1,0), Point(2,0), Point(3,0)],
    [Point(1,0), Point(0,1), Point(1,1), Point(2,1), Point(1,2)],
    [Point(0,0), Point(1,0), Point(2,0), Point(2,1), Point(2,2)],
    [Point(0,0), Point(0,1), Point(0,2), Point(0,3)],
    [Point(0,0), Point(1,0), Point(0,1), Point(1,1)]
]

def simulate(num_rocks):
    chamber = {}
    for x in range(7):
        chamber[Point(x,0)] = '#'
    highest = 0

    def is_okay(p, ri):
        nonlocal chamber
        for rp in ROCKS[ri]:
            np = rp+p
            if np in chamber or np.x < 0 or np.x >= 7:
                return False
        return True

    def put_rock(p, ri):
        nonlocal chamber, highest
        for rp in ROCKS[ri]:
            np = rp+p
            chamber[np] = True
            highest = max(highest, np.y)

    def show():
        nonlocal chamber, highest
        for y in range(highest):
            print(''.join('#' if Point(x,highest-y) in chamber else '.' for x in range(7)))
        print()

    hofs = 0
    lasth = 0
    lasti = 0
    last_diff = -1
    p = 0
    i = 0
    while i < num_rocks:
        if p == 1 and hofs == 0:
            hdiff = highest+1-lasth
            idiff = i-lasti
            if hdiff == last_diff:
                skips = num_rocks//idiff - 3
                i += skips * idiff
                hofs += skips * hdiff
            else:
                lasth = highest+1
                last_diff = hdiff
                lasti=i

        ri = i % 5
        cur = Point(2, highest+4)
        while True:
            if jetpattern[p] == '<' and is_okay(cur-Point(1,0), ri):
                cur -= Point(1,0)
            if jetpattern[p] == '>' and is_okay(cur+Point(1,0), ri):
                cur += Point(1,0)
            p = (p+1) % len(jetpattern)
            if not is_okay(cur - Point(0,1), ri):
                put_rock(cur, ri)
                break
            cur -= Point(0,1)

        i += 1
        # show()

    return highest+hofs

print(simulate(2022))
print(simulate(1000000000000))
