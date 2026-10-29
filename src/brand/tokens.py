"""Brand tokens — the single source of truth for every repo.

"Warm paper, petrol ink." Every colour, font and radius the portfolio and the
apps use is defined here once. Nothing else hardcodes a hex: the portfolio's
``tokens.css`` and each app's ``.streamlit/config.toml`` theme are *generated*
from this module by ``brand sync``, and CI fails when they drift.

This module imports nothing outside the standard library, so it is safe to use
from matplotlib, plotly, a script — anything, not only Streamlit.
"""

from __future__ import annotations

# ══════════════════════════════════════════════════════════════════════════════
# Brand — the five colours
# ══════════════════════════════════════════════════════════════════════════════
SAND_100 = "#F6E2B3"
AMBER_500 = "#E7A84E"
RUST_500 = "#D96C2C"
TEAL_500 = "#3E8E7E"
PETROL_900 = "#274C56"

# ══════════════════════════════════════════════════════════════════════════════
# Derived — required, do not substitute
# ══════════════════════════════════════════════════════════════════════════════
SURFACE = "#FDFAF4"  # page background
SURFACE_2 = "#F5EFE3"  # cards, sidebar, wells
BORDER = "#E4D9C4"  # hairlines
INK = "#274C56"  # body text
INK_MUTED = "#5C7480"  # secondary text — on SURFACE only (4.6:1)
RUST_700 = "#A8501F"  # links, primary button fill (white label)
TEAL_700 = "#2E6B5E"  # success, secondary button fill (white label)
RUST_050 = "#FBEADF"  # tint background
TEAL_050 = "#E4F0EC"  # tint background

# Added to fix measured contrast violations. INK_MUTED is 4.3:1 on SURFACE_2
# and on the tints, which fails AA for small text, so those surfaces get a
# darker muted ink. The light-on-petrol tokens exist because RUST_500 (2.7:1)
# and TEAL_500 (2.4:1) are too dark to read on the petrol band.
INK_MUTED_2 = "#4E636D"  # secondary text on SURFACE_2 / tints / sand
RUST_900 = "#6E2F10"  # the only "alarm" text — the palette has no red
TEAL_200 = "#7FB3A4"  # graphical, on PETROL_900 only (3.9:1)
RUST_300 = "#DF844E"  # graphical, on PETROL_900 only (3.4:1)
SAND_400 = "#C4BE9D"  # muted label text on PETROL_900 (5.0:1)
WHITE = "#FFFFFF"  # labels on RUST_700 / TEAL_700 / PETROL_900 fills only

# Money that changed sign or value: a gain and a loss (ADR 0002). Text on the
# light surfaces, always with a sign and an arrow, never alone. Teal and rust
# keep meaning "money in" and "money out"; these mean "better" and "worse".
GAIN_700 = "#267A3E"  # gains, figures that improved
LOSS_700 = "#B42318"  # losses, figures that got worse

#: Every colour by its CSS name. Renderers iterate this, in this order.
COLORS: dict[str, str] = {
    "sand-100": SAND_100,
    "amber-500": AMBER_500,
    "rust-500": RUST_500,
    "teal-500": TEAL_500,
    "petrol-900": PETROL_900,
    "surface": SURFACE,
    "surface-2": SURFACE_2,
    "border": BORDER,
    "ink": INK,
    "ink-muted": INK_MUTED,
    "rust-700": RUST_700,
    "teal-700": TEAL_700,
    "rust-050": RUST_050,
    "teal-050": TEAL_050,
    "ink-muted-2": INK_MUTED_2,
    "rust-900": RUST_900,
    "teal-200": TEAL_200,
    "rust-300": RUST_300,
    "sand-400": SAND_400,
    "white": WHITE,
    "gain-700": GAIN_700,
    "loss-700": LOSS_700,
}

# ══════════════════════════════════════════════════════════════════════════════
# Usage rules worth encoding rather than remembering (see BRAND.md)
# ══════════════════════════════════════════════════════════════════════════════
#: Colours that may carry small text on SURFACE. AMBER_500 (2.1:1), SAND_100
#: and RUST_500 (3.4:1) are fills, icons and charts only — never text.
TEXT_SAFE_ON_SURFACE: tuple[str, ...] = (
    INK,
    INK_MUTED,
    INK_MUTED_2,
    RUST_700,
    TEAL_700,
    RUST_900,
    GAIN_700,
    LOSS_700,
)

#: White labels are only legible on these fills — never on the 500s.
WHITE_LABEL_FILLS: tuple[str, ...] = (RUST_700, TEAL_700, PETROL_900)

LINK = RUST_700
SUCCESS = TEAL_700
ACCENT = RUST_500  # one or two elements per viewport; teal and petrol carry the identity

# ══════════════════════════════════════════════════════════════════════════════
# Chart scales
# ══════════════════════════════════════════════════════════════════════════════
#: Max 5 series. A sixth colour is a design error: aggregate instead.
CATEGORICAL: tuple[str, ...] = (PETROL_900, RUST_500, TEAL_500, AMBER_500, INK_MUTED)

#: Anything with a meaningful midpoint. Teal = below/good, rust = above/bad.
#: A blue–orange axis survives deuteranopia and protanopia: never green→red.
DIVERGING: tuple[str, ...] = (TEAL_700, TEAL_200, SAND_100, AMBER_500, RUST_500)

#: Counts, density, trend heat.
SEQUENTIAL: tuple[str, ...] = (SAND_100, AMBER_500, RUST_500, RUST_700, RUST_900)

# ══════════════════════════════════════════════════════════════════════════════
# Type
# ══════════════════════════════════════════════════════════════════════════════
FONT_DISPLAY = "Archivo"  # headings, 700
FONT_BODY = "Public Sans"  # body, 400
FONT_MONO = "IBM Plex Mono"  # figures, axis labels, code

#: Google Fonts CSS for each family — the same URLs the portfolio loads.
FONT_URLS: dict[str, str] = {
    FONT_DISPLAY: "https://fonts.googleapis.com/css2?family=Archivo:wght@400..700&display=swap",
    FONT_BODY: "https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600&display=swap",
    FONT_MONO: "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&display=swap",
}

CSS_FONT_STACKS: dict[str, str] = {
    "font-display": f"'{FONT_DISPLAY}', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    "font-body": f"'{FONT_BODY}', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    "font-mono": f"'{FONT_MONO}', ui-monospace, 'SF Mono', 'Cascadia Code', monospace",
}

# ══════════════════════════════════════════════════════════════════════════════
# Rhythm
# ══════════════════════════════════════════════════════════════════════════════
RADIUS_PX = 12
RADIUS_SM_PX = 8
MAX_WIDTH_PX = 1120

# ══════════════════════════════════════════════════════════════════════════════
# Identity — the byline every app carries
# ══════════════════════════════════════════════════════════════════════════════
AUTHOR = "Carlos De Manuel"
AUTHOR_ROLE = "Data & Analytics Engineer"
PORTFOLIO_URL = "https://carlosdmv7.github.io/personal-portfolio/"
LINKEDIN_URL = "https://www.linkedin.com/in/carlos-de-manuel"
