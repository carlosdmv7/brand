import re

from brand import tokens

HEX = re.compile(r"^#[0-9A-F]{6}$")


def test_every_colour_is_uppercase_six_digit_hex():
    for name, value in tokens.COLORS.items():
        assert HEX.match(value), f"{name}: {value}"


def test_the_five_brand_colours_never_change_silently():
    assert [
        tokens.SAND_100,
        tokens.AMBER_500,
        tokens.RUST_500,
        tokens.TEAL_500,
        tokens.PETROL_900,
    ] == [
        "#F6E2B3",
        "#E7A84E",
        "#D96C2C",
        "#3E8E7E",
        "#274C56",
    ]


def test_scales_only_use_tokens():
    known = set(tokens.COLORS.values())
    for scale in (tokens.CATEGORICAL, tokens.DIVERGING, tokens.SEQUENTIAL):
        assert set(scale) <= known


def test_categorical_is_capped_at_five():
    assert len(tokens.CATEGORICAL) == 5


def test_every_font_has_a_url():
    for family in (tokens.FONT_DISPLAY, tokens.FONT_BODY, tokens.FONT_MONO):
        assert tokens.FONT_URLS[family].startswith("https://fonts.googleapis.com/")
