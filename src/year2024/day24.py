from functools import cache
import sys
from dataclasses import dataclass
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

def read_input(section):
    input = {}
    for line in section:
        var, val = line.split(':')
        input[var] = int(val.strip())
    return input

def read_gates(section):
    gate_by_output = {}
    for gate in section:
        a, op, b, _, c = gate.split(' ')
        assert c not in gate_by_output
        gate_by_output[c] = (a, op, b)
    return gate_by_output


def create_adder(num_bits):
    section = []
    section.append("x00 XOR y00 -> z00")

    section.append("x00 AND y00 -> b01")
    section.append("x01 XOR y01 -> d01")
    section.append("b01 XOR d01 -> z01")

    for bit in range(2, num_bits):
        section.append(f"x{bit-1:02} AND y{bit-1:02} -> a{bit:02}")
        section.append(f"x{bit:02} XOR y{bit:02} -> b{bit:02}")
        section.append(f"b{bit-1:02} AND d{bit-1:02} -> c{bit:02}")
        section.append(f"a{bit:02} OR c{bit:02} -> d{bit:02}")
        section.append(f"b{bit:02} XOR d{bit:02} -> z{bit:02}")

    return read_gates(section)


def generate_input(x, y, bits):
    input = {}
    for i in range(bits):
        input[f"x{i:02}"] = (x >> i) & 1
        input[f"y{i:02}"] = (y >> i) & 1
    return input


# @cache
def evaluate(name, input):
    if name in input:
        return input[name]
    g = gates[name]
    match g[1]:
        case 'AND':
            res = evaluate(g[0], input) & evaluate(g[2], input)
        case 'OR':
            res = evaluate(g[0], input) | evaluate(g[2], input)
        case 'XOR':
            res = evaluate(g[0], input) ^ evaluate(g[2], input)

    # print(f"{min(g[0], g[2])} {g[1]} {max(g[0], g[2])} -> {name}")
    return res


def get_output(input, gates):
    i = 0
    output = 0
    while f"z{i:02}" in gates:
        if evaluate(f"z{i:02}", input):
            output += 1 << i
        i += 1
    return output

lines = [line.strip() for line in sys.stdin.readlines()]
sections = split_lines(lines)

input = read_input(sections[0])
gates = read_gates(sections[1])

def swap(a, b):
    tmp = gates[a]
    gates[a] = gates[b]
    gates[b] = tmp

swap("z10", "gpr")
swap("z21", "nks")
swap("z33", "ghp")
swap("cpm", "krs")


correct_gates = create_adder(45)

testing = ['cmn', 'cpm', 'dcd', 'frb', 'ftb', 'gbn', 'gnm', 'jhd', 'krb', 'krs', 'mhr', 'mph', 'ndp', 'pcg', 'ptf', 'qcm', 'qdc', 'qgm', 'qkb', 'sbj', 'sdk', 'sqw', 'vvm', 'wdg', 'wpg', 'wtc', 'z39', 'z40', 'z41', 'z42', 'z43', 'z44', 'z45']

def verify():
    gate_mapping = {}  # from generated name to actual input

    for i in range(46):
        gate_mapping[f"x{i:02}"] = f"x{i:02}"
        gate_mapping[f"y{i:02}"] = f"y{i:02}"
        gate_mapping[f"z{i:02}"] = f"z{i:02}"

    unmapped = set(gates.keys())

    for c, (a, op, b) in correct_gates.items():
        # if c == 'a39':
        #     print(sorted(unmapped))
        #     exit(0)
        found = False
        if a in gate_mapping and b in gate_mapping:
            for c2, (a2, op2, b2) in gates.items():
                if ((gate_mapping[a] == a2 and gate_mapping[b] == b2) or (gate_mapping[a] == b2 and gate_mapping[b] == a2)) and (op == op2):
                    # print("Match", c, c2)
                    gate_mapping[c] = c2
                    unmapped.discard(c2)
                    found = True
                    break
        if not found:
            print(f"Failed to find {a} {op} {b} -> {c}")
            return False

    return True
        # break
# print(sorted(unmapped))

# for k1, k2 in itertools.combinations(testing, 2):
#     swap(k1, k2)
#     if verify():
#         print("FOUND", k1, k2)
#         exit(0)
#     swap(k1, k2)

assert verify()


print(",".join(sorted(["z10", "gpr", "z21", "nks", "z33", "ghp", "cpm", "krs"])))



# for a in range(130):
#     for b in range(150):
#         input = generate_input(a, b, 8)
#         assert (a + b) % 256 == get_output(input, gates)
#         # print(f"{a} + {b} = {get_output(input, gates)}")

# output = []
# for c, (a, op, b) in gate_by_output.items():
#     s = f"{a} {op} {b} -> {c}" if a < b else f"{b} {op} {a} -> {c}"
#     output.append(s)
# for line in sorted(output):
#     print(line)


# gen_adder(8)
