#!/usr/bin/env python3
import sys
import signal
from typing import Any
from mazegen.utils import parse_config
from mazegen.generator import MazeGenerator
from mazegen.solver import solve
from display.graphical import MazeVisualizer


def handle_sigint(sig: int, frame: Any) -> None:
    """Handle CTRL+C to exit gracefully without stack trace."""
    print(
        "\n\033[93m[!] Execution interrupted by user (CTRL+C). " "Exiting...\033[0m")
    sys.exit(0)


def main() -> None:
    """Main entry point for the maze generator and solver."""
    # Register signal for clean exit
    signal.signal(signal.SIGINT, handle_sigint)

    # 1. Parse configuration
    try:
        config = parse_config("config.txt")
    except FileNotFoundError:
        print("\033[91m[ERROR] config.txt not found!\033[0m")
        sys.exit(1)

    # 2. Instantiate and Generate
    # Using seed=42 for deterministic results as requested
    maze = MazeGenerator(**config, seed=42)
    maze.generate()
    maze.save_to_file()

    # 3. Solve the maze
    solution = solve(maze.grid, maze.entry, maze.exit)

    # 4. Professional Terminal Output
    print("\033[92m\n--- MAZE DATA ---\033[0m")
    print(f"Dimensions : {maze.width}x{maze.height}")
    print(f"Entry      : {maze.entry}")
    print(f"Exit       : {maze.exit}")

    print("\033[94m\n--- SOLUTION ---\033[0m")
    if solution:
        print(f"Path FOUND : \033[97m{solution}\033[0m")
        print(f"Steps      : {len(solution)}")
    else:
        print("\033[91mNo solution found. Check entry/exit borders!\033[0m")

    # 5. Visualizer Instructions
    print("\033[92m\n--- GRAPHICAL INTERFACE ---\033[0m")
    print("Opening window...")
    print("  - Press \033[95mESC\033[0m to close the window.")
    print("  - Press \033[95mCTRL+C\033[0m in terminal to force quit.")

    # 6. Launch Visualizer (Passing grid, path and entry for correct trace)
    visualizer = MazeVisualizer(maze.grid, solution, maze.entry)
    visualizer.run()


if __name__ == "__main__":
    main()
