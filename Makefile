# --- Project Name ---
NAME         = a_maze_ing

# --- Executables and Paths ---
PYTHON       = python3
ENTRY_POINT  = a_maze_ing.py
CONFIG       = config.txt
OUTPUT       = output_maze.txt

# --- Colors for Terminal ---
GREEN        = \033[0;32m
RED          = \033[0;31m
YELLOW       = \033[0;33m
RESET        = \033[0m

# --- Main Rules ---

all: run

# Create a virtual environment and install dependencies
venv:
	@echo "$(YELLOW)Creating virtual environment...$(RESET)"
	$(PYTHON) -m venv venv
	@echo "$(GREEN)Installing dependencies in venv...$(RESET)"
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install flake8 mypy build
	@echo "$(GREEN)Environment ready. Use 'source venv/bin/activate' to start.$(RESET)"


# Install required tools in the current environment
install:
	@echo "$(YELLOW)Installing linting and build tools...$(RESET)"
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install flake8 mypy build

# Execute the main program
run:
	@echo "$(GREEN)Running $(NAME)...$(RESET)"
	$(PYTHON) $(ENTRY_POINT) $(CONFIG)

# Build the .whl package for distribution (Chapter VI)
package:
	@echo "$(YELLOW)Building the wheel package...$(RESET)"
	$(PYTHON) -m build
	@echo "$(GREEN)Moving .whl to root directory...$(RESET)"
	@# This moves the generated .whl and removes build artifacts
	mv dist/*.whl .
	rm -rf build dist *.egg-info
	@echo "$(GREEN)Package generated successfully.$(RESET)"

# Clean temporary files and caches
clean:
	@echo "$(RED)Cleaning caches and temporary files...$(RESET)"
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -f $(OUTPUT)
	find . -type d -name "__pycache__" -exec rm -rf {} +

# New rule: Specifically to remove the virtual environment
clean_venv:
	@echo "$(RED)Removing virtual environment...$(RESET)"
	rm -rf venv

# Full clean: removes everything including the .whl package
fclean: clean
	@echo "$(RED)Removing .whl packages...$(RESET)"
	rm -f *.whl

# Run the debugger
debug:
	@echo "$(YELLOW)Running in debug mode...$(RESET)"
	$(PYTHON) -m pdb $(ENTRY_POINT) $(CONFIG)

# Rebuild and run
re: clean run

# --- Linting (Code Quality) ---

# --- Linting (Code Quality) ---

lint:
	@echo "$(YELLOW)Running Flake8...$(RESET)"
	-$(PYTHON) -m flake8 . --exclude=venv,test_env,env,.venv,mlx_source,mlx
	@echo "$(YELLOW)Running Mypy...$(RESET)"
	-$(PYTHON) -m mypy . --exclude "mlx_source" --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --no-error-summary || true

# --- Help ---

help:
	@echo "$(GREEN)A-Maze-ing Makefile Options:$(RESET)"
	@echo "  make venv         - Create a venv and install all tools"
	@echo "  make install      - Install flake8, mypy and build"
	@echo "  make run          - Execute the program with $(CONFIG)"
	@echo "  make package      - Generate the .whl package for submission"
	@echo "  make lint         - Run static code analysis (PEP8 & Types)"
	@echo "  make clean        - Remove temporary files"
	@echo "  make fclean       - Remove all generated files including .whl"
	@echo "  make re           - Clean and restart"

.PHONY: all venv install run package clean fclean debug re lint help
