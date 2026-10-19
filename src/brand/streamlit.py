"""Shared Streamlit chrome — byline, freshness strip, lede, footer, charts.

Free of project knowledge by contract: no SQL, no table names, no domain
vocabulary. Each app computes its own facts and passes them in as
:class:`StripItem` values; this module only decides how they look.

No CSS injection. Colour comes from the generated ``.streamlit/config.toml``
theme and from Streamlit's native ``:color[text]{foreground="#hex"}`` markdown.
Needs the ``streamlit`` extra (``brand[streamlit]``).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Literal

import streamlit as st

import brand.altair  # noqa: F401 — registers and enables the chart theme
from brand.tokens import (
    AUTHOR,
    AUTHOR_ROLE,
    INK,
    INK_MUTED,
    LINKEDIN_URL,
    PORTFOLIO_URL,
    RUST_500,
    RUST_700,
    RUST_900,
    TEAL_700,
)

Tone = Literal["neutral", "good", "warn", "bad"]

# Every one clears 4.5:1 on SURFACE. The palette has no red, so "bad" is the
# darkest rust rather than a colour from outside the brand.
_TONE_COLOR: dict[str, str] = {
    "neutral": INK,
    "good": TEAL_700,
    "warn": RUST_700,
    "bad": RUST_900,
}


@dataclass(frozen=True)
class StripItem:
    """One fact in the freshness strip.

    ``label`` is the quiet part, ``value`` the loud part, ``tone`` the verdict,
    ``help`` the caveat. Values arrive formatted: no rounding or locale here.
    """

    label: str
    value: str
    tone: Tone = "neutral"
    help: str | None = None


def mark(text: str, color: str) -> str:
    """Native markdown colour directive — exact brand hex, no CSS injection."""
    return f':color[{text}]{{foreground="{color}"}}'


def strip_markdown(items: Sequence[StripItem]) -> str:
    parts = [
        f"{mark(item.label, INK_MUTED)} **{mark(item.value, _TONE_COLOR[item.tone])}**"
        for item in items
    ]
    return ":small[" + "  ·  ".join(parts) + "]"


def altair_chart(chart: Any, **kwargs: Any) -> None:
    """Render an Altair chart with the brand theme actually applied.

    ``st.altair_chart`` defaults to ``theme="streamlit"``, which overrides the
    registered theme with Streamlit's palette. Routing every chart through here
    means no call site can forget ``theme=None``.
    """
    kwargs.setdefault("width", "stretch")
    st.altair_chart(chart, theme=None, **kwargs)


def lede(answer: str, detail: str = "") -> None:
    """The page's question, answered in one sentence, before any control.

    A bordered container, not a coloured callout: ``st.success`` / ``st.error``
    carry a verdict a page is usually not entitled to make.
    """
    with st.container(border=True):
        st.markdown(f"#### {answer}")
        if detail:
            st.markdown(f":small[{mark(detail, INK_MUTED)}]")
    st.markdown("")


def section(label: str) -> None:
    """Quiet uppercase label that breaks a page into scannable blocks."""
    st.markdown(f":small[**{mark(label.upper(), INK_MUTED)}**]")


def render_header(
    title: str | None = None,
    subtitle: str = "",
    facts: Sequence[StripItem] = (),
    *,
    explain_facts: bool = False,
) -> None:
    """Byline, title, one line on what the page answers, then data freshness.

    The byline comes first on purpose: these apps are portfolio pieces, so who
    built it and the way back are part of the product. ``explain_facts`` turns
    the tooltips into an expander — worth it once, on the landing page.
    """
    st.markdown(
        f":small[**{AUTHOR}** · {mark(AUTHOR_ROLE, INK_MUTED)} · [← portfolio]({PORTFOLIO_URL})]"
    )
    if title:
        st.title(title, anchor=False)
    if subtitle:
        st.markdown(mark(subtitle, INK_MUTED))
    if facts:
        st.markdown(strip_markdown(facts))
        tips = [f"{i.label}: {i.help}" for i in facts if i.help]
        if explain_facts and tips:
            with st.expander("What these numbers mean", expanded=False):
                for tip in tips:
                    st.markdown(f":small[{mark('•', RUST_500)} {tip}]")
    st.markdown("")


def render_footer(*, repo_url: str | None = None) -> None:
    """Who built it and where to read the code. The name links to the portfolio."""
    st.divider()
    parts = [
        f"Built by [{AUTHOR}]({PORTFOLIO_URL})",
        mark(AUTHOR_ROLE, INK_MUTED),
        f"[LinkedIn]({LINKEDIN_URL})",
    ]
    if repo_url:
        parts.append(f"[Source]({repo_url})")
    st.markdown(":small[" + " · ".join(parts) + "]")
