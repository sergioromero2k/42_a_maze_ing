#!/usr/bin/env python3
from typing import Tuple, List
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

    # Calculate dimensions automatically
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    # Unpack entry and exit coordinates (row, column)
    start_r, start_c = start
    end_r, end_c = end

    # Queue stores: (current_row, current_col, path_string)
    queue: deque[Tuple[int, int, str]] = deque([(start_r, start_c, "")])
    visited: set[Tuple[int, int]] = {(start_r, start_c)}

    # Directions mapping: (row_delta, col_delta, wall_bit, move_char)
    # North (1): r-1 | East (2): c+1 | South (4): r+1 | West (8): c-1
    directions = [
        (-1, 0, 1, "N"),    # North
        (0, 1, 2, "E"),     # East
        (1, 0, 4, "S"),     # South
        (0, -1, 8, "W")     # West
    ]

    while queue:
        row, col, path = queue.popleft()

        # Check if target reached
        if (row, col) == (end_r, end_c):
            return path

        for dr, dc, bit, char in directions:
            # New row, new column
            nr, nc = row + dr, col + dc
            # Check if target reached
            if 0 <= nr < height and 0 <= nc < width:
                # Check bitwise if the wall is open in the given direction
                # and ensure the cell hasn't been visited yet
                if not (grid[row][col] & bit) and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, path + char))

    # No solution found
    return ""
