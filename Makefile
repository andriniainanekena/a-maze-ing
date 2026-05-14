PYTHON = python3
MAIN = a_maze_ing.py
CONFIG = config.txt

.PHONY: help run clean

help:
  @echo "make run   → Run the program"
  @echo "make clean → Clean"
  @echo "make test  → Validate the maze"

run:
  $(PYTHON) $(MAIN) $(CONFIG)

clean: 
  rm -f maze.txt
  find . -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
  @echo "Cleaning complete."

test:
  python3 output_validator.py maze.txt
