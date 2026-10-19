"""Render the tokens into the formats each repo consumes.

Each renderer returns the *body* of a managed block. ``brand.sync`` puts it
between markers inside the target file, so the rest of that file (server
settings, site-specific CSS) stays owned by the repo it lives in.
"""

from __future__ import annotations

from brand import tokens as t
from brand.contrast import ratio


def _toml_list(values: tuple[str, ...] | list[str]) -> str:
    return "[" + ", ".join(f'"{v}"' for v in values) + "]"


def _font(family: str, fallback: str) -> str:
    """Streamlit's native ``"<family>:<css url>, <fallback>"`` form — no @font-face injection."""
    return f"{family}:{t.FONT_URLS[family]}, {fallback}"


def css() -> str:
    """The portfolio's ``:root`` token block."""
    lines = [":root {"]
    width = max(len(name) for name in t.COLORS) + 3
    for name, value in t.COLORS.items():
        lines.append(f"    {f'--{name}:':<{width}} {value};")
    lines.append("")
    for name, stack in t.CSS_FONT_STACKS.items():
        lines.append(f"    --{name}: {stack};")
    lines.append("")
    lines.append(f"    --radius:    {t.RADIUS_PX}px;")
    lines.append(f"    --radius-sm: {t.RADIUS_SM_PX}px;")
    lines.append(f"    --maxw:      {t.MAX_WIDTH_PX}px;")
    lines.append("}")
    return "\n".join(lines)


def streamlit(font_prefix: list[str] | None = None) -> str:
    """The ``[theme]``, ``[theme.sidebar]`` and ``[theme.dark]`` tables.

    ``font_prefix`` puts extra families first in the body font list — e.g. a
    flags-only font for Windows, declared by the app under its own
    ``[[theme.fontFaces]]`` after the managed block.
    """
    body_font = ", ".join([*(font_prefix or []), _font(t.FONT_BODY, "sans-serif")])
    r = ratio  # the comments below quote live measurements, never stale numbers
    return f"""\
# No CSS injection anywhere: everything here is a native theme key, so a
# Streamlit upgrade can change the DOM without silently breaking the look.
[theme]
base = "light"

# Same families and Google Fonts URLs as the portfolio.
font = "{body_font}"
headingFont = "{_font(t.FONT_DISPLAY, "sans-serif")}"
codeFont = "{_font(t.FONT_MONO, "monospace")}"
baseFontWeight = 400

# Read off the portfolio's stylesheet, with h1 at the bottom of its display
# range: an app title sits above dense controls, not alone in a viewport.
# Not reachable natively: the portfolio's negative letter-spacing.
headingFontSizes = ["2.25rem", "1.6rem", "1.3rem", "1.1rem", "1rem", "0.875rem"]
headingFontWeights = [700, 700, 700, 600, 600, 600]

# Streamlit's default 2.25rem metric reads as a scoreboard on a page of six.
metricValueFontSize = "1.75rem"
metricValueFontWeight = 700

backgroundColor = "{t.SURFACE}"           # surface
secondaryBackgroundColor = "{t.SURFACE_2}"  # surface-2
textColor = "{t.INK}"                 # ink
borderColor = "{t.BORDER}"               # border
linkColor = "{t.RUST_700}"                 # rust-700

# rust-700, NOT rust-500: Streamlit puts white labels on primaryColor fills,
# and white on rust-500 is {r(t.WHITE, t.RUST_500):.2f}:1 (fails AA). On rust-700 it is {r(t.WHITE, t.RUST_700):.2f}:1.
primaryColor = "{t.RUST_700}"

baseRadius = "{t.RADIUS_PX / 16}rem"
buttonRadius = "{t.RADIUS_SM_PX / 16}rem"
showWidgetBorder = true
showSidebarBorder = true
linkUnderline = false

# Streamlit's alert colours are red-amber-blue-green — the green→red scale
# this brand forbids. Remapped onto tokens; every text/background pair ≥ 4.5:1.
# st.error → rust tint. The palette has no red; rust-900 is its alarm ink.
redColor = "{t.RUST_700}"
redBackgroundColor = "{t.RUST_050}"
redTextColor = "{t.RUST_900}"            # {r(t.RUST_900, t.RUST_050):.2f}:1
# st.warning → sand fill, ink on it. Sand is never text.
orangeColor = "{t.AMBER_500}"
orangeBackgroundColor = "{t.SAND_100}"
orangeTextColor = "{t.INK}"           # {r(t.INK, t.SAND_100):.2f}:1
yellowColor = "{t.AMBER_500}"
yellowBackgroundColor = "{t.SAND_100}"
yellowTextColor = "{t.INK}"
# st.info → a quiet neutral well, deliberately calmer than a verdict.
blueColor = "{t.PETROL_900}"
blueBackgroundColor = "{t.SURFACE_2}"
blueTextColor = "{t.INK}"             # {r(t.INK, t.SURFACE_2):.2f}:1
violetColor = "{t.PETROL_900}"
violetBackgroundColor = "{t.SURFACE_2}"
violetTextColor = "{t.INK}"
# st.success → teal tint.
greenColor = "{t.TEAL_700}"
greenBackgroundColor = "{t.TEAL_050}"
greenTextColor = "{t.TEAL_700}"          # {r(t.TEAL_700, t.TEAL_050):.2f}:1
grayColor = "{t.INK_MUTED_2}"
grayBackgroundColor = "{t.SURFACE_2}"
grayTextColor = "{t.INK_MUTED_2}"           # {r(t.INK_MUTED_2, t.SURFACE_2):.2f}:1

# These reach Altair, Vega-Lite and Plotly alike, so a chart built without
# brand.altair still lands on-brand instead of on Streamlit blue.
chartCategoricalColors = {_toml_list(t.CATEGORICAL)}
chartDivergingColors = {_toml_list(t.DIVERGING)}
chartSequentialColors = {_toml_list(t.SEQUENTIAL)}

dataframeHeaderBackgroundColor = "{t.SURFACE_2}"
dataframeBorderColor = "{t.BORDER}"
codeBackgroundColor = "{t.SURFACE_2}"
codeTextColor = "{t.RUST_900}"

[theme.sidebar]
backgroundColor = "{t.SURFACE_2}"
secondaryBackgroundColor = "{t.SURFACE}"
borderColor = "{t.BORDER}"
textColor = "{t.INK}"
linkColor = "{t.RUST_700}"
primaryColor = "{t.RUST_700}"
codeBackgroundColor = "{t.SURFACE}"

# The brand is light-only. Pinning the dark variant to the same tokens renders
# warm paper whatever the visitor's system or Streamlit Cloud setting.
[theme.dark]
backgroundColor = "{t.SURFACE}"
secondaryBackgroundColor = "{t.SURFACE_2}"
textColor = "{t.INK}"
borderColor = "{t.BORDER}"
linkColor = "{t.RUST_700}"
primaryColor = "{t.RUST_700}"
dataframeHeaderBackgroundColor = "{t.SURFACE_2}"
dataframeBorderColor = "{t.BORDER}"
codeBackgroundColor = "{t.SURFACE_2}"
codeTextColor = "{t.RUST_900}\""""
