#!/usr/bin/env python3
import random
from typing import Tuple, Optional, List


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int],
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        output_file: str,
        perfect: bool
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
        self.output_file = output_file
        self.perfect = perfect

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

        self.mold_positions = []
        # "Paint" the 42 into the visited matrix
        for dx, dy in mold_42:
            x_real = offset_x + dx
            y_real = offset_y + dy
            # Only if the point falls inside the maze (safety check)
            if 0 <= x_real < self.width and 0 <= y_real < self.height:
                self.grid[y_real][x_real] = 15
                self.mold_positions.append((x_real, y_real))

        # Define Entry [Top-Left] and Exit (Bottom-Right)
        self.entry = entry
        self.exit = exit

        # We mark the entry as visited so that the algorithm stats there
        #                  coordenate[0][0]
        self.visited[self.entry[0]][self.entry[1]] = True

    def generate(self) -> None:
        """Generate the maze using the Recursive Backtracker (DFS) algorithm.
        The algorithm ensures that the maze is perfect (expansion tree).
        """
        stack: List[Tuple[int, int]] = []
        start_cell: Tuple[int, int] = self.entry
        stack.append(start_cell)

        while stack:
            cx, cy = stack[-1]
            neighbors = self._get_unvisited_neighbors(cx, cy, self.visited)

            if neighbors:
                nx, ny, direction, opp_direction = random.choice(neighbors)
                # We remove the walls (bitwise) between
                # the current cell and the neighboring cell.
                self.grid[cy][cx] -= direction
                self.grid[ny][nx] -= opp_direction
                self.visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                # Backtracking step:
                # If the current cell has no unvisited neighbors,
                # We go back to the previous cell in the path
                # by popping the stack.
                stack.pop()

        for x, y in self.mold_positions:
            self.grid[y][x] = 0
        """
        Open the maze entrance and exit to the outside
        by removing the wall bit(s) that touch
        the grid border (N=1, E=2, S=4, W=8).

        For earch of the two cells (entry and exit), we check
        if lies on the North/South/West/East edge and clear the
        corresponding wall using bit by bit AND with
        the negated mask (&=~mask).
        """
        for pos in [self.entry, self.exit]:
            # Open entrance and exit to the outside.
            row, column = pos
            # Northern Border
            if row == 0:
                self.grid[row][column] &= ~1
                # Southern Border
            elif row == self.height - 1:
                self.grid[row][column] &= ~4
            # West Border
            if column == 0:
                self.grid[row][column] &= ~8
            # East Edge
            elif column == self.width - 1:
                self.grid[row][column] &= ~2

    def _get_unvisited_neighbors(
        self, x: int, y: int, visited: List[List[bool]]
    ) -> List[Tuple[int, int, int, int]]:
        """Searches for unvisited neighbors and
            returns their position and wall bits.

        Returns:
            List[Tuple[nx, ny, dir, opp_dir]]: Current direction
                                                and its opposite.
        """
        neighbors = []
        # Addresses: (dx, dy, current_bit, opposite_bit)
        directions = [
            (0, -1, 1, 4),  # North (1)     -> Opposite South (4)
            (1, 0, 2, 8),   # East (2)      -> Opposite West (8)
            (0, 1, 4, 1),   # South (4)     -> Opposite North (1)
            (-1, 0, 8, 2)   # West (8)      -> Opposite East (2)
        ]

        for dx, dy, bit, opp_bit in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.width
                    and 0 <= ny < self.height
                    and not visited[ny][nx]):
                neighbors.append((nx, ny, bit, opp_bit))
        return neighbors

    def save_to_file(self):
        # Hexadecimal reference for bitwise values (0-15)
        hexa = "0123456789abcdef"
        content = "".join(
            "".join(hexa[cell] for cell in row) for row in self.grid)
        with open(self.output_file, "w") as f:
            f.write(content)
