import sys

line = sys.stdin.readline()
if not line.startswith('#ip'):
    print 'Expected #ip on first line'
    exit(1)
ip_reg = int(line[3:].strip())

lines = sys.stdin.readlines()

print '#include <cstdio>'
print '#include <cstdlib>'
print '#include <cassert>'
print
print 'using namespace std;'
print

print 'int main() {'
print '  long long a=0, b=0, c=0, d=0, e=0, f=0;'
print

output = []
targets = set()
reg_names = 'abcdef'

op_map = {
    'add' : '+',
    'mul' : '*',
    'ban' : '&',
    'bor' : '|'
}
cmp_map = {
    'gt' : '>',
    'eq' : '=='
}

addr = 0
for line in lines:
    parts = line.split(' ')
    args = map(lambda x: int(x), parts[1:])
    instr = parts[0]
    org = '%s %s' % (instr, args)

    if args[2] == ip_reg:
        dest = -1
        prefix = ''
        if instr == 'seti':
            # Absolute jump
            dest = args[0] + 1
        elif instr == 'addi':
            if args[0] == ip_reg:
                # Relative jump
                dest = addr + args[1] + 1
            else:
                # Not supported, jumping to (REG) + OFFSET
                pass
        elif instr == 'addr':
            if args[0] != ip_reg and args[1] != ip_reg:
                # Not supported, jumping to (REG) + (REG)
                pass
            else:
                # Conditional jump; only supported if condition is 0 or 1
                ofs_reg = args[1] if args[0] == ip_reg else args[0]

                output.append((addr, 'assert(%s == 0 || %s == 1);' % (reg_names[ofs_reg], reg_names[ofs_reg]), ''))
                dest = addr + 2
                prefix = 'if (%c) ' % (reg_names[ofs_reg])

        if dest >= len(lines):
            output.append((addr, '%sexit(0);' % prefix, org))
        elif dest >= 0:
            output.append((addr, '%sgoto addr_%d;' % (prefix, dest), org))
            targets.add(dest)
        else:
            output.append((addr, '<unsupported goto>', org))
    else:
        regs0 = regs1 = -1
        regs2 = reg_names[args[2]]
        if args[0] < len(reg_names):
            regs0 = str(addr) if args[0] == ip_reg else reg_names[args[0]]
        if args[1] < len(reg_names):
            regs1 = str(addr) if args[1] == ip_reg else reg_names[args[1]]

        # Ordinary instructions
        if instr == 'seti':
            output.append((addr, '%s = %d;' % (regs2, args[0]), org))
        elif instr == 'setr':
            output.append((addr, '%s = %s;' % (regs2, regs0), org))
        elif instr == 'addi' or instr == 'muli' or instr == 'bani' or instr == 'bori':
            op = op_map[instr[0:3]]
            output.append((addr, '%s = %s %c %d;' % (regs2, regs0, op, args[1]), org))
        elif instr == 'addr' or instr == 'mulr' or instr == 'banr' or instr == 'borr':
            op = op_map[instr[0:3]]
            output.append((addr, '%s = %s %c %s;' % (regs2, regs0, op, regs1), org))
        elif instr == 'gtir' or instr == 'eqir':
            op = cmp_map[instr[0:2]]
            output.append((addr, '%s = %d %s %s ? 1 : 0;' % (regs2, args[0], op, regs1), org))
        elif instr == 'gtri' or instr == 'eqri':
            op = cmp_map[instr[0:2]]
            output.append((addr, '%s = %s %s %d ? 1 : 0;' % (regs2, regs0, op, args[1]), org))
        elif instr == 'gtrr' or instr == 'eqrr':
            op = cmp_map[instr[0:2]]
            output.append((addr, '%s = %s %s %s ? 1 : 0;' % (regs2, regs0, op, regs1), org))
        else:
            output.append((addr, '<unsupported instr>', '%s %s' % (instr, args)))

    addr += 1

output.append((addr, 'return 0;', ''))

for row in output:
    if row[0] in targets:
        print 'addr_%d:' % row[0]
        targets.remove(row[0])
    sys.stdout.write('  %-25s' % row[1])
    if row[2]:
        sys.stdout.write('   // %s' % row[2])
    print

print '}'
