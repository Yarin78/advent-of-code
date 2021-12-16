import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

lines = [line.strip() for line in sys.stdin.readlines()]

hex_map = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'}


bin_stream = ""
bin_pos = 0

def unpack(rec=False):
    global bin_pos, bin_stream
    packet_version = int(bin_stream[bin_pos:bin_pos+3], 2)
    packet_type = int(bin_stream[bin_pos+3:bin_pos+6], 2)
    bin_pos += 6
    if packet_type == 4:
        bin_value = 0
        rep = int(bin_stream[bin_pos:bin_pos+5], 2)
        bin_pos += 5
        while True:
            bin_value = bin_value * 16 + rep % 16
            if rep // 16 == 0:
                break
            rep = int(bin_stream[bin_pos:bin_pos+5], 2)
            bin_pos += 5

        return {
            "version": packet_version,
            "type": packet_type,
            "literal": bin_value
        }

    op_type = int(bin_stream[bin_pos], 2)
    bin_pos += 1

    if op_type == 0:
        tot_bits = int(bin_stream[bin_pos:bin_pos+15], 2)
        bin_pos += 15
        bin_pos_done = bin_pos + tot_bits
        sub_packets = []
        while bin_pos < bin_pos_done:
            sub_packets.append(unpack())
        return {
            "version": packet_version,
            "type": packet_type,
            "length_type": 0,
            "sub_packets": sub_packets
        }
    else:
        num_sub_packets = int(bin_stream[bin_pos:bin_pos+11], 2)
        bin_pos += 11
        sub_packets = []
        for _ in range(num_sub_packets):
            sub_packets.append(unpack())

        return {
            "version": packet_version,
            "type": packet_type,
            "length_type": 1,
            "sub_packets": sub_packets
        }


hex_stream = lines[0]

bin_pos = 0
bin_stream = ""
for c in hex_stream:
    bin_stream += hex_map[c]

def version_sum(expr):
    t = expr["version"]
    if "sub_packets" in expr:
        for sub_packet in expr["sub_packets"]:
            t += version_sum(sub_packet)
    return t

def evaluate(expr) -> int:
    et = expr["type"]
    sub_packets = expr.get("sub_packets", [])
    if et == 0:
        return sum(evaluate(sp) for sp in sub_packets)
    if et == 1:
        prod = 1
        for sp in sub_packets:
            prod *= evaluate(sp)
        return prod
    if et == 2:
        return min(evaluate(sp) for sp in sub_packets)
    if et == 3:
        return max(evaluate(sp) for sp in sub_packets)
    if et == 4:
        return expr["literal"]
    if et == 5:
        return 1 if evaluate(sub_packets[0]) > evaluate(sub_packets[1]) else 0
    if et == 6:
        return 1 if evaluate(sub_packets[0]) < evaluate(sub_packets[1]) else 0
    if et == 7:
        return 1 if evaluate(sub_packets[0]) == evaluate(sub_packets[1]) else 0

    assert False

expr = unpack()

print(version_sum(expr))
print(evaluate(expr))
