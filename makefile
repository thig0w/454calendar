export UV_LINK_MODE=copy

.PHONY: run clean cleancache devenv precommit build

run:
	uv run 454cal 2026

cleancache:
	find . -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .ruff_cache

clean: cleancache
	rm -rf .venv
	rm -rf dist retailcalendar.egg-info

devenv:
	uv sync --group dev
	uv run pre-commit install

precommit: devenv
	uv run black .
	uv run ruff check . --fix
	uv run pre-commit run --all-files
	uv run pytest

build:
	uv build
