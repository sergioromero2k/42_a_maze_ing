#!/usr/bin/env python3
import random
from typing import List, Dict, Tuple, Any, Optional


class MazeGenerator:
    def __init__(
            self, width: int, height: int, seed: int, entry: Tuple[int, int],
            exit: Tuple[int, int]
            ) -> None:
        # We save the values (with their type: int)
        self.width = width
        self.height = height
        self.seed = seed

        # We configure randomness with the seed.
        random.seed(self.seed)

        # This is where you will create the 15s matrix
        self.grid: list[list[int]] = []
        self.grid: list[list[int]] = [
            [15 for _ in range(width)] for _ in range(height)]
        self.visited = list[list[int]] = [
            [False for _ in range(width)] for _ in range(height)]


