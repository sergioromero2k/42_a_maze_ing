# Quick Reference – Build and Install Your Own `.whl` in Python

## 1. Install the build tool (once)

```bash
pip install build
```

Installs the `build` module, which generates the distributable package.

---

## 2. Create the `.whl` file

Navigate to the project root (where `pyproject.toml` is located):

```bash
python3 -m build
```

A `dist/` folder will be created containing something like:

```
dist/mazegen-1.0.0-py3-none-any.whl
```

That is your installable package.

---

## 3. Install your own `.whl`

From the project root:

```bash
pip install dist/mazegen-1.0.0-py3-none-any.whl --force-reinstall
```

`--force-reinstall` forces reinstallation even if the package is already installed.

---

## 4. Run it from anywhere

If you defined an entry point in `pyproject.toml` like:

```toml
[project.scripts]
a-maze-ing = "mazegen.cli:main"
```

You can then run:

```bash
a-maze-ing
```

From any directory (as long as the virtual environment is active).

---

## Steps to set it up on Campus

1. Open the terminal in the folder where the file is located.
2. Install it with this command:

```bash
pip install mlx-2.2-py3-ubuntu-any.whl
```

3. Quick test to confirm the system recognizes it:

```bash
python3 -c "from mlx import Mlx; m = Mlx(); print('MLX ready to rock!')"
```

---

## Useful reminders

- Activate your virtual environment before installing.
- If you change the version in `pyproject.toml`, a new `.whl` will be generated.
- Make sure you use the same Python to install and to run.
