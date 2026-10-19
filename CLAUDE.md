# Brand

The shared design system for every repo of the portfolio. `src/brand/tokens.py`
is the single source of truth for colours, fonts, chart scales and identity.
`brand sync` renders them into managed blocks in consumers' files
(`.streamlit/config.toml`, the portfolio's `styles.css`). `brand.altair` and
`brand.streamlit` are the chart theme and app chrome. The rules are in `BRAND.md`.

- A token change must keep `make check` green: the contrast tests are the rule
  set, so never loosen a pair to make a colour pass.
- Keep `tokens`, `contrast`, `render`, `sync` and `cli` standard-library only.

## Commands

- `make install` — sync deps with uv
- `make check` — lint + format check + tests (the CI gate). Run it before saying a change is done.
- `make format` — auto-fix
- `make contrast` — print the WCAG table for every colour pair

## Conventions

- Python via `uv run`, never a bare `python` / `pip`. Add deps with `uv add`.
- Ruff is the only linter and formatter (config in `pyproject.toml`).
- Code in `src/brand/`, tests in `tests/` mirroring it.
- Conventional commits; branch from fresh `main`; PR + green CI to merge.
- Decisions with trade-offs get an ADR in `docs/adr/`.
- Verify changes by running them, not only by reading code or unit tests.
