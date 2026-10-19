"""Altair theme built from the tokens — the charts' half of the brand.

Importing this module registers and enables the theme, so every chart in the
process inherits the brand without per-chart styling at the call site. An app
that needs an extra family in its charts (a flags-only font, say) calls
:func:`register` again with ``font_prefix``.
Needs the ``streamlit`` extra (``brand[streamlit]``), which brings Altair.
"""

from __future__ import annotations

from collections.abc import Sequence

import altair as alt

from brand.tokens import (
    BORDER,
    CATEGORICAL,
    DIVERGING,
    FONT_BODY,
    FONT_DISPLAY,
    FONT_MONO,
    INK,
    INK_MUTED,
    PETROL_900,
    RUST_500,
    SEQUENTIAL,
    SURFACE,
    TEAL_500,
)

THEME_NAME = "brand"

# Vega-Lite can name these families because the page around the SVG loads them
# (Streamlit through `theme.font`, the portfolio through its <link>).
FONT_STACK = f"{FONT_BODY}, sans-serif"
MONO_STACK = f"{FONT_MONO}, ui-monospace, monospace"
DISPLAY_STACK = f"{FONT_DISPLAY}, sans-serif"


def config(font_prefix: Sequence[str] = ()) -> alt.theme.ThemeConfig:
    """The theme as a Vega-Lite config, with ``font_prefix`` first in every font stack."""
    prefix = "".join(f"{family}, " for family in font_prefix)
    body, mono, display = (prefix + s for s in (FONT_STACK, MONO_STACK, DISPLAY_STACK))
    return {
        "config": {
            "background": SURFACE,
            "font": body,
            "view": {"stroke": "transparent", "continuousHeight": 320},
            "title": {
                "color": INK,
                "font": display,
                "fontSize": 15,
                "fontWeight": 700,
                "anchor": "start",
                "offset": 12,
                "subtitleColor": INK_MUTED,
                "subtitleFont": body,
                "subtitleFontSize": 12,
            },
            # Axis furniture is INK_MUTED — readable but recessive, so the marks
            # carry the colour. Labels are mono: they are almost always figures.
            "axis": {
                # Mono labels are wide; drop every other one on collision.
                "labelOverlap": True,
                "labelColor": INK_MUTED,
                "labelFont": mono,
                "labelFontSize": 11,
                "titleColor": INK_MUTED,
                "titleFontSize": 11,
                "titleFontWeight": 600,
                "domainColor": BORDER,
                "tickColor": BORDER,
                "gridColor": BORDER,
                "gridDash": [2, 2],
            },
            "axisX": {"grid": False},
            "axisY": {"domain": False, "ticks": False, "labelPadding": 6},
            "legend": {
                "labelColor": INK,
                "labelFontSize": 11,
                "titleColor": INK_MUTED,
                "titleFontSize": 11,
                "titleFontWeight": 600,
                "symbolType": "circle",
                "orient": "top",
                "direction": "horizontal",
                "titlePadding": 6,
                "offset": 8,
            },
            "range": {
                "category": list(CATEGORICAL),
                "diverging": list(DIVERGING),
                "heatmap": list(SEQUENTIAL),
                "ramp": list(SEQUENTIAL),
                "ordinal": list(SEQUENTIAL),
            },
            "bar": {"fill": PETROL_900, "cornerRadiusEnd": 3},
            "line": {"stroke": RUST_500, "strokeWidth": 2},
            "point": {"fill": RUST_500, "size": 60, "strokeWidth": 0, "opacity": 0.8},
            "area": {"fill": TEAL_500, "opacity": 0.7},
            "rule": {"stroke": INK_MUTED},
            "text": {"color": INK, "font": mono, "fontSize": 11},
            "header": {"labelColor": INK, "titleColor": INK_MUTED},
        }
    }


def register(font_prefix: Sequence[str] = ()) -> None:
    """Register the theme under :data:`THEME_NAME` and enable it, replacing any earlier one."""
    alt.theme.register(THEME_NAME, enable=True)(lambda: config(font_prefix))


register()
