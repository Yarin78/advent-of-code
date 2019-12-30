import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from intcode.intcode import *
from aocd import data, submit
import random

lines = data.strip().split('\n')
prog = Program(data)
prog.init_io(Queue(), Queue())

num_empty = 0

def get_line(echo=False):
    global num_empty
    s = prog.read_line()
    if s is None:
        return None
    s = s.strip()
    if echo:
        print('>> ', s)
    if s:
        num_empty = 0
        return s
    num_empty += 1
    if prog.halted:
        print('HALT')
        exit(0)
    if num_empty < 3:
        return ''
    return ''

def is_forbidden_item(item_name):
    if item_name in ['giant electromagnet', 'escape pod', 'infinite loop', 'photons', 'molten lava']:
        return True
    return False

commands = [
    "north",
    "take astronaut ice cream",
    "south",
    "west",
    "take mouse",
    "north",
    "take ornament",
    "west",
    "north",
    "take easter egg",
    "north",
    "west",
    "north",
    "take wreath",
    "south",
    "east",
    "south",
    "east",
    "take hypercube",
    "north",
    "east",
    "take prime number",
    "west",
    "south",
    "west",
    "south",
    "west",
    "take mug",
    "west",
]

def wait_until_cmd():
    text = []
    while True:
        s = get_line()
        if s is None:
            break
        text.append(s)
        if s == 'Command?':
            break
    return '\n'.join(text)

for i in range(len(commands)):
    cmd = commands[i]
    wait_until_cmd()
    prog.write_line(cmd)

wait_until_cmd()

items = ["astronaut ice cream",
"mouse",
"ornament",
"easter egg",
"wreath",
"hypercube",
"prime number",
"mug"]

inv = items[:]

for i in range(256):
    for j in range(8):
        if (2**j) & i:
            if items[j] not in inv:
                prog.write_line("take %s" % items[j])
                inv.append(items[j])
                wait_until_cmd()
        else:
            if items[j] in inv:
                prog.write_line("drop %s" % items[j])
                inv.remove(items[j])
                wait_until_cmd()

    prog.write_line('north')
    text = wait_until_cmd()
    if 'Alert!' not in text:
        print(inv)
        print(text)
        exit(0)
