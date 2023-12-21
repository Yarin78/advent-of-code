from dataclasses import dataclass
import sys
import os
import graphviz

from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

lines = [line.strip() for line in sys.stdin.readlines()]

@dataclass
class Module:
    id: str
    dest: List[str]

@dataclass
class FlipFlopModule(Module):
    state: bool # False = low

@dataclass
class ConjunctionModule(Module):
    last_input: Dict[str, bool]

@dataclass
class BroadcastModule(Module):
    pass

@dataclass
class OutputModule(Module):
    pass

modules: Dict[str, Module] = {}  # id -> module
for line in lines:
    src, dests = line.split(' -> ')
    id = src[1:]
    if src[0] == '%':
        module = FlipFlopModule(id, dests.split(', '), False)
    elif src[0] == '&':
        module = ConjunctionModule(id, dests.split(', '), {})
    else:
        module = BroadcastModule("broadcaster", dests.split(', '))

    modules[module.id] = module

modules["output"] = OutputModule("output", [])

for m in modules.values():
    for dest in m.dest:
        if dest in modules and isinstance(modules[dest], ConjunctionModule):
            modules[dest].last_input[m.id] = False

presses = 0
rx_cycles = {}

def go():
    global presses, rx_cycles
    q = []
    q.append(("broadcaster", False, "button"))
    num_lo = 0
    num_hi = 0
    while q:
        (id, signal, src) = q.pop(0)
        if signal:
            num_hi += 1
        else:
            num_lo += 1
        if id not in modules:
            continue
        mod = modules[id]
        if "rx" in mod.dest and signal and src not in rx_cycles:
            rx_cycles[src] = presses

        if isinstance(mod, BroadcastModule):
            for d in mod.dest:
                q.append((d, signal, id))
        elif isinstance(mod, FlipFlopModule):
            if not signal:
                mod.state = not mod.state
                for d in mod.dest:
                    q.append((d, mod.state, id))
        elif isinstance(mod, ConjunctionModule):
            assert src is not None
            mod.last_input[src] = signal
            all_hi = all(mod.last_input.values())
            for d in mod.dest:
                q.append((d, not all_hi, id))

    return num_lo, num_hi

def show(presses):
    dot = graphviz.Digraph()
    for m in modules.values():
        node_color="black"
        if isinstance(m, FlipFlopModule):
            if m.state:
                node_color="green" # Hi
            else:
                node_color="red" # Low
        elif isinstance(m, ConjunctionModule):
            node_color="black"
        dot.node(m.id, color=node_color)

        for dest in m.dest:
            edge_color = "black"
            if isinstance(modules.get(dest), ConjunctionModule):
                if modules[dest].last_input[m.id]:
                    edge_color = "green" # Hi
                else:
                    edge_color = "red" # Low

            dot.edge(m.id, dest, color=edge_color)
    dot.render(f'viz/state_{presses:04}', cleanup=True)


sum_lo = 0
sum_hi = 0
for i in range(1000):
    lo, hi = go()
    sum_lo += lo
    sum_hi += hi
print(sum_lo * sum_hi)

for mod in modules.values():
    if isinstance(mod, ConjunctionModule):
        mod.last_input = {k: False for k in mod.last_input.keys()}
    elif isinstance(mod, FlipFlopModule):
        mod.state = False

while presses < 4096:
    presses += 1
    go()


print(math.lcm(*rx_cycles.values()))
