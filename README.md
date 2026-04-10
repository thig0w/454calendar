# retailcalendar

A Python package for working with the [NRF 4-5-4 Retail Calendar](https://nrf.com/resources/4-5-4-calendar).

The retail calendar groups weeks into months following a **4-5-4 week pattern** per quarter, giving retailers a consistent structure for fiscal year reporting. Some years have 53 weeks (a "53-week year") — this package handles that automatically.

## Installation

```bash
pip install retailcalendar
```

## CLI Usage

```bash
# Display the 4-5-4 calendar for the current year
454cal

# Display for a specific year
454cal 2025

# Use a different fiscal year start month (default is February)
454cal --start_month 1 2025
```

The output is a color-formatted calendar printed to the terminal, organized with 3 months per row and week numbers on the left.

## Python API

```python
from retailcalendar import Cal454

# Create a calendar for fiscal year 2025 (starts February 2025)
cal = Cal454(year=2025, s_month=2)

# Display the full calendar
cal.format_year()

# Get month start/end dates (list of 12 dates)
cal.month_start_dates()
cal.month_end_dates()

# Get quarter start/end dates (list of 4 dates)
cal.quarter_start_dates()
cal.quarter_end_dates()

# Get all weeks in a given month (1-indexed)
cal.month_days_by_week(month=1)

# Get all weeks for the entire year
cal.year_days_by_week()

# Check if a year has 53 weeks
Cal454.has_43_weeks(year=2023)           # True
Cal454.has_43_weeks(year=2023, s_month=1)  # False
```

### `Cal454` Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `year` | current year | Fiscal year to calculate |
| `s_month` | `2` | Fiscal year start month (1–12) |

### `format_year()` Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `w_col` | `2` | Column width per day (min 2) |
| `space_month` | `3` | Space between month columns (min 3) |
| `line_months` | `3` | Number of months per row (min 3) |

## How the 4-5-4 Calendar Works

Each fiscal quarter follows a 4-5-4 week pattern:

| Month in Quarter | Weeks |
|-----------------|-------|
| First           | 4     |
| Second          | 5     |
| Third           | 4     |

The fiscal year normally has **52 weeks**. Per NRF rules, a **53rd week** is added to the last month of the year when the last day of a standard 52-week year has 4 or more days remaining in the start month. Known 53-week years (February start): 2000, 2006, 2012, 2017, 2023, 2028.

The fiscal year starts on the **Sunday on or before February 1** (or the configured start month).

## Development

```bash
git clone https://github.com/thig0w/454calendar.git
cd 454calendar

# Set up development environment (venv, dev deps, pre-commit hooks)
make devenv

# Run formatter, linter, and tests
make precommit

# Run tests only
.venv/bin/pytest

# Build distribution package
make build

# Clean everything
make clean
```

**Requirements:** Python 3.10+

## License

GNU General Public License v3.0 — see [LICENSE](LICENSE).
