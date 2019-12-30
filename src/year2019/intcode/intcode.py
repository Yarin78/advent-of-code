from collections import defaultdict
from queue import Queue, Empty
import concurrent.futures
import threading
import functools
import logging
import sys
import copy

logger = logging.getLogger(__name__)

# Behaviour when trying to read and there is nothing on the input
# Default is to pause the machine (and not update the IP)
CRASH_ON_EOF = False   # Raise exception if trying to read from input when there is no data
BLOCK_ON_EOF = False   # Block calling thread if trying to read from input when there is no data

SHOW_PROGRESS = True

# The parameters are called x, y, z
OPCODE_ADD = 1         # z = x + y
OPCODE_MUL = 2         # z = x * y
OPCODE_IN = 3          # x = <value from input>
OPCODE_OUT = 4         # <write x to output>
OPCODE_JUMP_TRUE = 5   # if x<>0 then jump y
OPCODE_JUMP_FALSE = 6  # if x=0 then jump y
OPCODE_LESS_THAN = 7   # z = x < y ? 1 : 0
OPCODE_EQUALS = 8      # z = x == y ? 1 : 0
OPCODE_ADD_BP = 9      # bp += x
OPCODE_HALT = 99

class Program(object):

    opcodes = {}

    def __init__(self, code, prog_id=0):
        if isinstance(code, list):
            self.factory_settings = code[:]
        else:
            self.factory_settings = list(map(lambda x: int(x), code.strip().split(',')))
        self.reset()
        self.prog_id = prog_id
        self._input = None
        self._output = None

    def reset(self):
        mem = self.factory_settings[:]
        self.mem = defaultdict(int)
        for i in range(len(mem)):
            self.mem[i] = mem[i]

        self.ip = 0
        self.count = 0  # num instructions executed
        self.instr_count = [0]*len(self.mem)
        self.halted = False
        self.blocked_on_input = False
        self.last_in = 0
        self.last_out = 0
        self.base_ptr = 0

    def last_addr(self):
        return max(self.mem.keys())

    def log_debug(self):
        logging.basicConfig(level=logging.DEBUG)

    def log_info(self):
        logging.basicConfig(level=logging.INFO)

    def log_warn(self):
        logging.basicConfig(level=logging.WARNING)

    def read(self, addr):
        data = self.mem[addr]
        logger.debug('Reading {} from [{}]'.format(data, addr))
        return data

    def write(self, addr, data):
        logger.debug('Writing {} to [{}]'.format(data, addr))
        self.mem[addr] = data

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

    def clone(self):
        # The queues can't be deepcopyied, so we need to reset those fields
        # and manually copy the elements to a new instance
        assert isinstance(self._input, Queue)
        assert isinstance(self._output, Queue)
        tmp_input = self._input
        tmp_output = self._output
        self._input = None
        self._output = None
        cp = copy.deepcopy(self)
        self._input = tmp_input
        self._output = tmp_output
        cp._input = Queue()
        cp._output = Queue()
        for e in tmp_input.queue:
            cp._input.put(e)
        for e in tmp_output.queue:
            cp._output.put(e)
        return cp

    def feed_input(self, v):
        assert isinstance(self._input, Queue)
        self._input.put(v)
        self.blocked_on_input = False

    def intercept(self):
        return False

    def run(self, input=None, output=None, steps=0):
        self.init_io(input, output)
        return self._run(steps)

    def run_until_halted(self):
        try:
            while True:
                self.step()
        except MachineHaltedException:
            pass

    def start_async(self, start=0, daemon=False):
        global BLOCK_ON_EOF
        BLOCK_ON_EOF = True
        if self._input is None:
            self.init_io(Queue(), Queue())

        t = threading.Thread(target=self.run_until_halted, daemon=daemon, args=(start,))
        t.start()
        return t

    def _run(self, steps=0):
        if steps:
            while steps > 0 and self.step():
                steps -= 1
        else:
            while self.step():
                pass

        if isinstance(self._output, ReturnSink):
            return self._output.values

    def run_until_next_io(self, input=None, output=None, feed_input=None):
        if self.count == 0:
            self.init_io(input if input else Queue(), output if output else Queue())
        if feed_input:
            for x in feed_input:
                self.feed_input(x)
        while not self.halted and not self.blocked_on_input and self._output.empty():
            self.step()
        if self.halted:
            print('HALT')
        if self.halted or self.blocked_on_input:
            return None
        return self._output.get()

    def read_token(self):
        '''Reads a token from the programs output'''
        s = ''
        while not self.halted and not self.blocked_on_input:
            while not self._output.empty():
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
            self.step()
        return None

    def read_line(self):
        s = ''
        while (not self.halted and not self.blocked_on_input) or not self._output.empty():
            while not self._output.empty():
                c = self._output.get()
                if c == 10:
                    return s
                if c < 32 or c > 127:
                    assert not s
                    return "<%d>" % c
                s += chr(c)
            self.step()
        return None

    def write_line(self, line):
        for c in line:
            self._input.put(ord(c))
        self._input.put(10)

    def step(self):
        assert self.input and self.output
        if self.halted:
            raise MachineHaltedException()
        if not self.intercept():
            opcode = self.read(self.ip)
            param_mode = opcode // 100
            opcode %= 100
            if opcode not in self.opcodes:
                raise UnknownOpcodeException('unknown opcode %d at addr %d' % (opcode, self.ip))
            (instr, mnemonic, length, write_par) = self.opcodes[opcode]
            params = []
            for i in range(1, length):
                x = self.read(self.ip + i)
                if i == write_par:
                    assert param_mode % 10 != 1
                    if param_mode % 10 == 2:
                        x += self.base_ptr
                elif param_mode % 10 == 0:
                    x = self.read(x)
                elif param_mode % 10 == 2:
                    x = self.read(x + self.base_ptr)
                param_mode //= 10
                params.append(x)

            if logger.isEnabledFor(logging.INFO):
                (mnemonic, code) = self.decode(self.ip)
                logger.info('%2d %5d: Executing %s' % (self.prog_id, self.ip, mnemonic))
            self.count += 1
            if SHOW_PROGRESS and self.count % 10000 == 0:
                sys.stderr.write('.')
                sys.stderr.flush()
            self.instr_count[self.ip] += 1
            default_new_ip = self.ip + length
            new_ip = instr(self, *params)
            self.ip = default_new_ip if new_ip is None else new_ip  # Must distinguish 0 and None
        return not self.halted

    def decode(self, addr):
        # Converts instruction to mnemonic
        opcode = self.read(addr)
        param_mode = opcode // 100
        opcode %= 100
        if opcode not in self.opcodes:
            mnemonic = 'DB %d' % opcode
        else:
            (instr, mnemonic, length, write_par) = self.opcodes[opcode]
            mnemonic += ' '
            params = []
            param_modes = []
            for i in range(1, length):
                if i > 1:
                    mnemonic += ', '
                x = self.read(addr + i)
                param_modes.append(param_mode % 10)
                if param_mode % 10 == 0:
                    mnemonic += '(%d)' % x
                    params.append('m%04d' % x)
                elif param_mode % 10 == 2:
                    mnemonic += '(BP+%d)' % x
                    params.append('self.mem[self.base_ptr + %d]' % x)
                else:
                    mnemonic += '#%d' % x
                    params.append(str(x))
                param_mode //= 10

        # Make it into pythonish code
        code = '?'
        if opcode == OPCODE_ADD or opcode == OPCODE_MUL:
            sign = '+' if opcode == 1 else '*'
            code = '%s = %s %s %s' % (params[2], params[0], sign, params[1])
            if params[2] == params[1]:
                code = '%s %s= %s' % (params[2], sign, params[0])
            elif params[2] == params[0]:
                code = '%s %s= %s' % (params[2], sign, params[1])
        elif opcode == OPCODE_IN:
            code = '%s = self.input()' % params[0]
        elif opcode == OPCODE_OUT:
            code = 'self.output(%s)' % params[0]
        elif opcode == OPCODE_JUMP_TRUE or opcode == OPCODE_JUMP_FALSE:
            jump_target = params[1]
            if jump_target[0] == 'm':
                # indirect jumps are more likely to modified by code
                jump_target = '(m%04d)' % (addr + 2)
            inverse = '' if opcode == OPCODE_JUMP_TRUE else 'not '
            code = 'if (%s%s): jump %s' % (inverse, params[0], jump_target)
            if opcode == OPCODE_JUMP_TRUE and param_modes[0] == 1 and int(params[0][0]) != 0:
                code = 'jump %s' % (jump_target)
            if opcode == OPCODE_JUMP_FALSE and param_modes[0] == 1 and int(params[0][0]) == 0:
                code = 'jump %s' % (jump_target)
        elif opcode == OPCODE_LESS_THAN:
            code = '%s = 1 if %s < %s else 0' % (params[2], params[0], params[1])
        elif opcode == OPCODE_EQUALS:
            code = '%s = 1 if %s == %s else 0' % (params[2], params[0], params[1])
        elif opcode == OPCODE_ADD_BP:
            code = 'self.base_ptr += %s' % params[0]
        elif opcode == OPCODE_HALT:
            code = 'self.halted = True\nreturn'

        return (mnemonic, code)

    def show(self, addr, addr_last=False):
        try:
            while addr <= self.last_addr():
                opcode = self.mem[addr] % 100
                opcode_addr = addr
                if opcode in self.opcodes:
                    (asm, code) = self.decode(addr)
                    (_, _, length, _) = self.opcodes[opcode]
                    addr += length
                else:
                    code = 'DB %d' % self.mem[addr]
                    asm = ''
                    addr += 1

                line = '%-30s#%5d: %-20s' % (code, opcode_addr, asm)
                if self.instr_count[opcode_addr]:
                    line += '[%6d]' % (self.instr_count[opcode_addr])
                print(line)
                if opcode == OPCODE_HALT:
                    print()
        except:
            pass

    def hotspots(self):
        # Might want to use show instead
        for i in range(len(self.instr_count)):
            if self.instr_count[i] > 0:
                print('%5d %15d' % (i, self.instr_count[i]))

    def input(self):
        if BLOCK_ON_EOF:
            try:
                self.last_in = self._input.get()
                self.blocked_on_input = False
                return self.last_in
            except Empty:
                # If we have multiple queues as input, this can happen because
                # we have no good way of blocking.
                self.blocked_on_input = True
                return None
        elif CRASH_ON_EOF:
            self.last_in = self._input.get_nowait()
            self.blocked_on_input = False
            return self.last_in
        else:
            try:
                self.last_in = self._input.get_nowait()
                logger.info('%2d        Read %d' % (self.prog_id, self.last_in))
                self.blocked_on_input = False
                return self.last_in
            except Empty:
                logger.info('%2d        Blocked' % (self.prog_id))
                self.blocked_on_input = True
                return None

    def output(self, value):
        self.last_out = value
        self._output.put(value)

    # If an opcode returns a non-value, it's the value of the new IP
    # Otherwise the length of the opcode is added to the IP

    def opcode_add(self, x, y, z):
        self.write(z, x + y)

    def opcode_mul(self, x, y, z):
        self.write(z, x * y)

    def opcode_in(self, x):
        value = self.input()
        if value is None:
            return self.ip
        else:
            self.write(x, value)

    def opcode_out(self, x):
        self.output(x)

    def opcode_jump_true(self, x, y):
        if x != 0:
            return y

    def opcode_jump_false(self, x, y):
        if x == 0:
            return y

    def opcode_less_than(self, x, y, z):
        self.write(z, 1 if x < y else 0)

    def opcode_equals(self, x, y, z):
        self.write(z, 1 if x == y else 0)

    def opcode_add_bp(self, x):
        self.base_ptr += x

    def opcode_exit(self):
        self.halted = True
        return self.ip

    # (function, mnemonic, length, lvalue param)
    # If a function has a variable number of parameters, set length=1
    # and parse the params manually in the instruction
    opcodes = {
        OPCODE_ADD: (opcode_add, 'ADD', 4, 3),
        OPCODE_MUL: (opcode_mul, 'MUL', 4, 3),
        OPCODE_IN: (opcode_in, 'IN', 2, 1),
        OPCODE_OUT: (opcode_out, 'OUT', 2, -1),
        OPCODE_JUMP_TRUE: (opcode_jump_true, 'JMPT', 3, -1),
        OPCODE_JUMP_FALSE: (opcode_jump_false, 'JMPF', 3, -1),
        OPCODE_LESS_THAN: (opcode_less_than, 'LT', 4, 3),
        OPCODE_EQUALS: (opcode_equals, 'EQ', 4, 3),
        OPCODE_ADD_BP: (opcode_add_bp, 'ADD_BP', 2, -1),

        OPCODE_HALT: (opcode_exit, 'HALT', 1, -1),
    }


def wire_up_serial(programs, input, output):
    '''Connects multiple programs with each other in a sequence.'''
    pipes = [Queue() for _ in range(len(programs) - 1)]
    for i in range(len(programs)):
        programs[i].init_io(pipes[i-1] if i > 0 else input, pipes[i] if i < len(programs) - 1 else output)


def parallel_executor(programs):
    '''Executes one instruction at a time across all programs in round robin fashion,
    until they're all halted. Assumes the IO has already been setup.
    Returns the an array, one element per input program. If the output is a ReturnSink
    for a program, the corresponding element will contain that list, otherwise None.
    '''
    global BLOCK_ON_EOF
    BLOCK_ON_EOF = False

    while True:
        all_halted = True
        all_blocked = True
        for prog in programs:
            if not prog.halted:
                prog.step()
                if not prog.blocked_on_input:
                    all_blocked = False
                all_halted = False
        if all_halted:
            break
        if all_blocked:
            raise MachineBlockedException()

    result = []
    for prog in programs:
        if isinstance(prog._output, ReturnSink):
            result.append(prog._output.values)
        else:
            result.append(None)
    return result

def threaded_executor(programs):
    '''Executes all programs in separate threads until they're all halted.
    Returns the an array, one element per input program. If the output is a ReturnSink
    for a program, the corresponding element will contain that list, otherwise None.'''
    global BLOCK_ON_EOF
    BLOCK_ON_EOF = True

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(programs)) as executor:
        result = executor.map(lambda p: p._run(), programs)
    return list(result)


class MachineHaltedException(Exception):
    '''Thrown when trying to execute code while the machine is halted.'''
    pass

class MachineBlockedException(Exception):
    '''Thrown when trying to execute code and the machine is blocked on input.'''
    pass

class ProgramOutOfBoundsException(Exception):
    '''Tried to execute an instruction outside of the programs memory.'''
    pass

class UnknownOpcodeException(Exception):
    '''Tried to execute an unknown opcode.'''
    pass

class ReturnSink(object):
    def __init__(self):
        self.values = []

    def put(self, x):
        self.values.append(x)

class StdoutSink(object):
    def put(self, x):
        if x >= 32 and x < 127:
            sys.stdout.write(chr(x))
        elif x == 10:
            sys.stdout.write('\n')
        else:
            sys.stdout.write(str(x) + '\n')

class StdinSource(object):
    def __init__(self):
        self._queue = Queue()

    def get(self, nowait=False):
        if self._queue.empty():
            s = input()
            if s == '':
                if nowait:
                    raise Empty()
                else:
                    raise MachineBlockedException()
            for c in s:
                self._queue.put(ord(c))
            self._queue.put(10)
        return self._queue.get()

    def get_nowait(self):
        return self.get(True)

class JoinedSource(object):
    '''Gets input from multiple sources.'''
    def __init__(self, queues):
        self.queues = queues

    def get(self):
        # No good way of doing a blocking get here
        return self.get_nowait()

    def get_nowait(self):
        # Need multiprocessing queues here
        for q in self.queues:
            try:
                return q.get_nowait()
            except Empty:
                pass
        raise Empty()

class DuplicateSink(object):
    '''Sends the same output to multiple output sources.'''
    def __init__(self, queues):
        self.queues = queues

    def put(self, x):
        for q in self.queues:
            q.put(x)

class BaseInput(object):
    def get(self):
        raise Exception()  # Should be overridden

    def get_nowait(self):
        return self.get()


class PythonProgram:
    pass

if __name__ == "__main__":
    SHOW_PROGRESS = False
    with open(sys.argv[1], "r") as f:
        code = f.readline()
    prog = Program(code)
    prog.run(input=StdinSource(), output=StdoutSink())
