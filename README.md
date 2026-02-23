*Created as part of the 42 curriculum by **serromer** and **dcasado-**.*

# 42_A_MAZE_ING — The Perfect Maze Generator
---

## What is this?

**A-Maze-ing** is a Python suite for generating and solving **perfect mazes** — mazes where any two points are connected by exactly one path, with no loops and no unreachable areas (a spanning tree, in graph theory terms).

Beyond the algorithm, the project embeds a mandatory **"42" visual pattern** into every maze, ships a live graphical visualizer, and exports results in a compact hexadecimal wall-encoding format.

---

## Features

- **Perfect maze guarantee** — single-path connectivity via spanning tree logic.
- **"42" easter egg** — the 42 logo is carved into the maze walls before generation begins.
- **Deterministic seeds** — reproduce any maze exactly with a given seed.
- **Interactive visualizer** — MiniLibX-powered window with real-time controls.
- **Hex export** — 4-bit wall encoding written to a configurable output file.

---

## Prerequisites

- Python 3.10+
- `pip`
- `X11` libraries (required for MiniLibX graphical output)

---

## Installation

From the project root, install in editable mode:

```bash
make install
pip install -e .
```

---

## Usage

### Quick Start (Simplifying life with Makefile)

To make your life easier, we've automated the entire setup and execution process. You don't need to worry about creating environments or installing tools manually.

| Command | Action |
|---------|--------|
| `make all` | **Recommended:** Execute all |
| `make venv` | **Recommended:** Creates a virtual environment and installs all dependencies. |
| `make run` | Runs the maze generator with the default `config.txt`. |
| `make package` | Generates the mandatory `.whl` file for submission. |
| `make lint` | Runs `flake8` and `mypy` to ensure code quality. |
| `make clean_venv` | Removes the virtual environment. |
| `make fclean` | Full reset: Deletes caches, `.whl` packages, and the `venv`. |

> **Pro Tip:** If it's your first time running the project, just type `make venv && source venv/bin/activate` followed by `make run`.

Or point to a custom config:

```bash
python3 a_maze_ing.py config.txt
```

### Visualizer Controls

| Key | Action |
|-----|--------|
| `R` | Regenerate maze with a new random seed |
| `S` | Toggle shortest-path solution (BFS) |
| `C` | Cycle color palettes |
| `ESC` / Close window | Exit gracefully |

---

## Configuration File

Key-value format. Lines starting with `#` are comments and are ignored.

| Key | Description |
|-----|-------------|
| `WIDTH` / `HEIGHT` | Must be **odd integers** (e.g. `31`) to maintain cell-wall symmetry |
| `ENTRY` / `EXIT` | Zero-indexed coordinates as `x,y` |
| `SEED` | Integer for reproducible generation |
| `OUTPUT_FILE` | Destination for the hex-encoded maze |
| `PERFECT` | `True` for DFS generation |

### Example

```ini
# Project Configuration
WIDTH=31
HEIGHT=31
ENTRY=1,1
EXIT=29,29
SEED=4242
OUTPUT_FILE=output_maze.txt
PERFECT=True
```

---

## How It Works

### Wall Encoding — 4-bit Bitwise Logic

Each cell is represented by 4 bits, one per direction:

| Direction | Bit | Value |
|-----------|-----|-------|
| North | 0 | 1 |
| East  | 1 | 2 |
| South | 2 | 4 |
| West  | 3 | 8 |

A cell with value `0x9` (`1001` in binary) has open walls to the **North** and **West**.

### Generation — Recursive Backtracker (DFS)

DFS was chosen for its aesthetic output: high tortuosity and long, winding dead-ends — far more visually compelling than Prim's algorithm, which tends to produce many short branches.

The **"42" pattern** is carved out *before* generation starts. Those cells are pre-marked as visited, so the DFS flows around them and preserves the shape.

### Solving — Breadth-First Search (BFS)

In a perfect maze there are no cycles, so the first time BFS reaches the exit, the path found is guaranteed to be the **only** (and therefore shortest) path.

---

## Project Structure

The project is split into two independent packages:

- **`mazegen`** — pure generation logic, no UI dependencies. Can be used in CLI tools or notebooks.
- **`display`** — visualization layer. Can be swapped for Pygame or Matplotlib without touching generation logic.

```
42_a_maze_ing
├── a_maze_ing.py          # Main entry point (the "brain")
├── config.txt             # Sample configuration file
├── Makefile               # Automation tool (all, run, clean, lint, re)
├── pyproject.toml         # Modern Python project metadata & config
├── README.md              # Project documentation
├── display/               # Graphical module
│   ├── __init__.py
│   └── graphical.py       # MLX visualization logic
├── docs/                  # Project guides and documentation
│   ├── ES/                # Translation into Spanish
│   ├── differentes_cases_config.txt
│   ├── es.subject_a_maze_py.pdf
│   ├── execution_whl.md
│   ├── mlx_setup.md
│   ├── output_validator.py
│   └── project_division.md
├── libs/                  # Offline dependencies (WHL files)
│   ├── mlx-2.2-py3-fedora-any.whl
│   └── mlx-2.2-py3-ubuntu-any.whl
├── mazegen/               # Core logic package
│   ├── __init__.py
│   ├── generator.py       # Maze generation (DFS + 42 pattern)
│   ├── py.typed           # Support for Mypy type checking
│   ├── solver.py          # Solving algorithm (BFS)
│   └── utils.py           # Config parser and helpers
├── mlx_source/            # MLX Python bindings source
│   ├── __init__.py
│   ├── mlx.py
│   └── docs/              # Man pages and headers
│       ├── mlx.3
│       ├── mlx.h
│       └── ... (other .3 files)
├── tests/                 # Unit tests for logic
│   ├── __init__.py_
└── .gitignore             # File to prevent tracking caches/garbage
```

---

## Team

| Member | Role |
|--------|------|
| **serromer** | Lead Architect — MazeGenerator engine, DFS logic, Python packaging, Makefile |
| **dcasado-** | Lead Developer — BFS Solver, config parser, MiniLibX graphical interface |

### Planning vs. Reality

The "42" pattern injection took longer than expected, pushing the generator from Day 2 to Day 3. We recovered the time by defining a shared interface (Abstract Base Classes) early, which allowed the UI and logic to be integrated in under 2 hours.

Using `mypy --strict` from day one prevented dozens of `NoneType` errors during integration — highly recommended.

---

## AI Disclosure

AI tools were used strictly for non-algorithmic tasks:

- Generating `Makefile` and `pyproject.toml` templates
- Boilerplate for signal handling (`SIGINT`)
- Drafting and translating documentation

All core algorithms (DFS / BFS) were designed and implemented by the team to ensure academic integrity.

---

## Resources

- [Maze Generation Algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm) — theoretical foundation
- [Python Packaging User Guide](https://packaging.python.org/) — `pyproject.toml` standards

