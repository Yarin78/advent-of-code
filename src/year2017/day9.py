import sys

for line in sys.stdin.readlines():
    line=line.strip()
    print(line)
    score = 0
    depth = 0
    removed = 0
    i = 0
    garbage = False
    while i < len(line):
        if garbage:
            if line[i] == '>':
                garbage = False
            elif line[i] == '!':
                i += 1
            else:
                removed += 1
        elif line[i] == '{':
            depth += 1
            score += depth
        elif line[i] == '<':
            garbage = True
        elif line[i] == '}':
            depth -= 1
        elif line[i] == ',':
            pass
        else:
            assert False
        i += 1
    assert depth == 0
    print(score)
    print(removed)
