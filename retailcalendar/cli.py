from datetime import date

import click

from retailcalendar import Cal454


@click.command()
@click.option("-s", "--start_month", type=int, default=1)
@click.option(
    "-d",
    "--days_highlight_off",
    is_flag=True,
    default=False,
    help="Disable today and holiday highlights",
)
@click.option(
    "-t",
    "--theme",
    type=str,
    default="default",
    help="Color theme: default, ocean, sunset, monokai, retro, matrix, sakura, ice, volcano",
)
@click.option(
    "-r",
    "--region",
    type=str,
    default="BR-PR-CWB",
    help="Holiday region: BR, BR-PR, BR-PR-CWB, BR-SP, BR-SP-SAO, US",
)
@click.argument("year", type=int, default=date.today().year)
def get_calendar(year, start_month, days_highlight_off, theme, region):
    c = Cal454(year, s_month=start_month)
    c.format_year(
        highlight_today=not days_highlight_off,
        highlight_holidays=not days_highlight_off,
        theme=theme,
        region=region,
    )


if __name__ == "__main__":
    get_calendar()
