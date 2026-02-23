# --- Project Name ---
NAME         = a_maze_ing

# --- Executables and Paths ---
PYTHON       = python3
ENTRY_POINT  = a_maze_ing.py
CONFIG       = config.txt
OUTPUT       = output_maze.txt

# --- Colors for the terminal ---
GREEN       = \033[0;32m
RED         = \033[0;31m
YELLOW      = \033[0;33m
RESET       = \033[0m

# --- Main Rules ---

# The 'all' rule is usually the default
all: run

# Installation of dependencies required for testing
install:
	@echo "$(YELLOW)Installing linting tools...$(RESET)"
	$(PYTHON) -m pip install flake8 mypy

# Program execution
run:
	@echo "$(GREEN)Running $(NAME)...$(RESET)"
	$(PYTHON) $(ENTRY_POINT) $(CONFIG)

# Cleaning Python temporary files and maze output
clean:
	@echo "$(RED)Cleaning caches and temporary files...$(RESET)"
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -f $(OUTPUT)
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Redo everything (clean and run)
re: clean run

# --- Linting (Python Norminette style) ---

# Standard linting with the flags
lint:
	@echo "$(YELLOW)Running Flake8...$(RESET)"
	-flake8 .
	@echo "$(YELLOW)Running Mypy...$(RESET)"
	-mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# Strict linting
strict:
	@echo "$(RED)Running Mypy STRICT...$(RESET)"
	-mypy . --strict

# --- Help ---
help:
	@echo "$(GREEN)Available options:$(RESET)"
	@echo "  make install      - Installs flake8 and mypy"
	@echo "  make run          - Runs the program with $(CONFIG)"
	@echo "  make lint         - Checks the code style"
	@echo "  make clean        - Deletes temporary files"
	@echo "  make re           - Cleans and reruns"

.PHONY: all run clean lint strict install re help
