PYTHON = python3
MAIN = a_maze_ing.py
INPUT = config.txt
VENV = maze
MLX_WHEEL = vendor/mlx-2_2-py3-ubuntu-any.whl

.SILENT:

help:
	@echo "Available commands:"
	@echo "  make setup        - Create virtual environment and install dependencies"
	@echo "  make install      - Install project dependencies"
	@echo "  make install-mlx  - Install the optional MLX graphical display (Ubuntu/Debian)"
	@echo "  make run          - Execute the main script"
	@echo "  make debug        - Run the main script in debug mode (pdb)"
	@echo "  make clean        - Remove all temporary files and caches"
	@echo "  make lint         - Run flake8 and mypy with standard checks"
	@echo "  make lint-strict  - Run flake8 and mypy with strict mode"
	@echo "  make build        - Build the Python package"
	@echo "  make help         - Show this help message"

build:
	$(PYTHON) -m build

install:
	pip install -r requirements.txt

install-mlx:
	SITE_PACKAGES=$$($(PYTHON) -c "import sysconfig; print(sysconfig.get_paths()['purelib'])"); \
	$(PYTHON) -m zipfile -e $(MLX_WHEEL) "$$SITE_PACKAGES"; \
	echo "MLX installed into $$SITE_PACKAGES"

setup:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt
	@echo "source maze/bin/activate"
	@echo "make install-mlx  # optional, for DISPLAY_MODE=MLX (Ubuntu/Debian)"

run:
	$(PYTHON) $(MAIN) $(INPUT)

debug:
	$(PYTHON) -m pdb $(MAIN) $(INPUT)

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name dist -exec rm -rf {} +
	find . -type d -name mazegen.egg-info -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "output.txt" -delete

lint:
	$(PYTHON) -m flake8 . --exclude=maze
	mypy . --explicit-package-bases \
	        --warn-return-any \
	        --ignore-missing-imports \
	        --disallow-untyped-defs \
	        --check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 . --exclude=maze
	mypy --strict . \
	     --explicit-package-bases

.PHONY: install install-mlx run debug clean lint lint-strict build help setup

.DEFAULT_GOAL := help
