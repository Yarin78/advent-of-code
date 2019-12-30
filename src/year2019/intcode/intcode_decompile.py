import argh
import json
import logging
import itertools
import heapq
import threading
from collections import defaultdict
from queue import Queue
from lib.intcode import *

MODE_POSITION = 0
MODE_IMMEDIATE = 1
MODE_RELATIVE = 2

FUNC_TYPE_SKIP = 'SKIP'  # Ignored function

MAX_FRAME_SIZE = 15


class Node:
    addr = 0   # The address in memory where this node starts
    addr_len = 0  # The number of consecutive bytes this node consumes; may include multiple opcodes
    instr = None  # Instructions at this node
    children = None # Possible next nodes
    parents = None # Possible previous nodes

    def __init__(self, addr, decompiler, func):
        self.addr = addr
        self.decompiler = decompiler
        self.func = func
        (opcode, params, modes) = decompiler.decode(addr)
        self.instr = [(opcode, params, modes)]
        self.addr_len = len(params) + 1
        self.children = []
        self.parents = []
        self.variables_assigned = set()  # variables guaranteed to be assigned

    def get_param_str(self, ip, param_modes):
        param_str = []
        for (param, mode) in param_modes:
            ip += 1
            if mode == MODE_POSITION:
                param_str.append(self.decompiler.mem_address(ip, param))
            elif mode == MODE_RELATIVE:
                param_str.append(self._local_var_name(param))
            else:
                param_str.append(self.decompiler.immediate_value(ip, param))
        return param_str

    def generate_code(self, next_node):
        '''Generates the code for this node.
        next_node is the next node to have code generated.'''
        codes = []
        ip = self.addr
        did_halt = False
        for j in range(len(self.instr)):
            if ip in self.decompiler.modifying_code_addr:
                # If this happens, we're sort of screwed
                logging.warning('Parsing opcode from address %s that can get modified' % ip)
                codes.append('# This instruction may get modified')
            (opcode, params, modes) = self.instr[j]
            param_str = self.get_param_str(ip, zip(params, modes))
            is_return_addr = (0, MODE_RELATIVE) in zip(params, modes)

            if opcode in [OPCODE_ADD, OPCODE_MUL]:
                if is_return_addr:
                    # Don't generate any code for read/writing the return address
                    code = ''
                else:
                    fv = fixed_value(opcode, params, modes)
                    if fv is not None:
                        code = '%s = %d' % (param_str[2], fv)
                    else:
                        code = self._add_mul_code(opcode, param_str, modes)
            elif opcode == OPCODE_IN:
                code = '%s = self.input()' % param_str[0]
            elif opcode == OPCODE_OUT:
                code = 'self.output(%s)' % param_str[0]
            elif opcode == OPCODE_LESS_THAN:
                code = '%s = int(%s < %s)' % (param_str[2], param_str[0], param_str[1])
            elif opcode == OPCODE_EQUALS:
                code = '%s = int(%s == %s)' % (param_str[2], param_str[0], param_str[1])
            elif opcode == OPCODE_ADD_BP:
                code = ''
            elif opcode == OPCODE_HALT:
                #code = 'self.halted = True'
                code = 'raise MachineHaltedException()'
                did_halt = True
            elif opcode in [OPCODE_JUMP_TRUE, OPCODE_JUMP_FALSE]:
                if j != len(self.instr) - 1:
                    # Can happen if a jump can never be evaluated to true
                    code = ''
                else:
                    condition = param_str[0]
                    if opcode == OPCODE_JUMP_FALSE:
                        condition = 'not %s' % condition
                    if len(self.children) < 2:
                        # No branch, the jump will be taken care of elsewhere
                        if ip in self.func.func_calls:
                            (target_addr, _) = self.func.func_calls[ip]
                            # Even if there is an address in func_calls,
                            # it might be a modified instruction, hence the isdigit() check
                            if target_addr is None or not param_str[1].isdigit():
                                # Dynamic dispatcher; the number of parameters is a problem,
                                # we'll assume it's the same as the numbers set in the instructions before
                                # Might be wrong on the numbers returned though
                                num_set = self.num_calling_params_set()
                                call_vars = ', '.join(['q%d' % x for x in range(num_set)])
                                mem_addr = param_str[1]
                                if call_vars:
                                    ret_vars = '(%s)' % call_vars
                                    if not self.decompiler.config['return_all']:
                                        ret_vars = 'q0'
                                    code = '%s = self.funcs[%s](self, %s)' % (ret_vars, mem_addr, call_vars)
                                else:
                                    code = 'self.funcs[%s](self)' % mem_addr
                            else:
                                # If we call a function with frame_size 5 (4 parameters/local vars),
                                # all of them may not have been set.
                                num_params_set = len(list(itertools.takewhile(
                                    lambda x: self._local_var_name(x) in self.variables_assigned,
                                    range(1, 20))))
                                code = self.decompiler.functions[target_addr].call_instr(num_params_set)
                        else:
                            code = 'pass # %d' % len(self. children)
                    else:
                        if ip in self.func.func_calls:
                            logging.warning('Conditional function calls not supported (%d)' % ip)
                        code = 'goto .lbl_%d' % self.children[1].addr

                    if condition:
                        try:
                            if eval(condition):
                                pass  # Always true
                            else:
                                code = ''  # Always false
                        except:
                            # Depends on something that we can evaluate
                            code = ['if %s:' % condition, '    %s' % code]
            else:
                code = ''
            if isinstance(code, list):
                codes.extend(code)
            else:
                codes.append(code)

            ip += 1 + len(params)

        if len(self.children) == 0:
            if not did_halt:
                codes.append(self.func.return_statement())
        elif next_node is None or self.children[0].addr != next_node.addr:
            codes.append('goto .lbl_%d' % self.children[0].addr)

        return codes

    def num_calling_params_set(self):
        # Gets the number of calling parameters set by looking at previous instructions
        cur = self
        vset = set()
        while len(cur.parents) == 1:
            cur = cur.parents[0]
            v = cur.get_target_variable(allow_ret=True)
            if v is None:
                break
            if v == 'RET_ADDR':
                continue
            if v[0] == 'q':
                vset.add(int(v[1:]))
        num_set = 0  # if vset = set(0,1,3), then we have 2 set variables - must be consecutive
        while num_set in vset:
            num_set += 1
        return num_set

    def get_target_variable(self, allow_ret=False):
        # Gets the variable that gets assigned a value in this node, if any
        ip = self.addr
        for j in range(len(self.instr)):  # Should only be one instruction in here that can write to sth
            (opcode, params, modes) = self.instr[j]
            param_str = self.get_param_str(ip, zip(params, modes))
            if opcode in [OPCODE_ADD, OPCODE_MUL, OPCODE_IN, OPCODE_LESS_THAN, OPCODE_EQUALS]:
                if param_str[-1] != 'RET_ADDR' or allow_ret:
                    return param_str[-1]
            ip += 1 + len(params)
        return None

    def get_target_mem_addr(self):
        # Gets the memory address that gets assigned a value in this node, if any
        ip = self.addr
        for j in range(len(self.instr)):  # Should only be one instruction in here that can write to sth
            (opcode, params, modes) = self.instr[j]
            if opcode in [OPCODE_ADD, OPCODE_MUL, OPCODE_IN, OPCODE_LESS_THAN, OPCODE_EQUALS]:
                if modes[-1] == MODE_POSITION:
                    return params[-1]
            ip += 1 + len(params)
        return None

    def _local_var_name(self, rel_addr):
        if rel_addr > 0:
            return 'q%d' % (rel_addr - 1)
        elif rel_addr < 0:
            return 'p%d' % (self.func.frame_size + rel_addr - 1)
        else:
            return 'RET_ADDR'

    def _add_mul_code(self, opcode, params, modes):
        sign = '+' if opcode == OPCODE_ADD else '*'
        if sign == '+' and params[1].startswith('-'):
            sign = '-'
            params[1] = params[1][1:]
        code = '%s = %s %s %s' % (params[2], params[0], sign, params[1])
        if (opcode == OPCODE_ADD and params[0] == '0') or (opcode == OPCODE_MUL and params[0] == '1'):
            if params[2] == params[1]:
                code = ''
            else:
                code = '%s = %s' % (params[2], params[1])
        elif (opcode == OPCODE_ADD and params[1] == '0') or (opcode == OPCODE_MUL and params[1] == '1'):
            if params[2] == params[0]:
                code = ''
            else:
                code = '%s = %s' % (params[2], params[0])
        elif params[2] == params[1]:
            if sign == '*' and params[0] == '-1':
                code = '%s = -%s' % (params[2], params[2])
            else:
                code = '%s %s= %s' % (params[2], sign, params[0])
        elif params[2] == params[0]:
            if sign == '*' and params[1] == '-1':
                code = '%s = -%s' % (params[2], params[2])
            else:
                code = '%s %s= %s' % (params[2], sign, params[1])
        return code


'''Represents a proper function in intcode. The start address is the unique identifier.'''
class Function:

    def __init__(self, decompiler, id, length, frame_size, func_name, func_calls):
        self.decompiler = decompiler
        self.id = id
        self.length = length
        # Frame size 0 means it's in "global" scope, e.g. don't use stack at all
        # Frame size > MAX_FRAME_SIZE mean it's the "init" function setting up the stack
        self.frame_size = frame_size
        self.func_calls = func_calls  # addr -> (target addr, return addr)
        self.func_name = func_name
        self.nodes = None

    def name(self):
        return self.func_name

    def call_instr(self, num_params_set):
        if self.frame_size > MAX_FRAME_SIZE or self.frame_size == 0:
            return 'self.%s()' % self.name()
        call_params = ', '.join(['q%d' % x for x in range(min(num_params_set, self.frame_size - 1))])
        if self.frame_size == 1:
            return 'self.%s(%s)' % (self.name(), call_params)
        if not self.decompiler.config['return_all']:
            return 'q0 = self.%s(%s)' % (self.name(), call_params)
        ret_params = ', '.join(['q%d' % x for x in range(self.frame_size - 1)])
        return '(%s) = self.%s(%s)' % (ret_params, self.name(), call_params)

    def definition(self):
        if self.frame_size > MAX_FRAME_SIZE or self.frame_size == 0:
            return 'def %s(self):' % (self.name())
        params = ', '.join(['p%d=0' % x for x in range(self.frame_size - 1)])
        return 'def %s(self, %s):' % (self.name(), params)

    def return_statement(self):
        if self.frame_size > MAX_FRAME_SIZE or self.frame_size == 0:
            return 'return'
        if self.frame_size == 1:
            return 'return'
        if not self.decompiler.config['return_all']:
            return 'return p0'
        params = ', '.join(['p%d' % x for x in range(self.frame_size - 1)])
        return 'return (%s)' % params

    def required_labels(self, node_order):
        # Stupid way of figuring out what labels are needed, should improve this
        labels = set()
        for i in range(len(node_order)):
            next_node = node_order[i+1] if i+1 < len(node_order) else None
            for child in node_order[i].children:
                if child != next_node:
                    labels.add(child.addr)
        return labels

    def generate_code(self):
        '''Generates code for this functino.'''
        lines = []

        if self.nodes is None:
            logging.warning('No nodes for function %s' % self.name())
            return lines
        lines.append('    @with_goto')
        lines.append('    %s' % self.definition())

        node_order = list(self.nodes.values())

        labels = self.required_labels(node_order)

        for i in range(len(node_order)):
            node = node_order[i]
            next_node = node_order[i+1] if i+1 < len(node_order) else None
            if self.decompiler.config['opcodes_in_functions']:
                (mnemonic, _) = self.decompiler.prog.decode(node.addr)
                lines.append('        # %4d: %s' % (node.addr, mnemonic))
                #lines.append('        # %s' % str(node.variables_assigned))
            if node.addr in labels:
                lines.append('        label .lbl_%d' % node.addr)
            for line in node.generate_code(next_node):
                if line:
                    lines.append('        %s' % line)

        return lines

    def set_variable_assignments(self):
        '''Checks what variables are guaranteed to be assigned at different addresses.'''
        node_order = list(self.nodes.values())
        for node in node_order:
            va = None
            if node.parents:
                for parent in node.parents:
                    if parent.variables_assigned is not None:
                        if va is None:
                            va = parent.variables_assigned
                        else:
                            va = va.intersection(parent.variables_assigned)
            if va is None:
                va = set()
            var = node.get_target_variable()
            va = set(va)  # clone it
            if var is not None:
                va.add(var)
            node.variables_assigned = va
            #logging.warning('Setting va in %d to %s' % (node.addr, str(va)))

    def build_code_graph(self):
        '''Returns a graph with the code execution flow in a function.
        Each node in the created graph represents one opcode and has
        0, 1 or 2 "next addresses" within the same function.
        '''
        next_addr = {}  # addr -> [next_addr]

        ip = self.id

        # Process the instructions in order
        while ip < self.id + self.length:
            next_addr[ip] = []
            (opcode, params, modes) = self.decompiler.decode(ip)
            if ip in self.func_calls:
                jc = self.decompiler.possible_jump_conditions(ip, 'call')
                if True in jc:
                    ret_addr = self.func_calls[ip][1]  # The return address
                    if ret_addr >= 0:
                        next_addr[ip].append(ret_addr)
                if False in jc:
                    # Conditional function calls; not sure we can have this
                    logging.warning('Conditional function call at %d' % ip)
                    next_addr[ip].append(ip+3)
            elif opcode in [OPCODE_JUMP_TRUE, OPCODE_JUMP_FALSE]:
                jc = self.decompiler.possible_jump_conditions(ip)
                if False in jc:
                    next_addr[ip].append(ip + 3)
                if True in jc:
                    if modes[1] == MODE_RELATIVE and params[1] == 0:
                        # Return statement, no more instructions in this function
                        pass
                    else:
                        target = self.decompiler.jump_target(ip)
                        if target is not None:
                            next_addr[ip].append(target)
                        else:
                            logging.warning('Unknown jump target at %d' % ip)
            elif opcode not in [OPCODE_HALT]:
                next_addr[ip].append(ip + 1 + len(params))

            ip += 1 + len(params)

        self.nodes = {}
        for ip, _ in next_addr.items():
            self.nodes[ip] = Node(ip, self.decompiler, self)

        for ip, addrs in next_addr.items():
            for addr in addrs:
                if addr not in self.nodes:
                    # Not good, weird code; hopefully doesn't happen
                    logging.warning('Jump from %d to address %d outside function' % (ip, addr))
                else:
                    self.nodes[ip].children.append(self.nodes[addr])
                    self.nodes[addr].parents.append(self.nodes[ip])


class Decompiler:

    prog = None
    config = None
    functions = None  # addr -> Function
    seen_function_starts = None
    function_queue = None
    addr_func = None # addr -> function id
    modifying_code_addr = None  # set of address in code space that may get written to

    def __init__(self, prog, config):
        self.prog = prog
        self.config = config

    def decompile(self):
        self.functions = {}
        self.addr_func = {}
        self.seen_function_starts = set()

        self.function_queue = Queue()
        self.function_queue.put(0)
        for addr in self.config['functions'].keys():
            self.function_queue.put(addr)

        self.extract_functions()

        # Do the auto detection afterward the regular extract functions, to minimize false positives
        if self.config['auto_detect_functions']:
            self.auto_detect_functions()
            self.extract_functions()

        self.modifying_code_addr = set()
        for func in self.functions.values():
            logging.info('Building code graph for function %s' % func.name())
            func.build_code_graph()
            func.set_variable_assignments()

            # Are we writing to any memory location that is actual code?
            node_order = list(func.nodes.values())
            for node in node_order:
                target_addr = node.get_target_mem_addr()
                if target_addr is not None:
                    for func in self.functions.values():
                        if target_addr >= func.id and target_addr < func.id+func.length:
                            self.modifying_code_addr.add(target_addr)
                            logging.warning('Self-modifying code: Instruction at %d writes to %d' % (node.addr, target_addr))

    def generate_memory_dump(self, start_addr, end_addr):
        lines = ['']

        addr = start_addr
        cur_line = None
        cur_ascii = ''
        cnt = 0

        while addr < end_addr:
            if addr in self.config['opcode_dump']:
                if cur_line is not None:
                    lines.append(cur_line)
                    lines.append('')
                    cur_line = None
                while addr < end_addr:
                    opcode = self.prog.mem[addr] % 100
                    opcode_addr = addr
                    if opcode in self.prog.opcodes:
                        (asm, _) = self.prog.decode(addr)
                        (_, _, length, _) = self.prog.opcodes[opcode]
                        addr += length
                    else:
                        asm = 'DB %d' % opcode
                        addr += 1
                    lines.append('    # %4d: %s' % (opcode_addr, asm))
            else:
                if cnt > 10:
                    lines.append('%-70s%s' % (cur_line, cur_ascii))
                    cur_line = None
                    cur_ascii = ''
                    cnt = 0
                v = self.prog.mem[addr]
                if cur_line is None:
                    cur_line = '    # %4d: DB %d' % (addr, v)
                    cur_ascii = chr(v) if v >= 32 and v < 127 else '.'
                else:
                    cur_line += ', %d' % v
                    cur_ascii += chr(v) if v >= 32 and v < 127 else '.'
                cnt += 1
                addr += 1

        if cur_line is not None:
            lines.append(cur_line)
        return lines

    def generate_code(self, code):
        lines = []
        lines.append('from goto import with_goto')
        lines.append('from lib.intcode import *')
        lines.append('from lib.intcode_decompile import *')
        lines.append('')
        lines.append('class DecompiledProgram(DecompiledProgramBase):')
        lines.append('')

        if self.config['global_variables']:
            for addr, name in self.config['global_variables'].items():
                lines.append('    %s = %d' % (name, self.prog.mem[addr]))

        last_addr = 0
        for func_addr in sorted(self.functions.keys()):
            if func_addr > last_addr:
                lines.extend(self.generate_memory_dump(last_addr, func_addr))

            func = self.functions[func_addr]
            lines.append('')
            lines.extend(func.generate_code())
            last_addr = func_addr + func.length

        lines.extend(self.generate_memory_dump(last_addr, self.prog.last_addr()))

        # Dynamic dispatch table

        lines.append('    funcs = {')
        lines.append('      ' + ', '.join(['%d: %s' % (func_addr, func.name()) for func_addr, func in sorted(self.functions.items())]))
        lines.append('    }')

        # Initial memory

        lines.append('')
        lines.append('    code = [')
        for i in range(0, len(code), 16):
            code_range = code[i:min(len(code), i+16)]
            code_ascii = ''.join([chr(c) if c >= 32 and c < 127 else '.' for c in code_range])
            lines.append('        %-70s  # %s' % (''.join(map(lambda x: '%d,' % x, code_range)), code_ascii))
        lines.append('    ]')

        lines.append('')
        lines.append('')
        lines.append('if __name__ == "__main__":')
        lines.append('      prog = DecompiledProgram()')
        lines.append('      prog.init_io()')
        lines.append('      prog.run_until_halted()')

        return lines

    def auto_detect_functions(self):
        # Find all addresses where we increase the stack pointer
        # OPCODE_ADD_BP + 100, <positive number>
        for i in range(self.prog.last_addr()+1):
            if (self.prog.mem[i] == OPCODE_ADD_BP + 100 and self.prog.mem[i+1] >= 1 and
                    self.prog.mem[i+1] <= MAX_FRAME_SIZE and i not in self.addr_func):
                logging.info('Auto-detected function at %d' % i)
                self.function_queue.put(i)

    def extract_functions(self):
        while not self.function_queue.empty():
            start_ip = self.function_queue.get()
            if start_ip not in self.seen_function_starts:
                func = self.extract_function(start_ip)
                self.seen_function_starts.add(start_ip)
                if func:
                    self.functions[start_ip] = func

    def extract_function(self, start_ip):
        if self.config['functions'].get(start_ip) == FUNC_TYPE_SKIP:
            logging.info('Skipping extracting function at %s' % start_ip)
            return
        if start_ip in self.addr_func:
            logging.warning('Tried to start extracting function at %d but that address is already covered by function at %d' % (start_ip, self.addr_func[start_ip]))

        # Determine frame size
        (opcode, params, modes) = self.decode(start_ip)
        if opcode == OPCODE_ADD_BP and modes[0] == MODE_IMMEDIATE:
            frame_size = params[0]
        else:
            frame_size = 0

        logging.info('Starting extracting function %d with frame size %d' % (start_ip, frame_size))

        func_name = self.config['functions'].get(start_ip)
        if not func_name:
            func_name = 'func%d' % start_ip

        func_addr = set()  # all addresses that are part of this function
        func_calls = {}  # func_calls[x] = (y, z)  => at addr x we're calling function at y and return to address z
        ret_addr = {}  # ret_addr[x] = y  => the return address y was set at x
        ipq = []  # queue of addresses reachable within the current function
        jumps = {}  # jumps[x] = y  => there is a jump (not call) from x to y
        heapq.heappush(ipq, start_ip)
        while ipq:
            ip = heapq.heappop(ipq)
            if ip < 0 or ip > self.prog.last_addr():
                logging.warning('Trying to read outside memory at %d' % ip)
                continue
            if ip in func_addr:
                # This is ok, can be a loop or something
                continue
            if func_addr and ip-1 not in func_addr:
                logging.warning('Function %d reached address %d but last seen opcode was at address %d' % (start_ip, ip, max(func_addr)))
                # Aborting extracting this function since it's probably over;
                # this might not be correct if the code is a bit weird so might want to have an option for this
                break
            if ip in self.addr_func:
                # This is not ok; what was thought to be two functions are intermingled
                logging.warning('Function %d reached address %d, which is included in function %d' % (start_ip, ip, self.addr_func[ip]))

            (opcode, params, modes) = self.decode(ip)
            opcode_len = 1 + len(params)

            if opcode not in self.prog.opcodes:
                logging.warning('Unknown opcode at %d' % ip)
                # func_addr.add(ip)  # Patch if everything is one function
                # heapq.heappush(ipq, ip+1)
                continue

            # Mark the memory of this instruction as belonging to this function
            for i in range(opcode_len):
                if ip + i in func_addr:
                    # Overlapping opcodes - this is weird
                    logging.warning('Part of opcode at %d was already covered in this function' % (ip + i))
                elif ip + i in self.addr_func:
                    # This is odd, should have been caught earlier
                    logging.warning('Part of opcode at %d was covered by function %d' % (ip+i, self.addr_func[ip+i]))
                    continue
                func_addr.add(ip + i)

            if opcode in [OPCODE_JUMP_TRUE, OPCODE_JUMP_FALSE]:
                jump_type = 'jump'
                # If a hard return address was written to (BP) the previous instruction,
                # then this is probably a call, not a jump
                if ip-4 in ret_addr:
                    jump_type = 'call'
                poss = self.possible_jump_conditions(ip, jump_type)
                s = 'Possible' if len(poss) == 2 else 'Mandatory'
                for v in poss:
                    if v:
                        # The jump/call/return may happen
                        if modes[1] == MODE_RELATIVE and params[1] == 0:
                            # Return statement
                            logging.debug('%s return at %d' % (s, ip))
                        else:
                            target = self.jump_target(ip, jump_type)
                            logging.debug('%s %s to %s from %d' % (s, jump_type, str(target) if target is not None else '?', ip))

                            if target is not None:
                                if jump_type == 'jump':
                                    if target < start_ip:
                                        logging.warning('Strange jump at %d to %d which is before function starts; ignoring' % (ip, target))
                                    else:
                                        heapq.heappush(ipq, target)
                                        jumps[ip] = target
                                else:
                                    func_calls[ip] = (target, ret_addr[ip-4])
                                    self.function_queue.put(target)
                                    heapq.heappush(ipq, ret_addr[ip-4])

                            elif modes[1] == MODE_RELATIVE:
                                # !?
                                logging.warning('Target address of %s at %d was relative but not a return statement; more investigation needed' % (jump_type, ip))
                            else:
                                logging.warning('Target address of %s at %d not known; dynamic dispatching will be used' % (jump_type, ip))
                                if ip-4 in ret_addr:
                                    func_calls[ip] = (None, ret_addr[ip-4])
                                if jump_type == 'call':
                                    heapq.heappush(ipq, ret_addr[ip-4])
                    else:
                        # The jump may not happen
                        heapq.heappush(ipq, ip + opcode_len)
            elif opcode != OPCODE_HALT:
                fv = self.fixed_value(ip)
                if fv is not None and modes[2] == MODE_RELATIVE and params[2] == 0:
                    logging.debug('At %d, set return address to %d' % (ip, fv))
                    if fv != ip+7:
                        # Warn if we don't have the pattern
                        # X: <set return address to X+7>
                        # X+4: <call somewhere>
                        # X+7: <continue here after return>
                        logging.warning('Return address is not the expected one')
                    ret_addr[ip] = fv

                heapq.heappush(ipq, ip + opcode_len)

        # Check if we have jumps in the covered area to outside id
        for ip, target in jumps.items():
            if target < min(func_addr) or target > max(func_addr):
                func_calls[ip] = (target, -1)
                self.function_queue.put(target)
                if frame_size != 0:
                    # This is suspicious
                    logging.warning("Jump at %d in proper function is actually to function %d" % (ip, target))
                else:
                    # This is ok, typically in the bootstrap code
                    logging.info("Jump at %d is actually to function %d" % (ip, target))

        # Verify function is continuous and sane
        # Otherwise something is fishy and will break later on
        func_len = max(func_addr) - min(func_addr) + 1
        if min(func_addr) != start_ip:
            logging.warning('Function %d reached earlier byte at %d' % (start_ip, min(func_addr)))
        else:
            if func_len != len(func_addr):
                logging.warning('Function %d covered range [%d,%d] but only %d bytes reached; skipping it' % (start_ip, min(func_addr), max(func_addr), len(func_addr)))
            else:
                logging.info('Successfully identified function [%d,%d]' % (start_ip, max(func_addr)))
                for addr in func_addr:
                    self.addr_func[addr] = start_ip

                return Function(self, start_ip, func_len, frame_size, func_name, func_calls)

    def jump_target(self, ip, jump_type='jump'):
        '''Determines the jump target address at a given ip. Returns None if not possible to figure out.'''
        (_, params, modes) = self.decode(ip)
        target = None

        if ip in self.config['override_target_address']:
            target = self.config['override_target_address'][ip]
        elif modes[1] == MODE_IMMEDIATE:
            target = params[1]
        return target

    def possible_jump_conditions(self, ip, jump_type='jump'):
        '''Returns an array with bools if the jump can happen or not; true if it can happen,
        false if not. If it can't be determined for sure, returns [False, True].
        This can be overridden by setting OVERRIDE_JUMP_CONDITIONS.
        '''
        opcode = self.prog.read(ip)
        mode = (opcode // 100) % 10  # mode of the variable being checked
        opcode %= 100
        assert opcode in [OPCODE_JUMP_FALSE, OPCODE_JUMP_TRUE]
        if ip in self.config['override_jump_conditions']:
            jc = self.config['override_jump_conditions'][ip]
            logging.debug('%s at %d is overridden to %s' % (jump_type.capitalize(), ip, str(jc)))
            return jc
        if mode != MODE_IMMEDIATE:
            logging.debug('%s at %d is conditional' % (jump_type.capitalize(), ip))
            return [False, True]  # indirect addressing, we can't know for sure
        v = self.prog.read(ip+1)
        will_jump = (v != 0) == (opcode == OPCODE_JUMP_TRUE)
        logging.debug('%s at %d will %s happen' % (jump_type.capitalize(), ip, 'always' if will_jump else 'never'))
        return [will_jump]

    def mem_address(self, ip, addr):
        # addr is where we are seemingly reading/writing from
        # but ip is where we got this info from; it could maybe be modified, in which case we need to read the actual value
        if ip in self.modifying_code_addr:
            return 'self.mem[self.mem[%d]]' % ip
        if addr in self.config['local_variables']:
            return self.config['local_variables'][addr]
        elif addr in self.config['global_variables']:
            return 'self.%s' % self.config['global_variables'][addr]
        return 'self.mem[%d]' % addr

    def immediate_value(self, ip, value):
        # value is the value we seemingly read
        # but ip is where we got this info from; it could maybe be modified, in which case we need to read the actual value
        if ip in self.modifying_code_addr:
            return 'self.mem[%d]' % ip
        return str(value)

    def fixed_value(self, ip):
        '''If the MOV or MUL instruction at ip always writes a fixed integer, return that integer.
        Otherwise return None.'''

        if self.modifying_code_addr and (ip+1 in self.modifying_code_addr or ip+2 in self.modifying_code_addr):
            logging.info('Not a fixed value at %d due to self modifying code' % ip)
            return None

        opcode = self.prog.read(ip)
        p1 = self.prog.read(ip+1)
        p2 = self.prog.read(ip+2)
        modes = opcode // 100
        opcode %= 100
        m1 = modes % 10
        m2 = (modes // 10) % 10

        return fixed_value(opcode, [p1, p2], [m1, m2])

    def decode(self, ip):
        '''Returns a tuple (opcode, [p0, p1, ...], [mode0, mode1, ...])'''
        opcode = self.prog.read(ip)
        param_mode = opcode // 100
        opcode %= 100
        params = []
        param_modes = []
        if opcode in self.prog.opcodes:
            opcode_len = self.prog.opcodes[opcode][2]

            for i in range(1, opcode_len):
                x = self.prog.read(ip + i)
                param_modes.append(param_mode % 10)
                params.append(x)
                param_mode //= 10

        return (opcode, params, param_modes)

def fixed_value(opcode, p, m):
    if opcode == OPCODE_MUL:
        if m[0] == MODE_IMMEDIATE and p[0] == 0:
            return 0
        if m[1] == MODE_IMMEDIATE and p[1] == 0:
            return 0
        if m[0] == MODE_IMMEDIATE and m[1] == MODE_IMMEDIATE:
            return p[0] * p[1]
        return None
    elif opcode == OPCODE_ADD:
        if m[0] == MODE_IMMEDIATE and m[1] == MODE_IMMEDIATE:
            return p[0] + p[1]
        return None
    else:
        return None

class DecompiledProgramBase:
    def __init__(self):
        self.mem = defaultdict(int)
        for i in range(len(self.code)):
            self.mem[i] = self.code[i]

    def init_io(self, input=None, output=None):
        if input is None:
            self._input = StdinSource()
            print('Input from stdin')
        elif isinstance(input, list):
            self._input = Queue()
            for x in input:
                self._input.put(x)
        else:
            self._input = input

        if output is None:
            self._output = StdoutSink()
            print('Output to stdout')
        else:
            self._output = output

    def input(self):
        return self._input.get()

    def output(self, value):
        self._output.put(value)

    def run_until_halted(self, start=0):
        try:
            self.funcs[start](self)
        except MachineHaltedException:
            pass

    def start_async(self, start=0, daemon=False):
        t = threading.Thread(target=self.run_until_halted, daemon=daemon, args=(start,))
        t.start()
        return t


    def read_token(self):
        '''Reads a token from the programs output'''
        s = ''
        while True:
            c = self._output.get()
            if c in [10, 32]:
                if s:
                    return s
            else:
                if c < 32 or c > 127:
                    assert not s
                    # non-ASCII values are returned as-is
                    return c
                s += chr(c)

    def read_line(self):
        '''Reads an ASCII line from the programs output'''
        s = ''
        while True:
            c = self._output.get()
            if c == 10:
                return s
            if c < 32 or c > 127:
                assert not s
                return "<%d>" % c
            s += chr(c)

    def write_line(self, line):
        '''Writes an ASCII line to the programs input'''
        for c in line:
            self._input.put(ord(c))
        self._input.put(10)

def load_config(config_file):
    with open(config_file, 'r') as f:
        s = ''
        for line in f.readlines():
            if not line.strip().startswith('#'):
                s += line
        config = json.loads(s)
        config['functions'] = {int(k) :v for k, v in config['functions'].items()}
        config['override_target_address'] = {int(k): v for k, v in config['override_target_address'].items()}
        config['override_jump_conditions'] = {int(k): v for k, v in config['override_jump_conditions'].items()}
        config['global_variables'] = {int(k): v for k, v in config['global_variables'].items()}
        config['local_variables'] = {int(k): v for k, v in config['local_variables'].items()}
        return config

@argh.arg('--config', help='Config file')
@argh.arg('--no-output', help='Just analyze, no output', action='store_true')
@argh.arg('--patch', nargs='+')
def main(config=None, no_output=False, patch=None):
    if config:
        config = load_config(config)

    code = sys.stdin.readline()
    mem = list(map(lambda x: int(x), code.strip().split(',')))
    if patch:
        for p in patch:
            (addr, value) = p.split(':')
            mem[int(addr)] = int(value)

    prog = Program(mem)
    decompiler = Decompiler(prog, config)
    decompiler.decompile()

    if not no_output:
        for line in decompiler.generate_code(mem):
            print(line)

if __name__ == "__main__":
    parser = argh.ArghParser()

    logging.basicConfig(level=logging.INFO)
    argh.dispatch_command(main)
