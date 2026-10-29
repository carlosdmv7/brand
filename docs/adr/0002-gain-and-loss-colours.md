# 0002 — A green and a red for gains and losses

- **Status:** accepted
- **Date:** 2026-10-29
- **Amends:** BRAND.md rule 7 ("No green→red").

## Context

The palette has teal and rust and no green or red. Apps used them for two
jobs at once: the kind of money (teal in, rust out) and whether a figure got
better or worse. In a finance app that reads wrong. A rust "Gastos" figure
looks like a loss, a teal return does not look like a gain, and in a dark
theme teal reads as a terminal green rather than as "good".

## Decision

- Two text tokens, `gain-700` (#16794A) and `loss-700` (#B42318), both AA on
  `surface` and `surface-2` (measured in `brand contrast`).
- They colour only a **signed change**: a return, a gain or loss, a
  difference against a reference. They always come with a sign and an arrow
  (▲ ▼ or ↗ ↘), so a reader who cannot tell them apart loses nothing.
- Plain amounts stay in `ink`. Teal and rust keep marking the kind of money
  in charts, dots and icons. The diverging chart scale is unchanged.

## Consequences

- Consumers that show money adopt the rule; the others are unaffected
  because the tokens are additive.
- A dark theme, where a consumer has one, derives lighter variants from
  these two tokens, as it already does for teal and rust.
