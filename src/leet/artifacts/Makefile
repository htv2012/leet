PLATFORM := $(shell uname -s)
ifeq ($(PLATFORM),Linux)
	VIM_FLAGS := -p
endif

.PHONY: all debug edit lab lint py test

### Default target(s)
all: test

### Debug code
debug:
	PYTHONBREAKPOINT=pudb.set_trace PYTHONPATH=../../_common uv run pytest -s -vv

### Edit files
edit:
	gvim $(VIM_FLAGS) Makefile pyproject.toml *.py

### Start a Jupyter Lab
lab:
	PYTHONPATH=../../_common uv run jupyter lab

### Perform static analysis
lint:
	uv run ruff check --select I --fix . --quiet
	uv run ruff format . --quiet
	uv run ruff check . --fix --quiet

### Start a Python interpreter
py:
	PYTHONPATH=../../_common uv run ipython

### Run unit tests
test: lint
	uv run pytest -s -vv

