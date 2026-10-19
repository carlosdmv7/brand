# Brand guidelines

**Warm paper, petrol ink.** One look across the portfolio site and every app,
so they read as one body of work.

The values live in [`src/brand/tokens.py`](src/brand/tokens.py). This page
explains how to use them. If the two disagree, the code wins and this page has
a bug.

## Palette

| Token | Hex | Role |
|---|---|---|
| `sand-100` | `#F6E2B3` | Warm fill: warnings, badges, the light end of ramps. **Never text.** |
| `amber-500` | `#E7A84E` | Fills, icons, chart series. **Never text** (2.0:1). |
| `rust-500` | `#D96C2C` | The accent: icons, rules, dots, chart lines. **Never text, never under a white label** (3.4:1). |
| `teal-500` | `#3E8E7E` | Identity colour, graphical: icons, area fills. |
| `petrol-900` | `#274C56` | The ink, and the only dark surface (header/footer bands). |

### Derived (required, do not substitute)

| Token | Hex | Use |
|---|---|---|
| `surface` | `#FDFAF4` | Page background |
| `surface-2` | `#F5EFE3` | Cards, sidebar, wells |
| `border` | `#E4D9C4` | Hairlines, grid lines |
| `ink` | `#274C56` | Body text |
| `ink-muted` | `#5C7480` | Secondary text, **on `surface` only** |
| `ink-muted-2` | `#4E636D` | Secondary text on `surface-2`, tints and sand |
| `rust-700` | `#A8501F` | Links, rust text, primary button fill (white label), focus ring |
| `rust-900` | `#6E2F10` | Alarm text. The palette has no red. |
| `teal-700` | `#2E6B5E` | Success text, secondary button fill (white label) |
| `rust-050` / `teal-050` | `#FBEADF` / `#E4F0EC` | Tint backgrounds |
| `teal-200` / `rust-300` / `sand-400` | `#7FB3A4` / `#DF844E` / `#C4BE9D` | On the petrol band only |

## Rules

1. **Never hardcode a hex.** Import from `brand.tokens` (Python) or use the
   CSS custom property. A colour that is not a token is a design error.
2. **Text needs 4.5:1, graphics need 3:1.** `uv run brand contrast` measures
   every pair the brand produces. CI fails on a regression.
3. **The 500s are graphical.** When a colour carries words, use its 700. A
   white label sits only on `rust-700`, `teal-700` or `petrol-900`.
4. **Rust is an accent, not a field.** One or two rust elements per viewport.
   Teal and petrol carry the identity.
5. **Light only.** There is no dark theme. Streamlit's dark variant is pinned
   to the light tokens.
6. **No CSS injection in Streamlit.** Colour comes only from the generated
   `config.toml` theme and from native `:color[...]{foreground=...}` markdown,
   so an upgrade can never silently break the look.
7. **No green→red.** Use the teal↔rust diverging scale for good/bad. It
   survives the common forms of colour blindness.

## Charts

| Scale | Colours | For |
|---|---|---|
| Categorical | petrol · rust · teal · amber · ink-muted | Up to **5** series. A sixth means aggregate. |
| Diverging | teal-700 → teal-200 → sand → amber → rust | Anything with a midpoint. Teal = below/good. |
| Sequential | sand → amber → rust-500 → rust-700 → rust-900 | Counts, density, heat |

Figures (continuous axes, value labels) are set in mono and names on
discrete axes in the body font, both in `ink-muted`. Grid lines are
dashed `border` hairlines, with no vertical grid. Titles are in Archivo 700,
left-aligned.

## Type

| Role | Family | Weight |
|---|---|---|
| Display / headings | Archivo | 700 (600 for small headings) |
| Body | Public Sans | 400 |
| Figures, axes, code | IBM Plex Mono | 400–500 |

## Rhythm

Radius `12px` (`8px` small) · max width `1120px`.

## Every app carries

- **A byline above the title:** *Carlos De Manuel · Data & Analytics Engineer ·
  ← portfolio*.
- **A freshness strip.** Every number on it is read live, never hardcoded.
- **A footer:** *Built by · role · LinkedIn · Source*.

`brand.streamlit.render_header()` and `render_footer()` render all three.
