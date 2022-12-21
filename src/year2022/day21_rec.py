import sys

m = {
    line[0:4]: (line[6:10], line[11], line[13:17]) if len(line) == 18 else int(line[6:])
    for line in sys.stdin.readlines()
}

def inverse(a, op, b):
    new_op = "-+/*"["+-*/".find(op)]
    return eval(f"{a}{new_op}{b}")

def rec(name):
    #return m[name] if isinstance(m[name], int) else eval(f"{rec(m[name][0])}{m[name][1]}{rec(m[name][2])}")
    if not isinstance(m[name], tuple):
        return m[name]
    left, right = rec(m[name][0]), rec(m[name][2])
    return None if left is None or right is None else eval(f"{left}{m[name][1]}{right}")


def rec2(name, desired):
    if name == "humn":
        return desired
    a, op, b = m[name]
    left, right = rec(a), rec(b)
    if left is None:
        if op == '+':
            return rec2(a, desired - right)
        elif op == '-':
            return rec2(a, right + desired)
        elif op == '/':
            return rec2(a, right * desired)
        else:
            return rec2(a, desired // right)
    else:
        if op == '+':
            return rec2(b, desired - left)
        elif op == '-':
            return rec2(b, left - desired)
        elif op == '/':
            return rec2(b, left // desired)
        else:
            return rec2(b, desired // left)

print("Part 1:", int(rec("root")))
m["root"] = (m["root"][0], "-", m["root"][2])
m["humn"] = None
print("Part 2:", int(rec2("root", 0)))
