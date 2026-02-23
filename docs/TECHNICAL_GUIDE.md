# Technical Project Guide: A-Maze-ing

A full breakdown of every file, class, and function in the project — what it does and why it exists.

---

## `a_maze_ing.py` — Entry Point

| Function | Description |
|----------|-------------|
| `handle_sigint()` | Catches the `SIGINT` signal (Ctrl+C) and closes the program cleanly, without printing a stack trace to the console. |
| `main()` | Orchestrates the full flow: validates arguments, calls the parser, manages the seed, instantiates the generator, runs the solver, and launches the interface. |

---

## `mazegen/` — Core Logic & Algorithms

### `generator.py` — Class `MazeGenerator`

| Function | Description |
|----------|-------------|
| `__init__` | Initializes dimensions, seed, entry/exit points, and the "perfect" flag. |
| `setup_matrices()` | Creates the initial grid filled with walls (closed cells) before any path is carved. |
| `draw_42()` | Modifies specific cells in the matrix to draw the number 42. By marking those cells as visited before the algorithm runs, the generator treats them as fixed obstacles, preserving the pattern. |
| `generate()` | Implements the DFS (Recursive Backtracker). This is the core engine that carves the maze tunnels. |
| `_break_extra_walls()` | If the maze is not required to be perfect, this function breaks additional walls to introduce cycles and alternative paths. |
| `_get_unvisited_neighbors()` | Scans the 4 cardinal directions to find adjacent cells that have not been visited yet. |
| `save_to_file()` | Encodes the matrix into hexadecimal format (1, 2, 4, 8) and writes the output file containing the solution. |

### `solver.py`

| Function | Description |
|----------|-------------|
| `solve()` | Implements the BFS algorithm. Explores the maze level by level to find the shortest path. Returns the solution as a string of directions (e.g. `"SSENW"`). |

### `utils.py` — Configuration Processing

| Function | Description |
|----------|-------------|
| `get_raw_config()` | Reads the file line by line and extracts key=value pairs, ignoring comments. |
| `format_value()` | Converts raw strings to proper Python types (e.g. `"10"` → `10`, `"True"` → `True`). |
| `format_config()` | Applies formatting to the entire configuration dictionary. |
| `validate_logic()` | Checks that the data is coherent (e.g. that entry/exit coordinates are within the maze bounds). |
| `parse_config()` | The master function that coordinates the full read-and-validate pipeline. |

---

## `display/` — Graphical Interface

### `graphical.py` — Class `MazeVisualizer`

| Function | Description |
|----------|-------------|
| `__init__` | Sets up the MiniLibX window and scales the block size based on screen resolution. |
| `put_pixel()` | Low-level function to paint a single pixel into the image buffer. |
| `draw_tile()` | Draws a full cell (floor and walls) by reading and interpreting its hex bits. |
| `terminal_menu()` | Prints the keyboard controls to the console so the user knows how to interact. |
| `handle_keys()` | Handles keyboard events (Esc to exit, R to regenerate, S to toggle the solution). |
| `render()` | The loop function that redraws the window continuously to keep the image up to date. |
| `run()` | Launches `mlx_loop()`, handing control over to the graphical interface. |

---

## Key Defense Questions

**Why did you split `utils.py` into so many small functions?**

> "To follow the Single Responsibility Principle. Each function does exactly one thing — read, format, or validate — which makes bugs easier to isolate and the code reusable in other contexts."

**Why DFS for generation and BFS for solving?**

> "DFS produces mazes with high tortuosity and long dead-ends — visually complex and interesting. BFS is the right tool for solving because in a perfect maze (no cycles), the first time it reaches the exit, that path is guaranteed to be the only one, and therefore the shortest."

**Why pre-mark the "42" cells before generation?**

> "If we carved the pattern after generation, the DFS might have already filled those cells with tunnels, destroying the shape. By marking them as visited first, the algorithm treats them as walls and flows around them naturally."

---

## `mlx_source/` — The MiniLibX Bridge

This directory contains the code that allows Python to "talk" to the original graphics library written in C. It is critical for the project's graphical performance.

### `mlx.py` — MLX Python Wrapper

A wrapper that uses the `ctypes` library to connect Python with the `libmlx.so` binary. Its main functions:

| Function | Description |
|----------|-------------|
| `__init__` | Locates the `.so` file on the system and loads the C functions into the Python environment. |

**Window Management**

| Function | Description |
|----------|-------------|
| `mlx_new_window()` | Asks the OS to create the graphical window. |
| `mlx_clear_window()` / `mlx_destroy_window()` | Cleanup functions to prevent memory leaks when closing the program. |

**Image Management**

| Function | Description |
|----------|-------------|
| `mlx_new_image()` | Creates a pixel buffer in memory for faster drawing than writing directly to the window. |
| `mlx_get_data_addr()` | **Critical.** Returns the memory address of the image, allowing Python to manipulate pixels directly as a data array. |
| `mlx_put_image_to_window()` | Flushes the entire image buffer to the window in one call, preventing screen flickering. |

**Event Hooks**

| Function | Description |
|----------|-------------|
| `mlx_key_hook()` / `mlx_hook()` | Register your code's functions (like movement or closing with ESC) to fire when the user interacts with the keyboard or mouse. |
| `mlx_loop()` | Keeps the program alive and listening for events continuously. |

**Utilities**

| Function | Description |
|----------|-------------|
| `mlx_get_screen_size()` | Gets the monitor resolution to scale the maze accordingly. |
| `mlx_png_file_to_image()` | Allows loading external textures or icons if needed. |

---

## Evaluation Note — The "API Break"

**Why do some functions return tuples (e.g. `mlx_get_screen_size` returns `(val, w, h)`)?**

> "In C, functions return values through pointers passed as arguments. In this Python wrapper, we converted those pointers into return tuples to make the code more readable and idiomatic, following standard Python conventions."