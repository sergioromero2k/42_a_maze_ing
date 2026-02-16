#!/usr/bin/env python3
import random
from typing import Tuple, Optional


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int],
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        output_file: str,
        perfect_maze: bool
    ) -> None:
        """
        Initializes a maze generator with the given configuration.

        Args:
            "width (int):" Number of columns in the maze grid.
            "height (int):" Number of rows in the maze grid.
            "seed (Optional[int]):" Random seed used to make maze generation
                deterministic. If None, a random seed will be used.

            "entry (Tuple[int, int]):" Starting cell coordinates
                in the form (row, col).
            "exit (Tuple[int, int]):" Ending cell coordinates
                in the form (row, col).

            "output_file (str):" Path or filename where the generated maze
                will be saved (e.g., as an image or text representation
                depending on implementation).
            "perfect_maze (bool):" If True, generates a perfect maze
                (a maze with exactly one unique path between any two cells,
                i.e., no loops). If False, the generator may allow loops
                or multiple paths.
        """
        # We save the values (with their type: int)
        self.width = width
        self.height = height
        self.seed = seed
        self.entry = entry
        self.exit = exit

        # We configure randomness with the seed.
        # Freeze randomness (deterministic generation)
        random.seed(self.seed)
        self.setup_matrices()
        self.draw_42(entry, exit)

    def setup_matrices(self):
        # Create the wall grid (all walls closed = 15)
        self.grid: list[list[int]] = [
            [15 for _ in range(self.width)] for _ in range(self.height)]
        # Create the control matrix (everything unvisited = False)
        self.visited: list[list[bool]] = [
            [False for _ in range(self.width)] for _ in range(self.height)
        ]

    def draw_42(self, entry, exit):
        # Defines the "42" stencil (small relative coordinates)
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
        offset_x = self.width // 2 - 3
        offset_y = self.height // 2 - 2

        # "Paint" the 42 into the visited matrix
        for dx, dy in mold_42:
            x_real = offset_x + dx
            y_real = offset_y + dy
            # Only if the point falls inside the maze (safety check)
            if 0 <= x_real < self.width and 0 <= y_real < self.height:
                self.visited[y_real][x_real] = True

        # Define Entry [Top-Left] and Exit (Bottom-Right)
        self.entry = entry
        self.exit = exit

        # We mark the entry as visited so that the algorithm stats there
        #                  coordenate[0][0]
        self.visited[self.entry[0]][self.entry[1]] = True
