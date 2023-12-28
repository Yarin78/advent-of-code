import sys
from collections import defaultdict
from queue import Queue
from typing import Tuple, List, Optional

SHOW_SOLUTIONS = True

def scanline_merge_components(
    previous_row: List[Optional[int]], current_row: List[bool]
) -> Tuple[List[Optional[int]], List[int], List[int]]:
    '''
    Helper function for merging components across two rows in a grid.
    previous_row contains a list of components id's for each cell
    (None if the cell is empty) in the previous row.
    current_row contains if a cell is empty (false) or not (true)
    in the current row.
    Returns a tuple containing:
      * a similar list of components id's for the current row,
      * a list of original component id's that were dropped.
      * a list of component id's that were introduced.
    Components can only be connected horizontally and vertically, not diagonally.

    Example (N = None, T = True, F = False)
    previous_row = [0, N, 1, 1, 1, N, N, N, 1, N, 2]
    current_row =  [T, T, T, F, F, F, T, F, T, F, F]

    Returns       ([0, 0, 0, N, N, N, 1, N, 0, N, N], [2], [1])
    '''

    assert len(previous_row) == len(current_row)

    comp_column_map = defaultdict(list)
    for i, comp in enumerate(previous_row):
        if comp is not None:
            comp_column_map[comp].append(i)

    n = len(previous_row)
    seen = [False] * n
    output: List[Optional[int]] = [None] * n
    new_components = []
    current_comp = 0

    for i in range(n):
         if current_row[i] and not seen[i]:
            q = Queue()
            new_component = True
            q.put(i)
            seen[i] = True
            while not q.empty():
                x = q.get()
                output[x] = current_comp
                if x+1 < n and current_row[x+1] and not seen[x+1]:
                    q.put(x+1)
                    seen[x+1] = True
                if previous_row[x] is not None:
                    new_component = False
                    for j in comp_column_map[previous_row[x]]:
                        if current_row[j] and not seen[j]:
                            q.put(j)
                            seen[j] = True
                    comp_column_map[previous_row[x]].clear()

            if new_component:
                new_components.append(current_comp)
            current_comp += 1

    return (output, sorted(k for k, v in comp_column_map.items() if v), new_components)


def valid_pattern(row1: List[Optional[int]], row2: List[bool]):
    s1 = ''.join('#' if comp is not None else '.' for comp in row1)
    s2 = ''.join('#' if filled else '.' for filled in row2)
    assert len(s1) == 3 and len(s2) == 3

    def matches(p1: str, p2: str):
        n = len(s1)
        pn = len(p1)
        for i in range(n - pn + 1):
            if s1[i:i+pn] == p1 and s2[i:i+pn] == p2:
                return True
            if s2[i:i+pn] == p1 and s1[i:i+pn] == p2:
                return True
        return False

    if matches('.#', '#.'):
        return False
    if matches('##', '##'):
        return False

    if matches('###', '.#.'):
        return False
    if matches('...', '.#.'):
        return False


    return True


def valid_final_row(components: List[Optional[int]], up: List[bool]):
    if 1 in components:
        return False

    n = len(components)
    for i in range(n):
        if components[i] is None:
            continue
        has_left = i > 0 and components[i-1] is not None
        has_right = i+1 < n and components[i+1] is not None

        if not has_left and not has_right:
            return False
        if not has_left and has_right and not up[i]:
            return False
        if has_left and not has_right and not up[i]:
            return False

    return True

def validate_up(row1: List[Optional[int]], row2: List[Optional[int]], up: List[bool]):
    n = len(row1)
    for i in range(n):
        if row1[i] is None:
            continue

        if (i == 0 or row1[i-1] is None) and i+1 < n and row1[i+1] is not None:
            if up[i] == (row2[i] is not None):
                return False

        if (i == n-1 or row1[i+1] is None) and i-1 >= 0 and row1[i-1] is not None:
            if up[i] == (row2[i] is not None):
                return False
    return True

current_grid = []

def show():
    for row in current_grid:
        print(row)
    print()

def count_grid_loops(components: List[Optional[int]], up: List[bool], rows_left: int):
    if rows_left == 0:
        return 0

    global current_grid

    started = any(x is not None for x in components)

    n = len(components)
    current_row = [False] * n

    def rec(x: int):
        nonlocal n, started
        if x == 2 and not valid_pattern([None, *components[x-2:x]], [False, *current_row[x-2:x]]):
            return 0
        if x >= 3 and not valid_pattern(components[x-3:x], current_row[x-3:x]):
            return 0

        if x == n:
            if not valid_pattern([*components[x-2:x], None], [*current_row[x-2:x], False]):
                 return 0

            if SHOW_SOLUTIONS:
                current_grid.append(''.join('#' if filled else '.' for filled in current_row))

            merged_components, lost_components, _ = scanline_merge_components(components, current_row)
            try:
                if not validate_up(components, merged_components, up):
                    return 0

                if len(lost_components) > 0:
                    return 0

                new_up = [merged_components[i] is not None and components[i] is not None for i in range(n)]

                if started and valid_final_row(merged_components, new_up):
                    if SHOW_SOLUTIONS:
                        for _ in range(rows_left-1):
                            current_grid.append('.' * n)
                        show()
                        for _ in range(rows_left-1):
                            current_grid.pop()

                    return 1

                return count_grid_loops(merged_components, new_up, rows_left - 1)
            finally:
                if SHOW_SOLUTIONS:
                    current_grid.pop()

        current_row[x] = False
        ans = rec(x+1)
        current_row[x] = True
        ans += rec(x+1)

        return ans

    return rec(0)


XSIZE = int(sys.argv[1])
YSIZE = int(sys.argv[2])

print(f"Counting loops in grid of size {XSIZE}x{YSIZE}")

num_solutions = count_grid_loops([None] * XSIZE, [False] * XSIZE, YSIZE)

print("Number of solutions:", num_solutions)
