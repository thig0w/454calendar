# -*- coding: utf-8 -*-
from datetime import date

import click

from retailcalendar import Cal454


@click.command()
@click.option("-s", "--start_month", type=int, default=1)
@click.argument("year", type=int, default=date.today().year)
def get_calendar(year, start_month):
    c = Cal454(year, s_month=start_month)
    c.format_year()


if __name__ == "__main__":
    get_calendar()
