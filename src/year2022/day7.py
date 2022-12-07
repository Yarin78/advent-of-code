import sys
from dataclasses import dataclass
import os.path
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
# scanner = Scanner(sys.stdin)
lines = [line.strip() for line in sys.stdin.readlines()]
# Split input into an array of array of lines, split by empty line
# sections = split_lines(lines)

directories: Dict[str, "Dir"] = {}


@dataclass
class Dir:
    cur_dir: str
    files: List[Tuple[str, int]]
    dirs: List[str]

    def dir_size(self):
        global directories
        res = 0
        for file in self.files:
            res += file[1]
        for dir in self.dirs:
            res += directories[os.path.join(self.cur_dir, dir)].dir_size()
        return res


cur_dir = ""
line_no = 0
while line_no < len(lines):
    line = lines[line_no]
    line_no += 1
    if line[0] == '$':
        cmd = line[2:]
        if cmd == "cd /":
            cur_dir = ""
        elif cmd == "cd ..":
            cur_dir = os.path.dirname(cur_dir)
        elif cmd.startswith("cd "):
            cur_dir = os.path.join(cur_dir, cmd[3:])
        else:
            assert cmd == "ls"
            files = []
            dirs = []
            while line_no < len(lines) and lines[line_no][0] != '$':
                a, b = lines[line_no].split(' ')
                if a != "dir":
                    files.append((b, int(a)))
                else:
                    dirs.append(b)
                line_no += 1
            assert cur_dir not in directories
            directories[cur_dir] = Dir(cur_dir, files, dirs)


part1 = 0
for dir in directories.values():
    if dir.dir_size() <= 100000:
        part1 += dir.dir_size()
print(part1)

total_disk = 70000000
current_used = directories[''].dir_size()
required = 30000000

best = 999999999999999999
best_dir = "--"

res = 0
for dir in directories.keys():
    ds = directories[dir].dir_size()
    if total_disk-(current_used - ds) >= required and ds < best:
        best = ds
        best_dir = dir

print(best_dir, best)
print("total number of dirs:", len(directories))