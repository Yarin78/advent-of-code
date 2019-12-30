import sys

opcodes = {
    'add': (1, 3, 4),
    'mul': (2, 3, 4),
    'in': (3, 1, 2),
    'out': (4, 1, 2),
    'jt': (5, 2, 3),
    'jf': (6, 2, 3),
    'lt': (7, 3, 4),
    'eq': (8, 3, 4),
    'addbp': (9, 1, 2),
    'halt': (99, 0, 1),

    'db': (0, 1, 1),
    'addto': (0, 2, 4),
    'mov': (0, 2, 4),
    'jmp': (0, 1, 3),
    'call': (0, 1, 7),
}


asm = {}  # line_number -> instr
labels = {}

line_no = 0
cur_addr = 0
for line in sys.stdin.readlines():
    line_no += 1
    line = line[0:-1]
    if '#' in line:
        line = line[0:line.find('#')]
    if not line.strip():
        continue
    if line[0] != ' ' and line.endswith(':'):
        labels[line[0:-1]] = cur_addr
    elif line[0] != ' ' and '=' in line:
        [lbl, value] = line.split('=')
        labels[lbl.strip()] = int(value)
    else:
        asm[line_no] = line.strip()
        instr = asm[line_no].split(' ')[0]
        assert instr in opcodes, 'Unknown instruction on line %d: %s' % (line_no, instr)
        cur_addr += opcodes[instr][2]

output = []

cur_addr = 0
for (line_no, line) in asm.items():
    line_parts = line.split(' ', 1)
    instr = line_parts[0]

    assert instr in opcodes, 'Unknown instruction on line %d: %s' % (line_no, instr)
    (opcode, num_params, instr_len) = opcodes[instr]
    next_addr = cur_addr + instr_len

    params = []
    param_modes = 0
    if len(line_parts) > 1:
        for p in line_parts[1].strip().split(','):
            # params can be in form
            # <number>|<label>
            # (<number>|<label>)
            # (bp+<number>)
            mode = 1
            p = p.strip()
            if p[0] == '(':
                assert p[-1] == ')'
                p = p[1:-1]
                if p.startswith('bp'):
                    mode = 2
                    p = p[2:]
                else:
                    mode = 0
            if p == '':
                value = 0
            elif p[0].isdigit() or p[0] == '-' or p[0] == '+':
               value = int(p)
            elif p[0] == "'":
                assert len(p) == 3
                assert p[2] == "'"
                value = ord(p[1])
            else:
                ofs = 0
                if '+' in p:
                    ix = p.find('+')
                    ofs=int(p[ix+1:])
                    p = p[:ix]
                elif '-' in p:
                    ix = p.find('-')
                    ofs=-int(p[ix+1:])
                    p = p[:ix]
                if p == 'CUR':
                    value = cur_addr + ofs
                elif p == 'NEXT':
                    value = next_addr + ofs
                else:
                    assert p in labels, 'Unknown label on line %d' % line_no
                    value = labels[p] + ofs
            param_modes += mode * 10**(2+len(params))
            params.append(value)

    assert len(params) == num_params, 'Wrong number of params on line %d' % line_no

    # pseudoinstructions
    if opcode == 0:
        if instr == 'addto':
            opcode = 1
            params.append(params[1])
            if param_modes // 1000 == 2:
                param_modes += 20000
        elif instr == 'mov':
            opcode = 1
            params.insert(0, 0)
            param_modes *= 10
            param_modes += 100
        elif instr == 'jmp':
            opcode = 5
            params.insert(0, 1)
            param_modes *= 10
            param_modes += 100
        elif instr == 'db':
            opcode = params[0]
            params = []
            param_modes = 0
        elif instr == 'call':
            output.extend([21101, 0, next_addr, 0])
            opcode = 5
            params.insert(0, 1)
            param_modes *= 10
            param_modes += 100


    output.append(opcode + param_modes)
    output.extend(params)

    cur_addr = next_addr

print(','.join(str(x) for x in output))
