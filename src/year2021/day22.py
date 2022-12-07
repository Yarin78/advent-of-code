from typing import Tuple
import sys
from yal.util import *
from yal.geo3d import *

lines = [line.strip() for line in sys.stdin.readlines()]

points: List[Tuple[Point, Point, bool]] = []
for line in lines:
    x1,x2,y1,y2,z1,z2 = get_ints(line)
    p1 = Point(x1,y1,z1)
    p2 = Point(x2+1,y2+1,z2+1)

    state = line.startswith("on")
    points.append((p1, p2, state))

def intersect(p1: Point, p2: Point, q1: Point, q2: Point) -> List[Tuple[Point, Point]]:
    x1, x2 = (max(p1.x, q1.x), min(p2.x,q2.x))
    y1, y2 = (max(p1.y, q1.y), min(p2.y,q2.y))
    z1, z2 = (max(p1.z, q1.z), min(p2.z,q2.z))

    if x2 <= x1 or y2 <= y1 or z2 <= z1:        
        return [(p1, p2)]
    
    splits = [
        (Point(p1.x, p1.y, p1.z), Point(x1, p2.y, p2.z)),
        (Point(x2, p1.y, p1.z), Point(p2.x, p2.y, p2.z)),
        (Point(x1, p1.y, p1.z), Point(x2, y1, p2.z)),
        (Point(x1, y2, p1.z), Point(x2, p2.y, p2.z)),
        (Point(x1, y1, p1.z), Point(x2, y2, z1)),
        (Point(x1, y1, z2), Point(x2, y2, p2.z)),
    ]
    
    return [(b1, b2) for (b1, b2) in splits if b1.x<b2.x and b1.y<b2.y and b1.z<b2.z]


def count_rec(p1: Point, p2: Point, current: int):
    global points
    if current == len(lines):
        return (p2.x-p1.x)*(p2.y-p1.y)*(p2.z-p1.z)

    q1,q2,_ = points[current]
    
    sum = 0
    for block in intersect(p1, p2, q1, q2):
        sum += count_rec(block[0], block[1], current+1)
    return sum    

print(sum(count_rec(p1, p2, i+1) for i, (p1,p2,state) in enumerate(points) if state))
