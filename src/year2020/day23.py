import sys

def get_chain(after, current, count):
    chain = []
    for _ in range(count):
        chain.append(after[current])
        current = after[current]
    return chain

def simulate(seed, cups, steps):
    order = [int(seed[pos]) if pos < len(seed) else pos+1 for pos in range(cups)]
    after = {order[i]: order[(i+1) % cups] for i in range(cups)}
    current = order[0]
    for _ in range(steps):
        p = get_chain(after, current, 3)
        dest = current - 1 if current > 1 else cups
        while dest in p:
            dest = dest - 1 if dest > 1 else cups

        after[current] = after[p[-1]]
        after[p[-1]] = after[dest]
        after[dest] = p[0]

        current = after[current]
    return after

seed = sys.stdin.read().strip()

after = simulate(seed, len(seed), 100)
print(''.join(map(str, get_chain(after, 1, len(seed)))))

after = simulate(seed, 1000000, 10000000)
print(after[1] * after[after[1]])
