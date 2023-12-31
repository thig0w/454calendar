VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

.PHONY: run clean cleancache devenv


$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

run: $(VENV)/bin/activate
	$(PYTHON) cli.py 2023

cleancache:
	find . -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .ruff_cache

clean: cleancache
	rm -rf $(VENV)
	rm -rf .tox
	rm -rf .pre-commit-config.yaml tox.ini pytest.ini
	rm -rf dist retailcalendar.egg-info

devenv: $(VENV)/bin/activate tox.ini pytest.ini .pre-commit-config.yaml
	$(PIP) install black pre-commit pydocstyle pytest pytest-clarity pytest-dotenv tox ruff httpx isort sourcery
	if [ ! -d ".git" ]; then git init; fi
	pre-commit install

precommit: devenv
	black .
	ruff . --fix
	pre-commit run --all-files
	tox

build: $(VENV)/bin/activate
	$(PYTHON) -m pip install --upgrade build
	$(PYTHON) -m build

include files.mk
