PYTHON ?= python

ifeq ($(OS),Windows_NT)
VENV_PYTHON := .venv\Scripts\python.exe
else
VENV_PYTHON := .venv/bin/python
endif

.PHONY: venv run clean

venv:
	$(PYTHON) -m venv .venv

run: venv
	$(VENV_PYTHON) -m ai_playground

clean:
	$(PYTHON) -c "import shutil; shutil.rmtree('.venv', ignore_errors=True)"
