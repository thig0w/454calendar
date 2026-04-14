from dataclasses import dataclass


@dataclass(frozen=True)
class CalendarTheme:
    year_title: str
    month_name: str
    day_header: str
    week_number: str
    today: str
    holiday: str


THEMES: dict[str, CalendarTheme] = {
    "default": CalendarTheme(
        year_title="bold red",
        month_name="yellow2",
        day_header="bright_black",
        week_number="spring_green2",
        today="bold white on purple",
        holiday="bold bright_white on green4",
    ),
    "ocean": CalendarTheme(
        year_title="bold cyan1",
        month_name="deep_sky_blue1",
        day_header="steel_blue3",
        week_number="turquoise2",
        today="bold white on dodger_blue2",
        holiday="bold bright_white on dark_cyan",
    ),
    "sunset": CalendarTheme(
        year_title="bold bright_red",
        month_name="orange1",
        day_header="dark_orange3",
        week_number="gold1",
        today="bold white on dark_red",
        holiday="bold bright_white on orange3",
    ),
    "monokai": CalendarTheme(
        year_title="bold bright_magenta",
        month_name="green_yellow",
        day_header="grey58",
        week_number="chartreuse1",
        today="bold white on medium_purple3",
        holiday="bold bright_white on dark_olive_green3",
    ),
    "retro": CalendarTheme(
        # Amber CRT monitor — warm monochrome, nostalgic terminal feel
        year_title="bold yellow3",
        month_name="dark_orange",
        day_header="orange3",
        week_number="gold1",
        today="bold black on yellow3",
        holiday="bold black on orange1",
    ),
    "matrix": CalendarTheme(
        # Green phosphor terminal — hacker monochrome aesthetic
        year_title="bold bright_green",
        month_name="green3",
        day_header="dark_green",
        week_number="green1",
        today="bold black on bright_green",
        holiday="bold black on green3",
    ),
    "sakura": CalendarTheme(
        # Japanese cherry blossom — soft pinks and mauves
        year_title="bold pink1",
        month_name="light_pink1",
        day_header="rosy_brown",
        week_number="light_pink3",
        today="bold white on deep_pink4",
        holiday="bold white on hot_pink3",
    ),
    "ice": CalendarTheme(
        # Arctic frost — crisp whites and pale blues, high contrast
        year_title="bold white",
        month_name="light_cyan1",
        day_header="grey70",
        week_number="pale_turquoise1",
        today="bold black on white",
        holiday="bold black on pale_turquoise4",
    ),
    "volcano": CalendarTheme(
        # Volcanic lava — deep reds, glowing yellows, intense contrast
        year_title="bold bright_yellow",
        month_name="red1",
        day_header="dark_red",
        week_number="orange_red1",
        today="bold bright_yellow on red3",
        holiday="bold black on yellow3",
    ),
}


def resolve_theme(theme: str | CalendarTheme) -> CalendarTheme:
    if isinstance(theme, CalendarTheme):
        return theme
    if theme not in THEMES:
        raise ValueError(f"Unknown theme '{theme}'. Available: {list(THEMES)}")
    return THEMES[theme]
