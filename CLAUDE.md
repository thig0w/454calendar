# CLAUDE.md

## Project Overview

`retailcalendar` is a Python package that implements the NRF (National Retail Federation) 4-5-4 Retail Calendar. The retail calendar groups weeks into months following a 4-5-4 week pattern per quarter, used by retailers for consistent fiscal year reporting. Some fiscal years have 53 weeks instead of 52 (called "43-week years" in the codebase).

## Package Structure

```
retailcalendar/
├── __init__.py       # Exports Cal454 class
├── cal.py            # Core logic: Cal454 class (~192 lines)
└── cli.py            # CLI entry point using Click
tests/
└── test_leapyear.py  # Tests for 43-week detection and calendar structure
```

## Core Concepts

- **Fiscal year**: Typically starts the Sunday on or before February 1
- **4-5-4 pattern**: Each quarter has months of 4, 5, and 4 weeks respectively (stored in `QUARTER_CONFIGURATION`)
- **43-week year**: A 53-week fiscal year — the last month gets +1 week (5 instead of 4)
- **`has_43_weeks()`**: Cached classmethod implementing the NRF algorithm for 53-week detection
- Week starts on **Sunday** (`STARTING_WEEKDAY = 7` in ISO weekday notation)

## Key Commands

```bash
# Run CLI
454cal [YEAR]
454cal --start_month 2 2025

# Development setup (uv)
make devenv       # uv sync --group dev + install pre-commit hooks
make precommit    # Format, lint, and test everything
make build        # uv build — produces dist/
make clean        # Remove .venv, dist/, and caches
make cleancache   # Remove __pycache__, .pytest_cache, .ruff_cache
```

## Running Tests

```bash
uv run pytest
# or via make:
make precommit
```

## Code Style & Tooling

- **Formatter**: `black` — run via `uv run black .`
- **Linter**: `ruff` — run via `uv run ruff check . --fix`
- **Import sorter**: `isort`
- **Pre-commit**: enforces formatting on every commit (installed via `make devenv`)
- **Python**: 3.10+ required (uses `list[...]` type hints without `from __future__`)
- **`UV_LINK_MODE=copy`**: set in makefile for Windows filesystem compatibility (cloud/OneDrive drives don't support hardlinks)

## CLI Entry Point

Defined in `pyproject.toml`:
```
454cal = "retailcalendar.cli:get_calendar"
```

The CLI default for `--start_month` is `1` (January) in `cli.py`, but the class default is `2` (February). Keep this in mind if changing defaults.

## Dependencies

Runtime (in `pyproject.toml` `[project].dependencies`): `click`, `rich`
Dev (in `pyproject.toml` `[dependency-groups].dev`): `black`, `ruff`, `isort`, `pytest`, `pytest-clarity`, `pytest-dotenv`, `pydocstyle`, `httpx`, `sourcery`, `pre-commit`

Pytest config lives in `[tool.pytest.ini_options]` in `pyproject.toml` — no separate `pytest.ini`.

## Release

GitHub Actions (`.github/workflows/release.yml`) publishes to PyPI on GitHub release creation using the `PYPI_TOKEN` secret. Uses `astral-sh/setup-uv` and `uv build`.
