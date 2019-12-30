import sys

state = sys.stdin.readline().strip()
d = {}
for line in sys.stdin.readlines():
    if len(line.strip()) > 0:
        d[line[0:5]] = line[9]

GEN = 50000000000

seen = {}
generation = 0
left_pad = 0
jumped = True #False
while generation < GEN:
    if not jumped and (state, left_pad) in seen:
        cycle = generation-seen[state]
        generation += (GEN / cycle) * cycle
        while generation >= GEN:
            generation -= cycle
        jumped = True
    seen[(state, left_pad)] = generation

    generation += 1
    old = '....' + state + '.......'
    next = ''
    for i in range(2, len(old)-2):
        next += d.get(old[i-2:i+3], '.')
    left_pad += 2
    state = next.lstrip('.')
    left_pad -= (len(next) - len(state))
    state = state.rstrip('.')
    while left_pad > 3:
        state = state[1:]
        left_pad -= 1

    sum = 0
    for i in range(len(state)):
        if state[i] == '#':
            sum += i-left_pad


    print '%2d: %s  (%d) => %d' % (generation, state, -left_pad, sum)

