import sys

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
lines = [line.strip() for line in sys.stdin.readlines()]

ysize=len(lines)
xsize=len(lines[0])
prev = lines
while True:
    cur = []
    for y in range(ysize):
        s = ""
        for x in range(xsize):
            c = prev[y][x]
            num_occ = 0
            num_empty = 0

            for dy in range(-1,2):
                for dx in range(-1,2):
                    if dx==0 and dy==0:
                        continue
                    nx=x
                    ny=y
                    nx+=dx
                    ny+=dy
                    while nx >= 0 and ny >= 0 and nx < xsize and ny < ysize:
                        if prev[ny][nx] == '.':
                            nx+=dx
                            ny+=dy
                            continue
                        if prev[ny][nx] == '#':
                            num_occ += 1
                        if prev[ny][nx] == 'L':
                            num_empty += 1
                        break
            if prev[y][x] == 'L' and num_occ == 0:
                c = '#'
            if prev[y][x] == '#' and num_occ >= 5:
                c = 'L'
            s += c
        cur.append(s)
    # for line in cur:
    #     print(line)
    # print()
    if cur == prev:
        break
    prev = cur


ans = 0
for i in range(ysize):
    ans += cur[i].count('#')
print(ans)
