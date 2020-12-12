import sys

def solve(cur, r=False, p=None):
    def _next(x, y, dx, dy):
        return _next(x+dx,y+dy, dx, dy) if cur[y][x] == '.' and r else cur[y][x]
    return sum(s.count('#') for s in cur) if cur==p else solve(["".join(f"{c}{c}{c}#{c}{c}{c}{c}L"[(c=='L')*3+(c=='#')*6+min(((c!='X' and [_next(x+dx, y+dy, dx, dy) for (dx, dy) in [(-1,-1),(-1, 0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]].count('#'))+2+r)//(3+r),2)] for x,c in enumerate(cur[y])) for y in range(len(cur))], r, cur)

data = list(sys.stdin)
[print(solve(["X"*99, *[f"X{s}X" for s in data], "X"*99], r)) for r in [0,1]]
