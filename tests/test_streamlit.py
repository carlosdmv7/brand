import altair as alt
from streamlit.testing.v1 import AppTest


def _app():
    # AppTest runs this function's source alone, so its imports live inside it.
    import altair as alt

    from brand.streamlit import StripItem, altair_chart, lede, render_footer, render_header, section

    render_header(
        "Title",
        "What this page answers",
        [StripItem("rows", "1,234", "good", help="loaded today")],
        explain_facts=True,
    )
    lede("The answer.", "The detail.")
    section("charts")
    altair_chart(alt.Chart(alt.Data(values=[{"x": 1}])).mark_bar().encode(x="x:Q"))
    render_footer(repo_url="https://github.com/carlosdmv7/brand")


def test_chrome_renders_without_errors():
    at = AppTest.from_function(_app).run()

    assert not at.exception
    assert at.title[0].value == "Title"
    markdown = " ".join(m.value for m in at.markdown)
    assert "Carlos De Manuel" in markdown
    assert '1,234]{foreground="#2E6B5E"}' in markdown
    assert "[Source](https://github.com/carlosdmv7/brand)" in markdown


def test_importing_the_layer_enables_the_brand_theme():
    import brand.streamlit  # noqa: F401

    assert alt.theme.active == "brand"
