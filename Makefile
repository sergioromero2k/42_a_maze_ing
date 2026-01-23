# Variables
PYTHON = python3
SRC = a_maze_ing.py 

# Rule for installing dependencies
install: 
	pip install flake8 mypy

# Rule for execute to the program
run:
	$(PYTHON) $(SRC) config.txt

# Rule to clear trash files of Python
clean:
	rm -rf __pycache__ .mypy_cache

# Linting rule (Code policing)
# Linting with mandatory flags
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# Optional strict linting
lint-strict: 
	flake8 .
	mypy --strict 