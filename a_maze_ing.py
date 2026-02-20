#!/usr/bin/env python3

from mazegen.utils import parse_config
from mazegen.generator import MazeGenerator

# Parser
config = parse_config("config.txt")

# Instantiate
maze = MazeGenerator(**config, seed=42)

# Generate
maze.generate()

# Print
for row in maze.grid:
    print(row)
