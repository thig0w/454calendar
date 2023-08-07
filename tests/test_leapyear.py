# -*- coding: utf-8 -*-
from retailcalendar import Cal454


def test_leap_years():
    leap_years_month_2 = [2000, 2006, 2012, 2017, 2023, 2028]
    leap_years_month_1 = [2003, 2008, 2014, 2020, 2025]

    # sourcery skip: no-loop-in-tests
    for year in range(2000, 2030):
        assert Cal454.has_43_weeks(year) == eval(f"year in {leap_years_month_2}")
        assert Cal454.has_43_weeks(year, s_month=1) == eval(
            f"year in {leap_years_month_1}"
        )


def test_leap_years_contents():
    # sourcery skip: no-loop-in-tests
    for year in range(2000, 2030):
        c = Cal454(year).year_days_by_week()
        assert len(c) == 12
        assert len(c[0]) == 4
        assert len(c[1]) == 5
        assert len(c[2]) == 4
        assert len(c[3]) == 4
        assert len(c[4]) == 5
        assert len(c[5]) == 4
        assert len(c[6]) == 4
        assert len(c[7]) == 5
        assert len(c[8]) == 4
        assert len(c[9]) == 4
        assert len(c[10]) == 5
        weeks_last_month = 5 if Cal454.has_43_weeks(year) else 4
        assert len(c[11]) == weeks_last_month
