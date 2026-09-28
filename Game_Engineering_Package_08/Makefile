# Use "make PYTHON=python3 test" where the executable is named python3.
PYTHON ?= python3
.PHONY: test preflight vectors hdl synthesis spice
preflight:
	$(PYTHON) tools/preflight.py
test:
	$(PYTHON) tools/run_python_tests.py
vectors:
	$(PYTHON) tools/generate_cpu_vectors.py
hdl:
	$(PYTHON) tools/run_hdl.py
synthesis:
	$(PYTHON) tools/run_synthesis.py
spice:
	$(PYTHON) tools/run_spice.py
