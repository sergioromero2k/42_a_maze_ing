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
        grid:  The maze matrix [row][col].
        start: Entry coordinates as (row, col).
        end:   Exit coordinates as (row, col).
    Returns:
        str:   Direction string (e.g. 'EESNW').
    """
    # Safety check for empty grid
    height = len(grid)
    if height == 0:
        return ""
    width = len(grid[0])

    # Unpack entry and exit coordinates (row, column)
    start_r, start_c = start
    end_r, end_c = end

    # Queue stores: (current_row, current_col, path_string)
    # Positions I have yet to explore
    queue: deque[Tuple[int, int, str]] = deque([(start_r, start_c, "")])
    visited: set[Tuple[int, int]] = {(start_r, start_c)}

    # Directions mapping: (row_delta, col_delta, wall_bit, move_char)
    # North (1): r-1 | East (2): c+1 | South (4): r+1 | West (8): c-1
    # IMPORTANT: The bit must match the wall we want to CROSS.
    directions = [
        (-1, 0, 1, "N"),  # North: bit 1
        (0, 1, 2, "E"),  # East:  bit 2
        (1, 0, 4, "S"),  # South: bit 4
        (0, -1, 8, "W"),  # West:  bit 8
    ]

    while queue:
        row, col, path = queue.popleft()

        # Check if target reached
        if (row, col) == (end_r, end_c):
            return path

        for dr, dc, bit, char in directions:
            nr, nc = row + dr, col + dc

            # Check map boundaries
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the wall in THAT direction is open (bit is 0)
                if not (grid[row][col] & bit) and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, path + char))

    # If no path is found
    # It means the maze generation or the coordinates are wrong
    print("[ERROR] No valid path found. Check boundary walls.")
    return ""
