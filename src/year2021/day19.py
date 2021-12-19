import sys
from collections import defaultdict
from typing import Iterable
from yal.util import *
from yal.geo3d import Point

lines = [line.strip() for line in sys.stdin.readlines()]

MIN_COMMON = 12

scanners = []
cur = []

for line in lines:
    if ',' in line:
        x,y,z = get_ints(line)
        cur.append(Point(x,y,z))
    if '---' in line:
        if cur:
            scanners.append(cur)
        cur = []

scanners.append(cur)

def rotations(points: List[Point]) -> List[List[Point]]:
    return transpose_matrix([p.rotations() for p in points])

n = len(scanners)


def overlaps(scanner1: List[Point], scanner2: List[Point]) -> Optional[Point]:
    delta_cnt = defaultdict(int)
    # This may overcount
    for p0 in scanner1:
        for p1 in scanner2:
            delta_cnt[p1-p0] += 1

    for delta, cnt in delta_cnt.items():
        if cnt >= MIN_COMMON:
            actual_cnt = 0
            for p0 in scanner1:
                if p0+delta in scanner2:
                    actual_cnt += 1

            if actual_cnt >= MIN_COMMON:
                return delta

    return None


beacons = set()
scanner_pos = set()

def dfs(cur_scanner_i, cur_scanner_rot, cur_scanner_points, offset, seen_scanners):
    global n, scanners
    print(f"at scanner {cur_scanner_i} with offset {offset}")
    for i in range(n):
        if i not in seen_scanners:
            for rot_num, rot in enumerate(rotations(scanners[i])):
                delta = overlaps(cur_scanner_points, rot)
                if delta is not None:
                    for p in rot:
                        beacons.add(p - (offset + delta))
                    print(f"scanner {cur_scanner_i} and {i} overlaps with rot {cur_scanner_rot}, {rot_num} and delta {str(delta)}")
                    scanner_pos.add(offset+delta)
                    seen_scanners.add(i)
                    dfs(i, rot_num, rot, offset+delta, seen_scanners)
                    break


seen = set([0])
scanner_pos.add(Point(0,0,0))
for p in scanners[0]:
    beacons.add(p)

dfs(0, 0, scanners[0], Point(0, 0, 0), seen)

print(f"# beacons {len(beacons)}")
print(f"dist {max(abs(p1.x-p2.x)+abs(p1.y-p2.y)+abs(p1.z-p2.z) for p1 in scanner_pos for p2 in scanner_pos)}")
