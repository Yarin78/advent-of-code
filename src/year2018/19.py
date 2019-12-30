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


memory = []
ip_reg = 0
for line in sys.stdin.readlines():
    if line.startswith('#ip'):
        ip_reg = int(line[3:].strip())
    else:
        parts = line.split(' ')
        vals = map(lambda x: int(x), parts[1:])
        memory.append( ((locals()[parts[0]]), vals) )

count = 0
ip = 0
regs = [0, 0, 0, 0, 0, 0]
while ip >= 0 and ip < len(memory):
    regs[ip_reg] = ip
    m = memory[ip]
    old_regs = regs[:]
    m[0](regs, m[1])
    print "ip=%d %s %s %d %d %d %s" % (ip, old_regs, m[0].__name__, m[1][0], m[1][1], m[1][2], regs)

    ip = regs[ip_reg]

    ip += 1
    count += 1
    if count > 20:
        break


#print regs
