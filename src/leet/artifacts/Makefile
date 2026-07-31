.PHONY: all lab lint py test

### Default target(s)
all: test

### Perform static analysis
lint:
	uv run ruff check --select I --fix . --quiet
	uv run ruff format . --quiet
	uv run ruff check . --fix --quiet


### Run unit tests
test: lint
	uv run pytest -s -v

### Start a Python interpreter
py:
	PYTHONPATH=../../_common uv run ipython

### Start a Jupyter Lab
lab:
	PYTHONPATH=../../_common uv run jupyter lab

