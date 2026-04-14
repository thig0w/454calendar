import pytest

from retailcalendar import THEMES, CalendarTheme
from retailcalendar.themes import resolve_theme

EXPECTED_THEMES = {
    "default",
    "ocean",
    "sunset",
    "monokai",
    "retro",
    "matrix",
    "sakura",
    "ice",
    "volcano",
}


# ---------------------------------------------------------------------------
# THEMES dict integrity
# ---------------------------------------------------------------------------


def test_all_themes_present():
    assert set(THEMES.keys()) == EXPECTED_THEMES


def test_all_theme_fields_are_non_empty_strings():
    # sourcery skip: no-loop-in-tests
    fields = CalendarTheme.__dataclass_fields__.keys()
    for name, theme in THEMES.items():
        for field in fields:
            value = getattr(theme, field)
            assert isinstance(value, str) and value.strip(), (
                f"Theme '{name}' has empty or non-string field '{field}'"
            )


# ---------------------------------------------------------------------------
# resolve_theme
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", sorted(EXPECTED_THEMES))
def test_resolve_theme_by_name(name):
    theme = resolve_theme(name)
    assert isinstance(theme, CalendarTheme)
    assert theme is THEMES[name]


def test_resolve_theme_passes_through_instance():
    custom = CalendarTheme(
        year_title="bold blue",
        month_name="cyan",
        day_header="grey50",
        week_number="bright_green",
        today="bold white on dark_blue",
        holiday="bold white on dark_green",
    )
    assert resolve_theme(custom) is custom


def test_resolve_theme_unknown_raises():
    with pytest.raises(ValueError, match="Unknown theme"):
        resolve_theme("nonexistent")
