#!/usr/bin/env python3
import random
from typing import Tuple, Optional, List


class MazeGenerator:
    """
    Class responsible for generating a maze with a centered '42' pattern.
    """

    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int],
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        output_file: str,
        perfect: bool,
    ) -> None:
        """
        Initializes a maze generator with the given configuration.

        Args:
            width: Number of columns.
            height: Number of rows.
            seed: Optional seed for deterministic generation.
            entry: Start coordinates as (row, col).
            exit: End coordinates as (row, col).
            output_file: Path to save the hex string.
            perfect: Whether to ensure exactly one path (DFS).
        """
        self.width: int = width
        self.height: int = height
        self.seed: Optional[int] = seed
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit
        self.output_file: str = output_file
        self.perfect: bool = perfect
        self.mold_positions: List[Tuple[int, int]] = []

        # We configure randomness with the seed.
        # Freeze randomness (deterministic generation)
        random.seed(self.seed)
        self.setup_matrices()
        self.draw_42()

    def setup_matrices(self) -> None:
        """
        Initializes the grid with all walls closed (15) and visit tracker.
        """
        self.grid: list[list[int]] = [
            [15 for _ in range(self.width)] for _ in range(self.height)
        ]
        # Create the control matrix (everything unvisited = False)
        self.visited: list[list[bool]] = [
            [False for _ in range(self.width)] for _ in range(self.height)
        ]

    def draw_42(self) -> None:
        """Defines and centers the '42' stencil within the maze grid."""
        # Simple drawing of a 4 and a 2
        mold_42 = {
            # The number 4
            (0, 0),
            (1, 0),
            (2, 0),  # Left stick
            (2, 1),  # Crossbar
            (0, 2),
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),  # Right post
            # The number 2 (starting in column 4 to leave space)
            (0, 4),
            (0, 5),
            (0, 6),  # Roof
            (1, 6),  # Right slope
            (2, 6),
            (2, 5),
            (2, 4),  # Middle
            (3, 4),  # Left slope
            (4, 4),
            (4, 5),
            (4, 6),  # Floor
        }

        """
        Center the stencil: subtract half of the stencil size so
        its top-left corner lands correctly
        (the stencil spans  x=0-6 => width 7 -> 7//2 = 3, and
                            y=0-4 => height 5 -> 5//2 = 2)
        """
        offset_row = self.height // 2 - 2
        offset_col = self.width // 2 - 3

        self.mold_positions = []
        # "Paint" the 42 into the visited matrix
        for dy, dx in mold_42:
            r_real = offset_row + dy
            c_real = offset_col + dx
            # Only if the point falls inside the maze (safety check)
            if 0 <= r_real < self.height and 0 <= c_real < self.width:
                self.mold_positions.append((r_real, c_real))

    def generate(self) -> None:
        """Generate the maze using DFS and handle perfection logic."""
        # Mark '42' cells as visited to block them
        for r, c in self.mold_positions:
            self.visited[r][c] = True

        stack: List[Tuple[int, int]] = []
        r_start, c_start = self.entry
        stack.append((r_start, c_start))
        self.visited[r_start][c_start] = True

        # Standard DFS for Perfect Maze
        while stack:
            cr, cc = stack[-1]
            neighbors = self._get_unvisited_neighbors(cr, cc)

            if neighbors:
                nr, nc, d, opp = random.choice(neighbors)
                self.grid[cr][cc] -= d
                self.grid[nr][nc] -= opp
                self.visited[nr][nc] = True
                stack.append((nr, nc))
            else:
                stack.pop()

        # If NOT perfect, break some extra walls to create loops
        if not self.perfect:
            self._break_extra_walls()

        # --- CORRECTED: Open entrance and exit based on (row, col) ---
        for r, c in [self.entry, self.exit]:
            if r == 0:                       # Top edge
                self.grid[r][c] &= ~1
            elif r == self.height - 1:       # Bottom edge
                self.grid[r][c] &= ~4
            if c == 0:                       # Left edge
                self.grid[r][c] &= ~8
            elif c == self.width - 1:        # Right edge
                self.grid[r][c] &= ~2

    def _break_extra_walls(self) -> None:
        """Breaks random walls to create a non-perfect maze (braid maze)."""
        extra_walls = (self.width * self.height) // 10
        for _ in range(extra_walls):
            r = random.randint(1, self.height - 2)
            c = random.randint(1, self.width - 2)
            # Break a random wall (North or East) if it exists
            wall = random.choice([1, 2])
            if self.grid[r][c] & wall:
                self.grid[r][c] &= ~wall
                if wall == 1:
                    self.grid[r - 1][c] &= ~4
                else:
                    self.grid[r][c + 1] &= ~8

    def _get_unvisited_neighbors(
        self, r: int, c: int
    ) -> List[Tuple[int, int, int, int]]:
        """
        Finds unvisited neighbors and calculates wall bitmasks.

        Returns:
            List of (next_row, next_col, direction_bit, opposite_bit)
        """
        neighbors = []
        # Directions: (dr, dc, bit, opp_bit)
        directions = [
            (-1, 0, 1, 4),  # North (1)     -> Opposite South (4)
            (0, 1, 2, 8),  # East (2)      -> Opposite West (8)
            (1, 0, 4, 1),  # South (4)     -> Opposite North (1)
            (0, -1, 8, 2),  # West (8)      -> Opposite East (2)
        ]

        for dr, dc, bit, opp_bit in directions:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < self.height
                and 0 <= nc < self.width
                and not self.visited[nr][nc]
            ):
                neighbors.append((nr, nc, bit, opp_bit))
        return neighbors

    def save_to_file(self, solution: str) -> None:
        """
        Save the maze following the strict format:
        - Hex grid (one row per line)
        - Empty line
        - Entry coordinates (X,Y according to subject)
        - Exit coordinates (X,Y according to subject)
        - Solution path
        """
        hexa = "0123456789ABCDEF"
        with open(self.output_file, "w") as f:
            for row in self.grid:
                f.write("".join(hexa[cell] for cell in row) + "\n")
            f.write("\n")
            # IMPORTANT: For the output file, we swap back to (X, Y)
            f.write(f"{self.entry[1]},{self.entry[0]}\n")
            f.write(f"{self.exit[1]},{self.exit[0]}\n")
            f.write(f"{solution}\n")
