# -*- coding: utf-8 -*-
from calendar import month_abbr, monthrange
from datetime import date, timedelta
from functools import lru_cache, reduce


class Cal454:
    """
    Class to handle the NRF 4-5-4 Calendar
    #TODO: Work this description

    About NRF 4-5-4 calendar: https://nrf.com/resources/4-5-4-calendar
    """

    # Starting Fiscal Month - It usually starts in February to maintains end of year
    # holidays sales and returns in the same fiscal year
    YEAR_START_MONTH = 2
    # Starting Weekday - usually Sunday (iso-weekday = 7)
    STARTING_WEEKDAY = 7
    # Usually 4-5-4 - but it can be configurable
    QUARTER_CONFIGURATION = [4, 5, 4]

    def __init__(self, year=date.today().year, s_month=YEAR_START_MONTH) -> None:
        self._year = year
        self._year_start_month = s_month
        self._quarter_configuration = self.QUARTER_CONFIGURATION * 4
        if self.has_43_weeks(year=self._year, s_month=self._year_start_month):
            self._quarter_configuration[-1] += 1

        self._year_start_day = self.year_start_date(
            year=self._year, s_month=self._year_start_month
        )
        self._year_end_day = self.year_end_date(
            year=self._year, s_month=self._year_start_month
        )

    @classmethod
    def year_start_date(cls, year, s_month=YEAR_START_MONTH) -> date:
        gregorian_first_day = date(year, s_month, 1)
        weekday = gregorian_first_day.isoweekday() % 7

        return (
            gregorian_first_day + timedelta(days=7 - weekday)
            if (cls.has_43_weeks(year - 1, s_month=s_month))
            else gregorian_first_day - timedelta(days=weekday)
        )

    @classmethod
    def year_end_date(cls, year, s_month=YEAR_START_MONTH) -> date:
        return cls.year_start_date(year + 1, s_month=s_month) - timedelta(days=1)

    @classmethod
    @lru_cache(maxsize=10)
    def has_43_weeks(cls, year, s_month=YEAR_START_MONTH) -> bool:
        """
        As defined by NRF, the year starts on the week that contains de first day of
        February, except when the week has four or more days left in January,
        when this happens the last retail year had a 53rd week.

        https://nrf.com/resources/4-5-4-calendar#:~:text=How%20does%20NRF%20determine%20the,a%2053rd%20week%20is%20added.
        """
        # Calculating last year dates, even if it is not a 53weeks year,
        # it will adjust the fist day for our year
        ly_gregorian_first_day = date(year - 1, s_month, 1)
        ly_weekday = ly_gregorian_first_day.isoweekday() % 7
        ly_first_day = ly_gregorian_first_day - timedelta(days=ly_weekday)
        ly_last_day = ly_first_day + timedelta(weeks=52) - timedelta(days=1)
        if monthrange(ly_last_day.year, ly_last_day.month)[1] - ly_last_day.day >= 4:
            ly_last_day += timedelta(days=7)
        # Knowing the real first week, lets check if it has the 53rd week
        first_day = ly_last_day + timedelta(days=1)
        last_day = first_day + timedelta(weeks=52) - timedelta(days=1)
        return (
            False
            if last_day.month == s_month
            else monthrange(last_day.year, last_day.month)[1] - last_day.day >= 4
        )

    def month_start_dates(self) -> list[date]:
        days_from_start = [sum(self._quarter_configuration[:x]) * 7 for x in range(12)]
        return [self._year_start_day + timedelta(days=d) for d in days_from_start]

    def month_end_dates(self) -> list[date]:
        days_from_start = [
            sum(self._quarter_configuration[: x + 1]) * 7 for x in range(12)
        ]
        return [self._year_start_day + timedelta(days=d - 1) for d in days_from_start]

    def quarter_start_dates(self) -> list[date]:
        days_from_start = [
            sum(self._quarter_configuration[: x * 3]) * 7 for x in range(4)
        ]
        return [self._year_start_day + timedelta(days=d) for d in days_from_start]

    def quarter_end_dates(self) -> list[date]:
        days_from_start = [
            sum(self._quarter_configuration[: (x + 1) * 3]) * 7 for x in range(4)
        ]
        return [self._year_start_day + timedelta(days=d - 1) for d in days_from_start]

    def month_days_by_week(self, month) -> list[list[int, list[date]]]:
        if month == 1:
            week_no = 1
        else:
            week_no = (
                reduce(lambda a, b: a + b, self._quarter_configuration[: month - 1]) + 1
            )
        months_dates = self.month_start_dates()

        return [
            [
                week_no + i,
                [
                    months_dates[month - 1] + timedelta(days=j + (7 * i))
                    for j in range(7)
                ],
            ]
            for i in range(self._quarter_configuration[month - 1])
        ]

    def year_days_by_week(self) -> list[list[list[int, list[date]]]]:
        return [self.month_days_by_week(i) for i in range(1, 13)]

    def format_year(self, w_col=2, space_month=3, line_months=3) -> None:
        width_col = max(2, w_col)
        space_month = max(3, space_month)
        months_per_row = max(3, line_months)
        week_number_size = 4
        month_width = ((width_col + 1) * 7) + week_number_size
        cal_size = ((month_width + space_month) * months_per_row) - space_month

        days = self.year_days_by_week()

        fmt = []
        a = fmt.append

        a(f"{self._year : ^{cal_size}}".rstrip())
        a("\n\n")

        for months in range(1, 12, months_per_row):
            for month in range(months, months + months_per_row):
                adj_month = (
                    12
                    if (month - 1 + self._year_start_month) % 12 == 0
                    else (month - 1 + self._year_start_month) % 12
                )
                a(f"{month_abbr[adj_month] : ^{month_width}}{'':^{space_month}}")
            fmt[-1] = fmt[-1].rstrip()
            a("\n")
            for week in range(5):
                for month in range(months, months + months_per_row):
                    try:
                        # week number
                        a(f"{days[month - 1][week][0]:02}| ")
                        for day in range(7):
                            a(f"{days[month - 1][week][1][day].day:02}")
                            a(" ")
                    except IndexError:
                        a(f"{'':^{month_width}}")
                    a(f"{'':^{space_month}}")
                a("\n")
            a("\n")

        print("".join(fmt))


if __name__ == "__main__":
    # Cal454(2023).format_year()
    # pprint(Cal454(2023,s_month=2).month_days_by_week(1))
    # pprint(Cal454(2023,s_month=2).month_days_by_week(12))
    # pprint(Cal454(2023,s_month=2).year_days_by_week())
    # print(Cal454(2023).format_year())
    Cal454(2023).format_year()
