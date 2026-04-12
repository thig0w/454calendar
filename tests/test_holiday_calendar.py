from datetime import date

import pytest

from retailcalendar import HolidayCalendar

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def by_name(holidays: list[dict]) -> dict[str, dict]:
    return {h["name"]: h for h in holidays}


def get_holiday(holidays: list[dict], name: str) -> dict:
    for h in holidays:
        if h["name"] == name:
            return h
    raise KeyError(f"Holiday {name!r} not found")


# ---------------------------------------------------------------------------
# Structure
# ---------------------------------------------------------------------------


def test_holiday_dict_has_required_keys():
    h = HolidayCalendar("BR", 2025).holidays()[0]
    assert {"date", "observed", "name", "name_en", "type", "region"} <= h.keys()


def test_holidays_sorted_by_date():
    dates = [h["date"] for h in HolidayCalendar("BR", 2025).holidays()]
    assert dates == sorted(dates)


def test_dates_returns_date_objects():
    assert all(isinstance(d, date) for d in HolidayCalendar("BR", 2025).dates())


def test_observed_dates_returns_date_objects():
    assert all(
        isinstance(d, date) for d in HolidayCalendar("US", 2025).observed_dates()
    )


def test_region_code_stored_on_each_holiday():
    # sourcery skip: no-loop-in-tests
    for h in HolidayCalendar("BR-PR-CWB", 2025).holidays():
        assert h["region"] == "BR-PR-CWB"


def test_unknown_region_raises():
    with pytest.raises(ValueError, match="Unknown region"):
        HolidayCalendar("XX", 2025)


# ---------------------------------------------------------------------------
# BR — Fixed holidays
# ---------------------------------------------------------------------------


def test_br_fixed_holidays_2025():
    h = by_name(HolidayCalendar("BR", 2025).holidays())
    assert h["Confraternização Universal"]["date"] == date(2025, 1, 1)
    assert h["Tiradentes"]["date"] == date(2025, 4, 21)
    assert h["Dia do Trabalho"]["date"] == date(2025, 5, 1)
    assert h["Independência do Brasil"]["date"] == date(2025, 9, 7)
    assert h["Nossa Senhora Aparecida"]["date"] == date(2025, 10, 12)
    assert h["Finados"]["date"] == date(2025, 11, 2)
    assert h["Proclamação da República"]["date"] == date(2025, 11, 15)
    assert h["Dia da Consciência Negra"]["date"] == date(2025, 11, 20)
    assert h["Natal"]["date"] == date(2025, 12, 25)


# ---------------------------------------------------------------------------
# BR — Easter-based holidays (multi-year)
# ---------------------------------------------------------------------------

#  year | Easter | Carnival Mon | Carnival Tue | Good Friday | Corpus Christi
EASTER_CASES = [
    (
        2020,
        date(2020, 4, 12),
        date(2020, 2, 24),
        date(2020, 2, 25),
        date(2020, 4, 10),
        date(2020, 6, 11),
    ),
    (
        2021,
        date(2021, 4, 4),
        date(2021, 2, 15),
        date(2021, 2, 16),
        date(2021, 4, 2),
        date(2021, 6, 3),
    ),
    (
        2022,
        date(2022, 4, 17),
        date(2022, 2, 28),
        date(2022, 3, 1),
        date(2022, 4, 15),
        date(2022, 6, 16),
    ),
    (
        2023,
        date(2023, 4, 9),
        date(2023, 2, 20),
        date(2023, 2, 21),
        date(2023, 4, 7),
        date(2023, 6, 8),
    ),
    (
        2024,
        date(2024, 3, 31),
        date(2024, 2, 12),
        date(2024, 2, 13),
        date(2024, 3, 29),
        date(2024, 5, 30),
    ),
    (
        2025,
        date(2025, 4, 20),
        date(2025, 3, 3),
        date(2025, 3, 4),
        date(2025, 4, 18),
        date(2025, 6, 19),
    ),
    (
        2026,
        date(2026, 4, 5),
        date(2026, 2, 16),
        date(2026, 2, 17),
        date(2026, 4, 3),
        date(2026, 6, 4),
    ),
]


@pytest.mark.parametrize(
    "year,easter,carnival_mon,carnival_tue,good_friday,corpus",
    EASTER_CASES,
    ids=[str(c[0]) for c in EASTER_CASES],
)
def test_br_easter_based_holidays(
    year, easter, carnival_mon, carnival_tue, good_friday, corpus
):
    h = by_name(HolidayCalendar("BR", year).holidays())
    assert h["Páscoa"]["date"] == easter
    assert h["Carnaval — Segunda-feira"]["date"] == carnival_mon
    assert h["Carnaval — Terça-feira"]["date"] == carnival_tue
    assert h["Sexta-feira Santa"]["date"] == good_friday
    assert h["Corpus Christi"]["date"] == corpus


# ---------------------------------------------------------------------------
# BR — `since` filter: Dia da Consciência Negra (national since 2024)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("year", [2020, 2021, 2022, 2023])
def test_br_consciencia_negra_absent_before_2024(year):
    names = {h["name"] for h in HolidayCalendar("BR", year).holidays()}
    assert "Dia da Consciência Negra" not in names


@pytest.mark.parametrize("year", [2024, 2025, 2026])
def test_br_consciencia_negra_present_since_2024(year):
    names = {h["name"] for h in HolidayCalendar("BR", year).holidays()}
    assert "Dia da Consciência Negra" in names


# ---------------------------------------------------------------------------
# BR — Total holiday count
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "year,expected",
    [
        (2020, 13),  # Consciência Negra not yet a national holiday
        (2021, 13),
        (2022, 13),
        (2023, 13),
        (2024, 14),  # +Consciência Negra
        (2025, 14),
        (2026, 14),
    ],
)
def test_br_total_holiday_count(year, expected):
    assert len(HolidayCalendar("BR", year).holidays()) == expected


# ---------------------------------------------------------------------------
# Region inheritance
# ---------------------------------------------------------------------------


def test_br_pr_adds_emancipation_day():
    names = {h["name"] for h in HolidayCalendar("BR-PR", 2025).holidays()}
    assert "Emancipação do Paraná" in names
    assert get_holiday(
        HolidayCalendar("BR-PR", 2025).holidays(), "Emancipação do Paraná"
    )["date"] == date(2025, 12, 19)


def test_br_pr_cwb_adds_city_anniversary():
    h = by_name(HolidayCalendar("BR-PR-CWB", 2025).holidays())
    assert h["Aniversário de Curitiba"]["date"] == date(2025, 3, 29)


def test_br_pr_cwb_inherits_all_levels():
    names = {h["name"] for h in HolidayCalendar("BR-PR-CWB", 2025).holidays()}
    assert "Confraternização Universal" in names  # BR
    assert "Emancipação do Paraná" in names  # BR-PR
    assert "Aniversário de Curitiba" in names  # BR-PR-CWB


def test_br_sp_adds_revolution_day():
    h = by_name(HolidayCalendar("BR-SP", 2025).holidays())
    assert "Revolução Constitucionalista de 1932" in h
    assert h["Revolução Constitucionalista de 1932"]["date"] == date(2025, 7, 9)


def test_br_sp_sao_adds_city_anniversary():
    h = by_name(HolidayCalendar("BR-SP-SAO", 2025).holidays())
    assert h["Aniversário de São Paulo"]["date"] == date(2025, 1, 25)


def test_inheritance_adds_holidays_at_each_level():
    br = len(HolidayCalendar("BR", 2025).holidays())
    br_pr = len(HolidayCalendar("BR-PR", 2025).holidays())
    br_pr_cwb = len(HolidayCalendar("BR-PR-CWB", 2025).holidays())
    assert br < br_pr < br_pr_cwb


# ---------------------------------------------------------------------------
# US — Relative holidays
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "year,expected",
    [
        (2023, date(2023, 1, 16)),
        (2024, date(2024, 1, 15)),
        (2025, date(2025, 1, 20)),
    ],
)
def test_us_mlk_day(year, expected):
    assert (
        get_holiday(
            HolidayCalendar("US", year).holidays(), "Martin Luther King Jr. Day"
        )["date"]
        == expected
    )


@pytest.mark.parametrize(
    "year,expected",
    [
        (2023, date(2023, 5, 29)),
        (2024, date(2024, 5, 27)),
        (2025, date(2025, 5, 26)),
    ],
)
def test_us_memorial_day(year, expected):
    assert (
        get_holiday(HolidayCalendar("US", year).holidays(), "Memorial Day")["date"]
        == expected
    )


@pytest.mark.parametrize(
    "year,expected",
    [
        (2023, date(2023, 11, 23)),
        (2024, date(2024, 11, 28)),
        (2025, date(2025, 11, 27)),
    ],
)
def test_us_thanksgiving(year, expected):
    assert (
        get_holiday(HolidayCalendar("US", year).holidays(), "Thanksgiving Day")["date"]
        == expected
    )


# ---------------------------------------------------------------------------
# US — `observed` adjustments
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "year,canonical,observed",
    [
        (2022, date(2022, 1, 1), date(2022, 1, 3)),  # Saturday → next Monday
        (2023, date(2023, 1, 1), date(2023, 1, 2)),  # Sunday → next Monday
        (2025, date(2025, 1, 1), date(2025, 1, 1)),  # Wednesday → no shift
    ],
)
def test_us_new_years_observed(year, canonical, observed):
    h = get_holiday(HolidayCalendar("US", year).holidays(), "New Year's Day")
    assert h["date"] == canonical
    assert h["observed"] == observed


@pytest.mark.parametrize(
    "year,canonical,observed",
    [
        (2021, date(2021, 12, 25), date(2021, 12, 24)),  # Saturday → nearest Friday
        (2022, date(2022, 12, 25), date(2022, 12, 26)),  # Sunday → nearest Monday
        (2023, date(2023, 12, 25), date(2023, 12, 25)),  # Monday → no shift
    ],
)
def test_us_christmas_observed(year, canonical, observed):
    h = get_holiday(HolidayCalendar("US", year).holidays(), "Christmas Day")
    assert h["date"] == canonical
    assert h["observed"] == observed


@pytest.mark.parametrize(
    "year,observed",
    [
        (2021, date(2021, 7, 5)),  # Sunday → nearest Monday
        (2022, date(2022, 7, 4)),  # Monday → no shift
        (2025, date(2025, 7, 4)),  # Friday → no shift
    ],
)
def test_us_independence_day_observed(year, observed):
    h = get_holiday(HolidayCalendar("US", year).holidays(), "Independence Day")
    assert h["observed"] == observed


# ---------------------------------------------------------------------------
# US — `since` filter: Juneteenth (federal holiday since 2021)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("year", [2019, 2020])
def test_us_juneteenth_absent_before_2021(year):
    names = {h["name"] for h in HolidayCalendar("US", year).holidays()}
    assert "Juneteenth National Independence Day" not in names


@pytest.mark.parametrize("year", [2021, 2022, 2025])
def test_us_juneteenth_present_since_2021(year):
    names = {h["name"] for h in HolidayCalendar("US", year).holidays()}
    assert "Juneteenth National Independence Day" in names
