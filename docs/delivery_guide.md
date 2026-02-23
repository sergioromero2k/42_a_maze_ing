# Delivery Guide: A-Maze-ing

Follow these steps in order to ensure you meet all the requirements from Chapter VI (Reusability) and Chapter IX (Delivery).

---

## 1. Full Cleanup (Pre-delivery)

Before generating anything, remove all binaries and caches that are forbidden in the repository.

```bash
# Run your clean rule
make clean

# Remove any previous build folders if they exist
rm -rf dist/ build/ *.egg-info

# Remove the MLX binary (must be compiled/installed on site)
rm -f mlx_source/libmlx.so
```

---

## 2. Reusable Package Generation (`.whl`)

The subject requires the `mazegen` module to be installable.

**Step 1** — Install the build tool:

```bash
pip install build
```

**Step 2** — Build the package:

```bash
python3 -m build
```

**Step 3** — Move the file to the root (MANDATORY REQUIREMENT): The evaluator must find the `.whl` at the root, not inside a `dist/` folder.

```bash
mv dist/mazegen-*.whl .
```

---

## 3. Final Structure Verification

Your GitHub/GitLab repository must look exactly like this:

```
42_a_maze_ing/
├── a_maze_ing.py                        # Main script
├── config.txt                           # Default configuration
├── Makefile                             # With install, run, lint, clean, debug rules
├── pyproject.toml                       # Build metadata
├── README.md                            # Professional documentation
├── mazegen-1.0.0-py3-none-any.whl       # <-- HERE AT THE ROOT
├── mazegen/                             # Logic folder
├── display/                             # UI folder
├── mlx_source/                          # Wrapper folder (without the .so)
└── .gitignore                           # Ignoring __pycache__ and .so
```

---

## 4. The Evaluation Dry Run

Do this to be 100% sure you will not fail in front of the evaluator:

```bash
# 1. Create a clean virtual environment
python3 -m venv test_env
source test_env/bin/activate

# 2. Install your own .whl file
pip install mazegen-1.0.0-py3-none-any.whl

# 3. Test linting (must return 0 errors)
make lint

# 4. Test execution
make run

# 5. Exit the environment and delete the test
deactivate
rm -rf test_env
```

---

## 5. Defense Checklist

Be ready to answer these:

**Why the `.whl`?**
> "To comply with the reusability requirement. It allows any other developer to install my generation logic as a standard Python library."

**How do you draw the 42?**
> "I inject it into the matrix before generating the maze and mark those cells as visited so the algorithm flows around them without breaking the path."

**What happens if the `config.txt` is set to an impossible size?**
> "The parser validates the coordinates against the width and height. If they are incoherent, it raises a controlled error instead of crashing."