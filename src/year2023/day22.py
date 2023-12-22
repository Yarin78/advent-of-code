import sys
from collections import defaultdict
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo3d import *

DOWN = Point(0,0,-1)

lines = [line.strip() for line in sys.stdin.readlines()]

taken = {} # Point3D -> shape num

def can_place(shape: Shape):
    return not any(p in taken or p.z <= 0 for p in shape.points)

is_supporting = defaultdict(set)  # shape num -> shape nums resting on it
supported_by = defaultdict(set) # shape num -> shape nums it rests on

shapes_falling: List[Shape] = []
for line in lines:
    ps1, ps2 = line.split('~')
    p1 = Point(*map(int, ps1.split(',')))
    p2 = Point(*map(int, ps2.split(',')))
    shapes_falling.append(Shape.from_inclusive_coords(p1, p2))

shapes_falling.sort(key=lambda shape: min(p.z for p in shape.points))

shapes: List[Shape] = []
for i, shape in enumerate(shapes_falling):
    while can_place(shape + DOWN):
        shape += DOWN

    for p in shape.points:
        taken[p] = i
        below = taken.get(p+DOWN)
        if below is not None and below != i:
            supported_by[i].add(below)
            is_supporting[below].add(i)

    shapes.append(shape)

part1 = 0
part2 = 0
for i, candidate_shape in enumerate(shapes):
    if all(len(supported_by[k]) != 1 for k in is_supporting[i]):
        part1 += 1

    remaining: Set[int] = set()
    for j, check_shape in enumerate(shapes):
        if i == j:
            continue
        if len(supported_by[j]) == 0 or any(x in remaining for x in supported_by[j]):
            remaining.add(j)
        else:
            part2 += 1

print(part1)  # 448
print(part2)  # 57770
