from collections import defaultdict
from queue import Queue, Empty
import concurrent.futures
import threading
import functools
import logging
import sys
import copy
from yal.util import tokenize, tokenize_minus, intify

logger = logging.getLogger(__name__)

# Behaviour when trying to read and there is nothing on the input
# Default is to pause the machine (and not update the IP)
CRASH_ON_EOF = False   # Raise exception if trying to read from input when there is no data
BLOCK_ON_EOF = False   # Block calling thread if trying to read from input when there is no data

SHOW_PROGRESS = True

# The parameters are called x, y, z
OP_NOP = "nop"       # pass
OP_ACC = "acc"       # acc += x
OP_JMP = "jmp"       # pc += x
OP_DEBUG = "debug"   # outputs acc

# Not defined yet
OP_IN = "in"            #
OP_OUT = "out"          #
OP_JUMP_TRUE = "jt"     #
OP_JUMP_FALSE = "jf"    #
OP_LESS_THAN = "lt"     #
OP_EQUALS = "eq"        #
OP_HALT = "halt"        #


class Program(object):

    def __init__(self, code, prog_id=0):
        self.factory_settings = code[:]
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
        self.instr_count = [0]*(len(self.factory_settings)+1)
        self.halted = False
        self.blocked_on_input = False
        self.last_in = 0
        self.last_out = 0
        self.acc = 0

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

    def read_instr(self, addr):
        # Not sure yet if the instructions are in memory or not,
        # so read all instructions from the "factory setting"
        if addr == len(self.factory_settings):
            return OP_HALT
        return self.factory_settings[addr]

    def parse_instr(self, instr):
        tokens = tokenize_minus(instr)
        return tokens[0], intify(tokens[1:])

    def write(self, addr, data):
        logger.debug('Writing {} to [{}]'.format(data, addr))
        self.mem[addr] = data

    def init_io(self, input=None, output=None):
        if input is None:
            self._input = StdinSource()
            # print('Input from stdin')
        elif isinstance(input, list):
            self._input = Queue()
            for x in input:
                self._input.put(x)
        else:
            self._input = input

        if output is None:
            self._output = StdoutSink()
            # print('Output to stdout')
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
            line = self.read_instr(self.ip)
            operation, arguments = self.parse_instr(line)

            if operation not in self.operations:
                raise UnknownOpcodeException(f'unknown operation {operation} at addr {self.ip}')

            op = self.operations[operation]

            if logger.isEnabledFor(logging.INFO):
                logger.info('%2d %5d: Executing %s' % (self.prog_id, self.ip, line))
            self.count += 1
            if SHOW_PROGRESS and self.count % 10000 == 0:
                sys.stderr.write('.')
                sys.stderr.flush()
            self.instr_count[self.ip] += 1
            default_new_ip = self.ip + 1
            new_ip = op(self, *arguments)
            self.ip = default_new_ip if new_ip is None else new_ip  # Must distinguish 0 and None
        return not self.halted

    def show(self, addr, addr_last=False):
        # TODO: Needs changing once the memory layout is figured out
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

    # If an operation returns a non-value, it's the value of the new IP
    # Otherwise IP will increase by 1

    def op_acc(self, x):
        self.acc += x

    def op_nop(self, x):
        pass

    def op_jmp(self, x):
        return self.ip + x

    def op_in(self, x):
        value = self.input()
        if value is None:
            return self.ip
        else:
            self.write(x, value)

    def op_out(self, x):
        self.output(x)

    def op_jump_true(self, x, y):
        if x != 0:
            return y

    def op_jump_false(self, x, y):
        if x == 0:
            return y

    def op_eq(self, x, y, z):
        self.write(z, 1 if x < y else 0)

    def op_less_than(self, x, y, z):
        self.write(z, 1 if x < y else 0)

    def op_equals(self, x, y, z):
        self.write(z, 1 if x == y else 0)

    def op_halt(self):
        self.halted = True
        return self.ip

    def op_debug(self, x):
        print('DEBUG', x)

    operations = {
        OP_NOP: op_nop,
        OP_ACC: op_acc,
        OP_JMP: op_jmp,
        OP_DEBUG: op_debug,
        OP_IN: op_in,
        OP_OUT: op_out,
        OP_JUMP_TRUE: op_jump_true,
        OP_JUMP_FALSE: op_jump_false,
        OP_LESS_THAN: op_less_than,
        OP_EQUALS: op_eq,
        OP_HALT: op_halt
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
