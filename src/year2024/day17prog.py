
def run(A):
    B = 0
    C = 0

    output = []
    while A > 0:
        B = A%8
        B = (B^1) % 8
        C = A >> B
        A = A >> 3
        B = B ^ C
        B = B ^ 6
        output.append(B%8)

    return output


prog = [2,4,1,1,7,5,0,3,4,3,1,6,5,5,3,0]
poss = []

def go(i, prefix):
    if i == len(prog):
        poss.append(prefix)
        return

    for a in range(8):
        if prefix*8+a == 0:
            continue
        if "".join(str(x) for x in prog).endswith("".join(str(x) for x in run(prefix*8+a))):
            go(i+1, prefix*8+a)

go(0, 0)

print(min(poss))

