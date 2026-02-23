#!/usr/bin/env python3
import os
import sys
import signal
import random
from typing import Any

from mazegen.utils import parse_config
from mazegen.generator import MazeGenerator
from mazegen.solver import solve
from display.graphical import MazeVisualizer


def handle_sigint(sig: int, frame: Any) -> None:
    """Handle CTRL+C to exit gracefully."""
    print("\n\033[93m[!] Interrupted by user. Exiting...\033[0m")
    os._exit(0)


def main() -> None:
    """Main entry point for the A-Maze-ing generator."""
    # Register signal for clean exit
    signal.signal(signal.SIGINT, handle_sigint)

    # 1. Validate Arguments (Requirement IV.2)
    if len(sys.argv) != 2:
        print("\033[91mUsage: python3 a_maze_ing.py <config_file>\033[0m")
        sys.exit(1)

    config_file = sys.argv[1]

    # 2. Parse Configuration (Requirement IV.3)
    try:
        config = parse_config(config_file)
    except Exception as e:
        print(f"\033[91m[ERROR] Invalid configuration: {e}\033[0m")
        sys.exit(1)

    # 3. Handle SEED for Reproducibility (Requirement IV.4)
    # Use seed from config or generate a random one if not provided
    seed_val = config.get("seed")
    if seed_val is None:
        seed_val = random.randint(0, 999999)

    # Extract seed from config copy to pass remaining keys as kwargs
    config_params = config.copy()
    if "seed" in config_params:
        del config_params["seed"]

    # 4. Initialize and Generate Maze (Requirement IV.4)
    try:
        """
        FIXED: Explicitly passing arguments to avoid
                'output_file' missing error
        We use .get() for output_file to ensure it always has a value
        """
        maze = MazeGenerator(
            width=config_params["width"],
            height=config_params["height"],
            entry=config_params["entry"],
            exit=config_params["exit"],
            perfect=config_params["perfect"],
            output_file=config_params.get("output_file", "output_maze.txt"),
            seed=seed_val,
        )

        # Check if '42' pattern fits (Requirement IV.4 Special Case)
        if maze.width < 7 or maze.height < 5:
            print(
                "\033[93m[WARNING] "
                "Maze size too small for '42' pattern.\033[0m")

        maze.generate()
    except Exception as e:
        print(f"\033[91m[ERROR] Generation failed: {e}\033[0m")
        sys.exit(1)

    # 5. Solve and Save Output File (Requirement IV.5)
    solution = solve(maze.grid, maze.entry, maze.exit)
    if not solution:
        print(
            "\033[91m[ERROR] "
            "No valid path found. Check boundary walls.\033[0m")

    # Save using the hex format specified in IV.5
    maze.save_to_file(solution)

    # 6. Terminal Summary
    print("\033[92m--- MAZE GENERATED SUCCESSFULLY ---\033[0m")
    print(f"Output File  : {maze.output_file}")
    print(f"Seed Used    : {seed_val}")
    print(f"Dimensions   : {maze.width}x{maze.height}")
    print(f"Entry/Exit   : {maze.entry} -> {maze.exit}")

    # 7. Launch Interactive Visualizer (Chapter V)
    # Pass the full maze object to handle interactive regeneration
    print("\033[94mLaunching Graphical Interface...\033[0m")
    visualizer = MazeVisualizer(maze, solution)
    visualizer.run()


if __name__ == "__main__":
    main()
