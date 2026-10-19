# 0001 — Ship the brand as one package that generates each repo's theme

- **Status:** accepted
- **Date:** 2026-10-18

## Context

The palette was copied by hand into four places: the portfolio's `styles.css`,
two `.streamlit/config.toml` files and two `theme.py` modules. With only two
apps it had already drifted:

- The two `theme.py` files had different APIs, although one of them claimed
  to be byte-identical across apps.
- job-market-intelligence filled `primaryColor` with `rust-500`, so its white
  button labels were 3.42:1 and failed AA, a rule the portfolio states.
- Its config was missing about 60 theme keys that housing-radar had: the
  semantic colours, the fonts, the dark-mode pin and the chart scales.

The written rules existed only as comments in CSS and Python.

## Decision

One repo, `brand`, holds the tokens (`tokens.py`), the written rules
(`BRAND.md`), the contrast test, and generators. `brand sync` writes a managed
block between markers into each consumer's file (`config.toml` `[theme]`, the
portfolio's `:root`). `brand sync --check` runs in each consumer's CI and fails
on drift. The Altair theme and Streamlit chrome ship as the `streamlit` extra.

## Alternatives considered

- **Keep copying, add a doc.** It is cheap, but it is what produced the drift.
  A doc does not fail a build.
- **Generate whole files instead of managed blocks.** Each repo owns
  non-brand settings in the same file (`[server]`, an app's own fonts, the
  portfolio's shadows). Markers keep that ownership explicit.
- **Make `tokens.toml` the source and read it at runtime.** Python constants
  give autocomplete and static checking at every call site, and the TOML/CSS
  outputs are generated from them anyway.
- **Live inside `personal-portfolio`.** That repo is a static site with no
  build step. Adding a Python package there would mix the two concerns.

## Consequences

- A colour change is one edit, one tag, then `brand sync` in each consumer.
  It is not a find-and-replace across repos.
- Every consumer depends on a git URL. Streamlit Community Cloud installs it
  from `requirements.txt` or `pyproject.toml` like any other dependency, but
  the repo must stay public.
- Bumping the brand is a deliberate per-repo upgrade, because consumers pin a
  tag. A repo can lag, but `--check` makes the lag visible.
