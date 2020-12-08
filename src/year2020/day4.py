import sys
import re
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from aocd import data, submit

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)

lines = data.strip().split('\n')

req_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
ranges = {
    "byr": (1920, 2002),
    "iyr": (2010, 2020),
    "eyr": (2020, 2030),
    "hgt_cm": (150, 193),
    "hgt_in": (59, 76),
}

def is_valid(fields_org):
    fields = dict(fields_org)
    if "cid" in fields:
        del fields["cid"]
    if not all(f in fields for f in req_fields):
        return False
    if fields["hgt"].endswith("cm"):
        fields["hgt_cm"] = fields["hgt"][0:-2]
    elif fields["hgt"].endswith("in"):
        fields["hgt_in"] = fields["hgt"][0:-2]
    else:
        return False

    for name, (min, max) in ranges.items():
        if name in fields and (int(fields[name]) < min or int(fields[name]) > max):
            return False

    if not re.match("^#[0-9a-z]{6}$", fields["hcl"]):
        return False

    if fields["ecl"] not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
        return False
    if not re.match("^[0-9]{9}$", fields["pid"]):
        return False

    return True

num_valid = 0
fields = {}
has_duplicates = False
lines.append("")

for line in lines:
    if line == "":
        if not has_duplicates and is_valid(fields):
            num_valid += 1
        fields = {}
        has_duplicates = False
    else:
        parts = line.split(' ')
        for p in parts:
            (field_name, field_value)  = p.split(':')
            if field_name in fields:
                has_duplicates = True
            fields[field_name] = field_value

print(num_valid)
