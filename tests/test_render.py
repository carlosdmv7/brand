import re
import tomllib

from brand import render, tokens


def test_streamlit_block_is_valid_toml_with_the_three_tables():
    theme = tomllib.loads(render.streamlit())["theme"]
    assert theme["primaryColor"] == tokens.RUST_700
    assert theme["backgroundColor"] == tokens.SURFACE
    assert theme["chartCategoricalColors"] == list(tokens.CATEGORICAL)
    assert theme["sidebar"]["backgroundColor"] == tokens.SURFACE_2
    assert theme["dark"]["backgroundColor"] == tokens.SURFACE


def test_primary_colour_carries_a_legible_white_label():
    theme = tomllib.loads(render.streamlit())["theme"]
    assert theme["primaryColor"] in tokens.WHITE_LABEL_FILLS


def test_font_prefix_goes_first():
    theme = tomllib.loads(render.streamlit(["Twemoji Country Flags"]))["theme"]
    assert theme["font"].startswith("Twemoji Country Flags, Public Sans:https://")


def test_css_declares_every_colour():
    declared = dict(re.findall(r"--([\w-]+):\s*([^;]+);", render.css()))
    for name, value in tokens.COLORS.items():
        assert declared[name] == value
    assert declared["radius"] == f"{tokens.RADIUS_PX}px"
