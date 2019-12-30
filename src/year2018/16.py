import sys

def addr(regs, vals):
    regs[vals[2]] = regs[vals[0]] + regs[vals[1]]

def addi(regs, vals):
    regs[vals[2]] = regs[vals[0]] + vals[1]

def mulr(regs, vals):
    regs[vals[2]] = regs[vals[0]] * regs[vals[1]]

def muli(regs, vals):
    regs[vals[2]] = regs[vals[0]] * vals[1]

def banr(regs, vals):
    regs[vals[2]] = regs[vals[0]] & regs[vals[1]]

def bani(regs, vals):
    regs[vals[2]] = regs[vals[0]] & vals[1]

def borr(regs, vals):
    regs[vals[2]] = regs[vals[0]] | regs[vals[1]]

def bori(regs, vals):
    regs[vals[2]] = regs[vals[0]] | vals[1]

def setr(regs, vals):
    regs[vals[2]] = regs[vals[0]]

def seti(regs, vals):
    regs[vals[2]] = vals[0]

def gtir(regs, vals):
    regs[vals[2]] = 1 if vals[0] > regs[vals[1]] else 0

def gtri(regs, vals):
    regs[vals[2]] = 1 if regs[vals[0]] > vals[1] else 0

def gtrr(regs, vals):
    regs[vals[2]] = 1 if regs[vals[0]] > regs[vals[1]] else 0

def eqir(regs, vals):
    regs[vals[2]] = 1 if vals[0] == regs[vals[1]] else 0

def eqri(regs, vals):
    regs[vals[2]] = 1 if regs[vals[0]] == vals[1] else 0

def eqrr(regs, vals):
    regs[vals[2]] = 1 if regs[vals[0]] == regs[vals[1]] else 0

INSTRUCTIONS = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

def matches(regs_before, regs_after, vals):
    m = []
    for instr in INSTRUCTIONS:
        regs = regs_before[:]
        instr(regs, vals[1:])
        if regs == regs_after:
            m.append(instr)
    return m


op_code = []

for i in range(16):
    op_code.append(set(INSTRUCTIONS))

no_cases = 0
three_or_more = 0
while True:
    before = sys.stdin.readline()
    if not before.strip():
        break
    before = map(lambda x: int(x), before[9:-2].split(','))
    vals = map(lambda x: int(x), sys.stdin.readline().split(' '))
    after = sys.stdin.readline()
    after = map(lambda x: int(x), after[9:-2].split(','))

    matching = matches(before, after, vals)
    if len(matching) >= 3:
        three_or_more += 1

    op_code[vals[0]] = op_code[vals[0]].intersection(set(matching))

    no_cases += 1

    sys.stdin.readline()

print 'Processed %d cases' % no_cases
print 'Three or more: %d' % three_or_more


op_code_m = [0] * 16
fixed = set()
updated = True
while updated:
    updated = False
    for i in range(16):
        if op_code_m[i] == 0:
            op_code[i] = op_code[i].difference(fixed)
            if len(op_code[i]) == 1:
                op_code_m[i] = list(op_code[i])[0]
                fixed.add(op_code_m[i])
                updated = True


for i in range(16):
    print op_code_m[i]

no_lines = 0

regs = [0, 0, 0, 0]
for line in sys.stdin.readlines():
    if not line.strip():
        continue
    vals = map(lambda x: int(x), line.split(' '))
    instr = op_code_m[vals[0]]
    instr(regs, vals[1:])
    no_lines += 1

print 'No lines executed: %d' % no_lines
print regs

