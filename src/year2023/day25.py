import sys
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.nxgraph import *
from yal.geo2d import *
import networkx as nx

lines = [line.strip() for line in sys.stdin.readlines()]

gg = nx.Graph()

for line in lines:
    p1, p2 = line.split(':')
    for q in p2.strip().split(' '):
        gg.add_edge(p1, q)

cut_edges = nx.minimum_edge_cut(gg)

# show_graph(gg, edge_colors={edge: "green" for edge in cut_edges})

gg.remove_edges_from(cut_edges)

ans = 1
for comp in nx.connected_components(gg):
    ans *= len(comp)

print(ans)
