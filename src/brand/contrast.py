"""WCAG 2.1 contrast for every colour pair the brand actually produces.

Ported from the portfolio's ``tools/contrast-check.py``. Changing a token here
re-measures every pair in the test suite, so a colour tweak that breaks AA
fails CI instead of shipping.
"""

from __future__ import annotations

from typing import NamedTuple

from brand.tokens import COLORS

TEXT = 4.5  # small text, WCAG AA
GRAPHIC = 3.0  # icons, rules, dots, borders, large text


class Pair(NamedTuple):
    fg: str
    bg: str
    minimum: float
    note: str
    forbidden: bool = False  # documented as never used; measured, never enforced


PAIRS: tuple[Pair, ...] = (
    # ── small text ───────────────────────────────────────────────────────────
    Pair("ink", "surface", TEXT, "body text"),
    Pair("ink", "surface-2", TEXT, "body text on cards"),
    Pair("ink", "sand-100", TEXT, "text on sand fill"),
    Pair("ink", "rust-050", TEXT, "text on rust tint"),
    Pair("ink", "teal-050", TEXT, "text on teal tint"),
    Pair("ink-muted", "surface", TEXT, "secondary text on page bg"),
    Pair("ink-muted-2", "surface", TEXT, "secondary text on page bg"),
    Pair("ink-muted-2", "surface-2", TEXT, "secondary text on cards"),
    Pair("ink-muted-2", "sand-100", TEXT, "secondary text on sand"),
    Pair("ink-muted-2", "rust-050", TEXT, "secondary text on rust tint"),
    Pair("ink-muted-2", "teal-050", TEXT, "secondary text on teal tint"),
    Pair("rust-700", "surface", TEXT, "links"),
    Pair("rust-700", "surface-2", TEXT, "links on cards"),
    Pair("rust-700", "rust-050", TEXT, "link / badge on rust tint"),
    Pair("rust-900", "surface", TEXT, "alarm text"),
    Pair("rust-900", "rust-050", TEXT, "error callout text"),
    Pair("teal-700", "surface", TEXT, "success text"),
    Pair("teal-700", "surface-2", TEXT, "success text on cards"),
    Pair("teal-700", "teal-050", TEXT, "success / badge on teal tint"),
    Pair("white", "rust-700", TEXT, "primary button label"),
    Pair("white", "teal-700", TEXT, "secondary button label"),
    Pair("sand-100", "petrol-900", TEXT, "band text"),
    Pair("white", "petrol-900", TEXT, "band value text"),
    Pair("sand-400", "petrol-900", TEXT, "freshness strip cell labels"),
    # ── graphical ────────────────────────────────────────────────────────────
    Pair("rust-500", "surface", GRAPHIC, "icons / rules on page bg"),
    Pair("teal-500", "surface", GRAPHIC, "icons / fills on page bg"),
    Pair("teal-500", "surface-2", GRAPHIC, "icons on cards"),
    Pair("teal-200", "petrol-900", GRAPHIC, "pass-state dot on band"),
    Pair("amber-500", "petrol-900", GRAPHIC, "stale-state dot on band"),
    Pair("rust-300", "petrol-900", GRAPHIC, "fail-state dot on band"),
    Pair("sand-100", "rust-700", GRAPHIC, "underline on primary button"),
    # ── what the rules forbid, and why ───────────────────────────────────────
    Pair("white", "rust-500", TEXT, "white label on rust-500 — use rust-700", True),
    Pair("teal-500", "petrol-900", GRAPHIC, "never paired", True),
    Pair("rust-500", "petrol-900", GRAPHIC, "too dark on petrol — use rust-300", True),
    Pair("rust-300", "surface", GRAPHIC, "petrol band only", True),
    Pair("sand-400", "surface", GRAPHIC, "petrol band only", True),
    Pair("amber-500", "surface", TEXT, "never text — fills/charts only", True),
    Pair("sand-100", "surface", TEXT, "never text — fills/charts only", True),
)


def _linear(channel: int) -> float:
    c = channel / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _linear(r) + 0.7152 * _linear(g) + 0.0722 * _linear(b)


def ratio(a: str, b: str) -> float:
    """Contrast ratio between two hex colours, 1.0–21.0."""
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def measure(pair: Pair) -> float:
    return ratio(COLORS[pair.fg], COLORS[pair.bg])


def violations() -> list[tuple[Pair, float]]:
    """Every allowed pair below its minimum. Empty means the palette is AA-clean."""
    return [(p, r) for p in PAIRS if not p.forbidden and (r := measure(p)) < p.minimum]


def report() -> str:
    lines = [f"{'foreground':<12} {'background':<11} {'ratio':>6} {'min':>4}  {'':<4} note"]
    lines.append("-" * 78)
    for p in PAIRS:
        r = measure(p)
        flag = "n/a " if p.forbidden else ("PASS" if r >= p.minimum else "FAIL")
        lines.append(f"{p.fg:<12} {p.bg:<11} {r:>6.2f} {p.minimum:>4.1f}  {flag} {p.note}")
    lines.append("-" * 78)
    lines.append(f"{len(violations())} violation(s)")
    return "\n".join(lines)
