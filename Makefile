PYTHON=python3
VENV=.venv

# Setup and install all of the required tools for building, testing,
# and deploying
setup::
	rm -rf $(VENV)
	$(PYTHON) -m venv $(VENV)
	./$(VENV)/bin/python -m pip install pytest
	./$(VENV)/bin/python -m pip install pytest-cov
	./$(VENV)/bin/python -m pip install build
	./$(VENV)/bin/python -m pip install twine

# Run unit tests
test::
	./$(VENV)/bin/python -m pip install .
	./$(VENV)/bin/python tests/testlex.py
	./$(VENV)/bin/python tests/testyacc.py

# Build an artifact suitable for installing with pip
build::
	./$(VENV)/bin/python -m build

# Install into the default Python
install::
	$(PYTHON) -m pip install .
