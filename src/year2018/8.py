import sys

data = map(lambda x:int(x), sys.stdin.readline().strip().split(' '))
ptr = 0

def sum():
    global data, ptr
    no_trees = data[ptr]
    ptr += 1
    no_metadata = data[ptr]
    ptr += 1
    s = 0
    child_values = [0]
    for i in range(no_trees):
        child_values.append(sum())
    if no_trees == 0:
        for i in range(no_metadata):
            s += data[ptr]
            ptr += 1
    else:
        for i in range(no_metadata):
            q = data[ptr]
            if q < len(child_values):
                s += child_values[q]
            ptr += 1

    return s

print sum()
