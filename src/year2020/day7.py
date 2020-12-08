import sys

g = {"%s %s" % (t[0], t[1]): [(int(t[i]), "%s %s" % (t[i+1], t[i+2])) for i in range(4, len(t), 4)] if t[4] != "no" else [] for t in map(lambda x: x.split(), sys.stdin.readlines())}

def p1(cur):
    return cur=="shiny gold" or any(p1(c) for (m, c) in g[cur])

def p2(cur):
    return sum(m * (1+p2(c)) for (m, c) in g[cur])

print(sum(p1(k) for k in g.keys())-1, p2("shiny gold"))

