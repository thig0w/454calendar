from datetime import date, timedelta
from functools import lru_cache
from pathlib import Path

import yaml

_YAML_PATH = Path(__file__).parent / "holidays.yaml"

_WEEKDAY_ISO = {
    "monday": 1,
    "tuesday": 2,
    "wednesday": 3,
    "thursday": 4,
    "friday": 5,
    "saturday": 6,
    "sunday": 7,
}


@lru_cache(maxsize=1)
def _load_yaml() -> dict:
    return yaml.safe_load(_YAML_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=16)
def _easter(year: int) -> date:
    """Compute Easter Sunday using the Anonymous Gregorian Algorithm.

    The algorithm works in three phases:

    Phase 1 — locate the ecclesiastical full moon:
      The Metonic cycle repeats lunar phases every 19 years.
      ``golden_number`` is the year's position in that cycle (0–18).
      The century-level corrections (``metonic_adj``, ``century_adj``) account
      for the Gregorian calendar's extra leap-year rules vs. the Julian calendar.
      ``epact`` is the number of days after March 21 on which the ecclesiastical
      full moon falls (the "paschal full moon").

    Phase 2 — advance to the following Sunday:
      Easter must be a Sunday. ``weekday_adj`` shifts the paschal full moon date
      forward to the next Sunday.

    Phase 3 — convert to a calendar date:
      ``month_adj`` corrects for the rare case where the combined offset would
      push the date past April 25 (the latest Easter can legally fall).
      The final arithmetic maps the offsets to a concrete month and day.

    Reference: https://en.wikipedia.org/wiki/Date_of_Easter#Anonymous_Gregorian_algorithm
    """
    # Phase 1: ecclesiastical full moon
    golden_number = year % 19  # position in 19-year Metonic cycle
    century, year_of_century = divmod(year, 100)
    century_leaps = century // 4  # leap-year centuries completed
    century_remainder = century % 4
    metonic_adj = (century + 8) // 25  # Gregorian correction to Metonic cycle
    century_adj = (
        century - metonic_adj + 1
    ) // 3  # correction for skipped leap centuries
    epact = (19 * golden_number + century - century_leaps - century_adj + 15) % 30

    # Phase 2: advance to Sunday
    year_leaps = year_of_century // 4  # leap years in current century so far
    year_remainder = year_of_century % 4
    weekday_adj = (
        32 + 2 * century_remainder + 2 * year_leaps - epact - year_remainder
    ) % 7

    # Phase 3: calendar date
    month_adj = (
        golden_number + 11 * epact + 22 * weekday_adj
    ) // 451  # pushes Apr 26+ back
    combined = epact + weekday_adj - 7 * month_adj + 114
    month = combined // 31
    day = (combined % 31) + 1
    return date(year, month, day)


def _nth_weekday(year: int, month: int, weekday: str, ordinal: int) -> date:
    """Return the Nth occurrence of a weekday in the given month/year.

    ordinal: 1=first, 2=second, -1=last, -2=second-to-last, etc.
    """
    iso_wd = _WEEKDAY_ISO[weekday.lower()]
    if ordinal > 0:
        first = date(year, month, 1)
        delta = (iso_wd - first.isoweekday()) % 7
        return first + timedelta(days=delta) + timedelta(weeks=ordinal - 1)
    else:
        # Last day of month
        if month == 12:
            last = date(year, 12, 31)
        else:
            last = date(year, month + 1, 1) - timedelta(days=1)
        delta = (last.isoweekday() - iso_wd) % 7
        last_occurrence = last - timedelta(days=delta)
        return last_occurrence + timedelta(weeks=ordinal + 1)


def _apply_observed(d: date, observed: str | None) -> date:
    """Return the observed (legally effective) date after weekend adjustment."""
    if not observed or observed == "none":
        return d
    iso_wd = d.isoweekday()
    if observed == "next_monday":
        if iso_wd == 6:  # Saturday → following Monday
            return d + timedelta(days=2)
        if iso_wd == 7:  # Sunday → following Monday
            return d + timedelta(days=1)
    elif observed == "nearest_weekday":
        if iso_wd == 6:  # Saturday → preceding Friday
            return d - timedelta(days=1)
        if iso_wd == 7:  # Sunday → following Monday
            return d + timedelta(days=1)
    return d


class HolidayCalendar:
    """Calculates public holidays for a region and year defined in holidays.yaml.

    Region codes follow a hierarchy (e.g. BR → BR-SP → BR-SP-SAO) and
    child regions inherit all holidays from their parent.

    Supported rule types: fixed, relative, offset, complex.

    Usage::

        cal = HolidayCalendar("BR-PR-CWB", 2025)
        for h in cal.holidays():
            print(h["date"], h["name"])
    """

    def __init__(self, region: str, year: int) -> None:
        self._region = region
        self._year = year
        self._data = _load_yaml()
        if region not in self._data["regions"]:
            raise ValueError(f"Unknown region: {region!r}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def holidays(self) -> list[dict]:
        """Return all holidays sorted by canonical date.

        Each dict contains:

        - ``date``     — canonical holiday date (``datetime.date``)
        - ``observed`` — legally effective date after weekend shift (``datetime.date``)
        - ``name``     — local name
        - ``name_en``  — English name (``None`` when absent)
        - ``type``     — rule type (``"fixed"``, ``"relative"``, ``"offset"``, ``"complex"``)
        - ``region``   — region code used for the lookup
        """
        rules = self._collect_rules(self._region)
        result = []
        for rule in rules:
            d = self._resolve_date(rule)
            if d is None:
                continue
            result.append(
                {
                    "date": d,
                    "observed": _apply_observed(d, rule.get("observed")),
                    "name": rule["name"],
                    "name_en": rule.get("name_en"),
                    "type": rule["type"],
                    "region": self._region,
                }
            )
        result.sort(key=lambda x: x["date"])
        return result

    def dates(self) -> list[date]:
        """Return canonical holiday dates sorted ascending."""
        return [h["date"] for h in self.holidays()]

    def observed_dates(self) -> list[date]:
        """Return observed (legally effective) holiday dates sorted ascending."""
        return [h["observed"] for h in self.holidays()]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _collect_rules(self, region: str) -> list[dict]:
        regions = self._data["regions"]
        reg = regions[region]
        parent = reg.get("inherits")
        inherited = self._collect_rules(parent) if parent else []
        return inherited + reg.get("holidays", [])

    def _resolve_date(self, rule: dict) -> date | None:
        """Return the holiday date for self._year, or None if not applicable."""
        since = rule.get("since")
        if since is not None and self._year < since:
            return None

        year = self._year
        rtype = rule["type"]

        if rtype == "fixed":
            return date(year, rule["month"], rule["day"])

        if rtype == "relative":
            return _nth_weekday(year, rule["month"], rule["weekday"], rule["ordinal"])

        if rtype == "offset":
            base = rule["base"]
            if base == "easter":
                base_date = _easter(year)
            else:
                raise ValueError(f"Unknown base algorithm: {base!r}")
            return base_date + timedelta(days=rule["offset_days"])

        if rtype == "complex":
            algo = rule["algorithm"]
            if algo == "easter":
                return _easter(year)
            raise ValueError(f"Unknown complex algorithm: {algo!r}")

        raise ValueError(f"Unknown holiday type: {rtype!r}")
