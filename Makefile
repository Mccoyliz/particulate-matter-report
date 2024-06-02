# Variables
VENV_DIR = $(shell poetry env info --path)
PYTHON = poetry run python
POETRY = poetry

# Default target
all: install test docs

# Install dependencies
install:
	$(POETRY) install

# Run tests
test:
	$(PYTHON) -m unittest discover -s tests

# Generate docs
docs:
	$(POETRY) run pdoc --output-dir docs ./src

# Clean up
clean:
	rm -rf $(VENV_DIR)
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -type d -name '*.egg-info' -exec rm -r {} +

# Run PM2.5 Report
run:
	$(PYTHON) run.py $(DEVICE_ID) $(PROJECT_NAME)

# Phony targets
.PHONY: all install test docs clean run
