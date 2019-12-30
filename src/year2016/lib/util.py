import re

_integer_pattern = re.compile("-?[0-9]+")

def get_ints(line):
    return [int(m) for m in _integer_pattern.findall(line)]
