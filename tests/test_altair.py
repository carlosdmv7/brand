import altair as alt

import brand.altair


def test_importing_enables_the_brand_theme():
    assert alt.theme.active == brand.altair.THEME_NAME


def test_font_prefix_goes_first_in_every_stack():
    config = brand.altair.config(["Twemoji Country Flags"])["config"]

    for font in (config["font"], config["title"]["font"], config["axis"]["labelFont"]):
        assert font.startswith("Twemoji Country Flags, ")


def test_register_replaces_the_active_theme():
    try:
        brand.altair.register(["Twemoji Country Flags"])
        spec = alt.Chart(alt.Data(values=[{"x": 1}])).mark_bar().encode(x="x:Q").to_dict()
        assert spec["config"]["axis"]["labelFont"].startswith("Twemoji Country Flags, ")
    finally:
        brand.altair.register()
    spec = alt.Chart(alt.Data(values=[{"x": 1}])).mark_bar().encode(x="x:Q").to_dict()
    assert spec["config"]["axis"]["labelFont"].startswith("IBM Plex Mono")


def test_scales_serialise_as_tuples():
    # Callers slice the token tuples straight into a scale (`SEQUENTIAL[:4]`).
    from brand.tokens import SEQUENTIAL

    chart = (
        alt.Chart(alt.Data(values=[{"x": 1}]))
        .mark_rect()
        .encode(color=alt.Color("x:Q", scale=alt.Scale(range=SEQUENTIAL[:4])))
    )
    assert chart.to_dict()["encoding"]["color"]["scale"]["range"] == list(SEQUENTIAL[:4])


def test_discrete_axes_use_the_body_font_and_continuous_ones_mono():
    config = brand.altair.config()["config"]

    assert config["axis"]["labelFont"].startswith("IBM Plex Mono")
    assert config["axisDiscrete"]["labelFont"].startswith("Public Sans")
