import sys
from functools import cache
from collections import defaultdict
from queue import Queue
from typing import Iterable, Tuple, List, Optional

SHOW_SOLUTIONS = False
STORE_SOLUTIONS = False

# Force cells in a grid. Use '#', '.' or '?'
# Might make solution slower as less caching can be used
FORCED = None

# FORCED = [
#     "########",
#     "#......#",
#     "#.####.#",
#     "#.#..#.#",
#     "#.#.##.#",
#     "#.#.#..#",
#     "###.####"
# ]

@cache
def scanline_merge_components(
    previous_row: Tuple[Optional[int], ...], current_row_str: str
) -> Tuple[Tuple[Optional[int], ...], int]:
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

    current_row = [c == '#' for c in current_row_str]

    assert len(previous_row) == len(current_row)

    comp_column_map = defaultdict(list)
    for i, comp in enumerate(previous_row):
        if comp is not None:
            comp_column_map[comp].append(i)

    n = len(previous_row)
    seen = [False] * n
    output: List[Optional[int]] = [None] * n
    current_comp = 0

    for i in range(n):
         if current_row[i] and not seen[i]:
            q = Queue()
            q.put(i)
            seen[i] = True
            while not q.empty():
                x = q.get()
                output[x] = current_comp
                if x+1 < n and current_row[x+1] and not seen[x+1]:
                    q.put(x+1)
                    seen[x+1] = True
                if x-1 >= 0 and current_row[x-1] and not seen[x-1]:
                    q.put(x-1)
                    seen[x-1] = True
                if previous_row[x] is not None:
                    for j in comp_column_map[previous_row[x]]:
                        if current_row[j] and not seen[j]:
                            q.put(j)
                            seen[j] = True
                    comp_column_map[previous_row[x]].clear()

            current_comp += 1

    return (tuple(output), len([k for k, v in comp_column_map.items() if v]))

def valid_pattern_bitmask(row1: int, row2: int):
    # Certain patterns in any local 3x2 part of the grid are invalid
    # Examples of invalid local patterns:
    # ...   #..   .##   .#.
    # .#.   .##   .##   ###

    assert row1 < 8 and row2 < 8

    if row1 in (0, 7) and row2 == 2:
        return False
    if row1 == 2 and row2 in (0, 7):
        return False
    if (row1 & 3) == 3 and (row2 & 3) == 3:
        return False
    if (row1 & 6) == 6 and (row2 & 6) == 6:
        return False
    if (row1 & 3) == 2 and (row2 & 3) == 1:
        return False
    if (row1 & 3) == 1 and (row2 & 3) == 2:
        return False
    if (row1 & 6) == 2 and (row2 & 6) == 4:
        return False
    if (row1 & 6) == 4 and (row2 & 6) == 2:
        return False
    return True

precalc_valid_patterns = []
for i in range(8):
    for j in range(8):
        precalc_valid_patterns.append(valid_pattern_bitmask(i, j))

def valid_final_row(components: Tuple[Optional[int], ...], up: Tuple[bool, ...]):
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

def validate_up(row1: Tuple[Optional[int], ...], row2: str, up: Tuple[bool, ...], i: int):
    # Both edges of horizontal lines in row1 must either go up (up[x] set) or down (row2[x] set)

    if row1[i] is None:
        return True

    n = len(row1)
    if (i == 0 or row1[i-1] is None) and i+1 < n and row1[i+1] is not None:
        if up[i] == (row2[i] == '#'):
            return False

    if (i == n-1 or row1[i+1] is None) and i-1 >= 0 and row1[i-1] is not None:
        if up[i] == (row2[i] == '#'):
            return False

    return True

current_grid = []
all_solutions = []

def rotate(grid: List[str]):
    res = []
    xsize, ysize = len(grid[0]), len(grid)
    for x in range(xsize):
        s = ""
        for y in range(ysize):
            s += grid[ysize -1 - y][x]
        res.append(s)
    return res

def show():
    for row in current_grid:
        print(row)
    print()

def store():
    global all_solutions
    all_solutions.append(current_grid[:])


@cache
def generate_row_patterns(components: Tuple[Optional[int], ...], up: Tuple[bool, ...], row_num: int) -> List[str]:
    n = len(components)

    patterns = []

    def rec(current_row: str, row1_last3: int, row2_last3: int):
        x = len(current_row)
        if not precalc_valid_patterns[row1_last3 * 8 + row2_last3]:
            return
        if x > 1 and not validate_up(components, current_row, up, x-2):
            return

        if x == n:
            if not precalc_valid_patterns[((row1_last3 * 2) & 7) * 8 + ((row2_last3 * 2) & 7)]:
                return
            if not validate_up(components, current_row, up, x-1):
                return

            patterns.append(current_row)
        else:
            mask1 = ((row1_last3 * 2) & 7) + (components[x] is not None)
            mask2 = (row2_last3 * 2) & 7

            c = FORCED[row_num][x] if FORCED and row_num < len(FORCED) and x < len(FORCED[row_num]) else '?'

            if c != '#':
                rec(current_row + ".", mask1, mask2)
            if c != '.':
                rec(current_row + "#", mask1, mask2+1)

    rec("", 0, 0)
    return patterns


@cache
def count_grid_loops_rec(components: Tuple[Optional[int], ...], up: Tuple[bool, ...], rows_left: int, row_num: int):
    if rows_left == 0:
        return 0

    global current_grid

    n = len(components)

    started = any(x is not None for x in components)

    num_solutions = 0

    for current_row in generate_row_patterns(components, up, row_num):
        if SHOW_SOLUTIONS or STORE_SOLUTIONS:
            current_grid.append(current_row)

        merged_components, num_lost_components = scanline_merge_components(components, current_row)
        try:
            if num_lost_components > 0:
                # Ensure we don't have multiple loops
                return 0

            new_up = tuple(merged_components[i] is not None and components[i] is not None for i in range(n))

            if started and valid_final_row(merged_components, new_up):
                if SHOW_SOLUTIONS or STORE_SOLUTIONS:
                    for _ in range(rows_left-1):
                        current_grid.append('.' * n)
                    if SHOW_SOLUTIONS:
                        show()
                    if STORE_SOLUTIONS:
                        store()
                    for _ in range(rows_left-1):
                        current_grid.pop()

                num_solutions += 1
            else:
                num_solutions += count_grid_loops_rec(merged_components, new_up, rows_left - 1, row_num + 1 if FORCED else row_num)
        finally:
            if SHOW_SOLUTIONS or STORE_SOLUTIONS:
                current_grid.pop()

    return num_solutions

def count_grid_loops(xsize, ysize):
    return count_grid_loops_rec(tuple([None] * xsize), tuple([False] * xsize), ysize, 0)

def symmetry_compare(N: int, M: int):
    global all_solutions
    count_grid_loops(M, N)

    print(f"Found {len(all_solutions)} solutions for {M}x{N} grid")

    rotated_solutions = set()
    for solution in all_solutions:
        rotated_solutions.add('\n'.join(rotate(solution)))
    all_solutions = []

    count_grid_loops(N, M)

    print(f"Found {len(all_solutions)} solutions for {N}x{M} grid")

    for solution in all_solutions:
        sol = '\n'.join(solution)
        if sol in rotated_solutions:
            rotated_solutions.remove(sol)
        else:
            print(f"Found in {N}x{M} but not in {M}x{N}")
            print(sol)
            print()

    for sol in rotated_solutions:
        print(f"Found in {M}x{N} but not in {N}x{M}")
        print(sol)

def main(xsize, ysize):
    print(f"Counting loops in grid of size {xsize}x{ysize}")
    num_solutions = count_grid_loops(xsize, ysize)
    print("Number of solutions:", num_solutions)
    try:
        print(f"count_grid_loops_rec {count_grid_loops_rec.cache_info()}")
        print(f"scanline_merge_components {scanline_merge_components.cache_info()}")
        print(f"generate_row_patterns {generate_row_patterns.cache_info()}")

    except:
        pass

    # 3x3           1
    # 4x4          13
    # 5x5         167
    # 6x5         571
    # 6x6        2685
    # 7x5        1656
    # 7x6       10314
    # 7x7       50391
    # 8x7      222805
    # 8x8     1188935
    # 8x9     6510243
    # 8x10   39576571
    # 9x10  303385827
    # 8x20  3350776906928379
    # 9x9    41749885  # cachesize: 11676, 0.19s user
    # 10x10  2645126227  # cachesize: 34476, 0.57s user
    # 11x11  341643017303  # cachesize: 100237, 1.93s user
    # 12x12  82472721488013  # cachesize: 287978, 6.53s user
    # 13x13  31312529515504513  # cachesize: 827233, 21.22s user
    # 14x14  17381378412860375479  # cachesize: 2365211, 74.20s user

    # Number of solutions for NxN grids for N=3..14:
    # 1, 13, 167, 2685, 50391, 1188935, 41749885, 2645126227, 341643017303, 82472721488013,
    #   31312529515504513, 17381378412860375479

# symmetry_compare(7, 8)

sys.setrecursionlimit(10000)
main(int(sys.argv[1]), int(sys.argv[2]))
