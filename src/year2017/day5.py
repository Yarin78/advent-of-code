import sys
jump = []
for line in sys.stdin.readlines():
    jump.append(int(line))

pc = 0
steps = 0
while pc < len(jump):
    # print('step %d, pc %d, %s' %  (steps, pc, str(jump)))
    steps += 1
    new_pc = pc + jump[pc]
    if jump[pc] >= 3:
        jump[pc] -= 1
    else:
        jump[pc] += 1
    pc = new_pc
print(steps)
