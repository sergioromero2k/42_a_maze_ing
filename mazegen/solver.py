#!/usr/bin/env python3
from typing import Tuple, Optional, List
from collections import deque


def solve(
        grid: List[List[int]],
        start: Tuple[int, int], end: Tuple[int, int]) -> str:
    """
    Find the shortest path using BFS.
    Receive the matrix generated.

    Args:
        start:  Input coordinates (x, y).
        end:    Output coordinates (x, y).
    Returns:
        str: Address string (e.g. 'EESNW').
    """

    # We calculate dimensions automatically
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    # Initialize Queue: (row, col, path_string)
    # We use (row, col) to be consistent with your generator's entry/exit
    queue: deque[Tuple[int, int, str]] = deque([(start[0], start[1], "")])
    visited: set[Tuple[int, int]] = {start}

    # Directions : (d_row, d_col, bit_mask, char)
    # North: row-1 (1), East: col+1 (2), South: row+1 (4), West: col-1 (8)
    directions = [
        (-1, 0, 1, "N"),    # North
        (0, 1, 2, "E"),     # East
        (1, 0, 4, "S"),     # South
        (0, -1, 8, "W")     # West
    ]

    while queue:
        r, c, path = queue.popleft()

        # If we reach the exit (matching row and column).
        if (r, c) == end:
            return path

        for dr, dc, bit, char in directions:
            # New row, new column
            nr, nc = r + dr, c + dc  
            # nr (row) is compared to height | nc (column) is compared to width
            if 0 <= nr < height and 0 <= nc < width:
                # VERY IMPORTANT: grid[row][column] -> grid[r][c]
                if not (grid[r][c] & bit) and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, path + char))

    # No solution found
    return ""
