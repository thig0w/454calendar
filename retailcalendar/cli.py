from datetime import date

import click

from retailcalendar import Cal454


@click.command()
@click.option("-s", "--start_month", type=int, default=1)
@click.option(
    "-d", "--days_off", is_flag=True, default=False, help="Disable today highlight"
)
@click.argument("year", type=int, default=date.today().year)
def get_calendar(year, start_month, days_off):
    c = Cal454(year, s_month=start_month)
    c.format_year(highlight_today=not days_off)


if __name__ == "__main__":
    get_calendar()
