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

# Make sure ~/.config/aocd/token is correct! (Application tab -> Cookies)
# scanner = Scanner(sys.stdin)
lines = [line.strip() for line in sys.stdin.readlines()]
# Split input into an array of array of lines, split by empty line
# sections = split_lines(lines)

# disk = []
# for i, c in enumerate(lines[0]):
#     if i % 2 == 0:
#         for x in range(int(c)):
#             disk.append(i // 2)
#     else:
#         for x in range(int(c)):
#             disk.append(-1)

# # print(disk)

# i = 0
# j = len(disk) - 1
# assert disk[j] >= 0
# while i < j:
#     if disk[i] < 0:
#         amount_free = 0
#         while disk[i+amount_free] < 0:
#             amount_free += 1
#         last_file_size = 0
#         while disk[j] == disk[j-last_file_size]:
#             last_file_size += 1
#         if last_file_size <= amount_free:
#             print(f"move file {disk[j]} of size {last_file_size} to pos {i}")
#             for k in range(last_file_size):
#                 disk[i] = disk[j]
#                 disk[j] = -1
#                 i += 1
#                 j -= 1
#         else:
#             print(f"skip file {disk[j]}")
#             j -= last_file_size
#         while i < j and disk[j] == -1:
#             j -= 1
#     else:
#         i += 1

# ans = 0
# for i, c in enumerate(disk):
#     if c >= 0:
#         ans += i*c
# print(ans)
# print(disk)

@dataclass
class File:
    index: int
    pos: int
    size: int

@dataclass
class FreeSpace:
    pos: int
    size: int

files = []  # (index, pos, size)
free_space = [] # (pos, size)

pos = 0
for i, d in enumerate(lines[0]):
    c = int(d)
    if i % 2 == 0:
        files.append(File(i//2, pos, c))
        pos += c
    else:
        free_space.append(FreeSpace(pos, c))
        pos += c

print(files)
print(free_space)

for i in range(len(files)):
    ci = len(files) - i - 1
    j = 0
    # print(f"Trying to move file {ci}")
    while j < len(free_space) and free_space[j].size < files[ci].size:
        j += 1
    if j < len(free_space) and free_space[j].pos < files[ci].pos:
        print(f"Moved file {ci} to position {free_space[j].pos}")
        files[ci].pos = free_space[j].pos
        free_space[j].pos += files[ci].size
        free_space[j].size -= files[ci].size

ans = 0
for i, f in enumerate(files):
    for c in range(f.size):
        ans += (f.pos + c) * i

print(ans)
