# retailcalendar

A Python package for working with the [NRF 4-5-4 Retail Calendar](https://nrf.com/resources/4-5-4-calendar) and public holiday calendars for Brazil and the United States.

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

# Use a different fiscal year start month (default is January)
454cal --start_month 2 2025

# Disable today and holiday highlights
454cal -d 2025
```

The output is a color-formatted calendar printed to the terminal, organized with 3 months per row and week numbers on the left. Public holidays are highlighted with a green background; today is highlighted in purple.

### CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `-s` / `--start_month` | `1` | Fiscal year start month (1–12) |
| `-d` / `--days_highlight_off` | off | Disable today and holiday highlights |
| `YEAR` | current year | Fiscal year to display |

## Python API

### `Cal454` — NRF 4-5-4 Retail Calendar

```python
from retailcalendar import Cal454

# Create a calendar for fiscal year 2025 (starts February 2025)
cal = Cal454(year=2025, s_month=2)

# Display the full calendar (holidays highlighted by default)
cal.format_year()
cal.format_year(highlight_today=False, highlight_holidays=False)

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
Cal454.has_43_weeks(year=2023)            # True
Cal454.has_43_weeks(year=2023, s_month=1) # False
```

#### `Cal454` Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `year` | current year | Fiscal year to calculate |
| `s_month` | `2` | Fiscal year start month (1–12) |

#### `format_year()` Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `w_col` | `2` | Column width per day (min 2) |
| `space_month` | `3` | Space between month columns (min 3) |
| `line_months` | `3` | Number of months per row (min 3) |
| `highlight_today` | `True` | Highlight today's date in purple |
| `highlight_holidays` | `True` | Highlight public holidays in green |

---

### `HolidayCalendar` — Public Holiday Calculator

Calculates public holidays for a given region and year. Regions are defined in `holidays.yaml` and support inheritance — a city-level region automatically includes state and national holidays.

```python
from retailcalendar import HolidayCalendar

cal = HolidayCalendar("BR-PR-CWB", 2025)

# Full list of holidays as dicts, sorted by date
for h in cal.holidays():
    print(h["date"], h["name"])

# Just the canonical holiday dates
cal.dates()           # list[date]

# Observed (legally effective) dates after weekend shifts
cal.observed_dates()  # list[date]
```

Each dict returned by `holidays()` contains:

| Key | Type | Description |
|-----|------|-------------|
| `date` | `date` | Canonical holiday date |
| `observed` | `date` | Effective date after weekend adjustment (`next_monday` / `nearest_weekday`) |
| `name` | `str` | Local name |
| `name_en` | `str \| None` | English name |
| `type` | `str` | Rule type: `fixed`, `relative`, `offset`, or `complex` |
| `region` | `str` | Region code used for the lookup |

#### Supported Regions

| Code | Description |
|------|-------------|
| `BR` | Brazil — national holidays |
| `BR-PR` | Paraná state (inherits `BR`) |
| `BR-PR-CWB` | Curitiba city (inherits `BR-PR`) |
| `BR-SP` | São Paulo state (inherits `BR`) |
| `BR-SP-SAO` | São Paulo city (inherits `BR-SP`) |
| `US` | United States — federal holidays |

#### Holiday rule types

| Type | Description | Example |
|------|-------------|---------|
| `fixed` | Same day/month every year | Christmas (Dec 25) |
| `relative` | Nth weekday of a given month | Thanksgiving (4th Thursday of November) |
| `offset` | N days before/after a base algorithm | Good Friday (Easter − 2 days) |
| `complex` | Full algorithm | Easter Sunday |

#### `since` field

Holidays with a `since` year are excluded for earlier years. For example, Brazil's Dia da Consciência Negra (`since: 2024`) does not appear for 2023 and earlier.

---

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
uv run pytest

# Build distribution package
make build

# Clean everything
make clean
```

**Requirements:** Python 3.10+

## License

GNU General Public License v3.0 — see [LICENSE](LICENSE).
