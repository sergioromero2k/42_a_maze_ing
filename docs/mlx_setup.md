## Compiling MLX from Source

### Steps
```bash
cd mlx_source
chmod +x pybuild.sh
./pybuild.sh
```

The script creates a virtual environment, compiles the C code and generates a `.whl` in `mlx_source/python/dist/`.
```bash
pip install python/dist/mlx-*.whl
```

### If dependencies are missing (Ubuntu)
```bash
sudo apt update
sudo apt install libvulkan-dev libxcb-keysyms1-dev libxcb1-dev zlib1g-dev
```
Then try `./pybuild.sh` again.

### Why did the original .whl fail?

It was compiled for a different Python version or architecture. Running `pybuild.sh` generates the package tailored specifically for your system.
