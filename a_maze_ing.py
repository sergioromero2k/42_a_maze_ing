#!/usr/bin/env python3

from mazegen.utils import parse_config
from mazegen.generator import MazeGenerator
from mazegen.solver import solve

# Parser
config = parse_config("config.txt")

# Instantiate
maze = MazeGenerator(**config, seed=42)

# Generate
maze.generate()
maze.save_to_file()

# Print
solution = solve(maze.grid, maze.entry, maze.exit)
print("\n--- RESULTS ---")
if solution:
    print(f"Path: {solution}")
else:
    print("No solution found. Check entry/exit borders!")
print(f"Solution length: {len(solution)} steps")

print("\n--- HEX GRID ---")
hexa = "0123456789abcdef"
for row in maze.grid:
    print(" ".join(hexa[cell] for cell in row))