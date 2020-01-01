PYTHON ?= python

install:
	python install.py

test:
	cd test && $(PYTHON) testlex.py
	cd test && $(PYTHON) testyacc.py

.PHONY: install test
