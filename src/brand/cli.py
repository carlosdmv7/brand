"""``brand`` command line.

    brand sync streamlit [.streamlit/config.toml] [--font-prefix FAMILY] [--check]
    brand sync css [styles.css] [--check]
    brand contrast

Runs without installing anything into the target repo, which is what lets the
static portfolio use it too:

    uvx --from git+https://github.com/carlosdmv7/brand brand sync css --check
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from brand import contrast, render
from brand.sync import CSS, TOML, SyncError, sync


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="brand", description=__doc__.split("\n")[0])
    commands = parser.add_subparsers(dest="command", required=True)

    sync_cmd = commands.add_parser("sync", help="write the brand block into a file")
    targets = sync_cmd.add_subparsers(dest="target", required=True)

    st = targets.add_parser("streamlit", help="the [theme] tables of .streamlit/config.toml")
    st.add_argument("path", nargs="?", type=Path, default=Path(".streamlit/config.toml"))
    st.add_argument(
        "--font-prefix",
        action="append",
        default=[],
        metavar="FAMILY",
        help="family to put before the body font (repeatable), e.g. a flags-only font",
    )

    css = targets.add_parser("css", help="the :root token block of a stylesheet")
    css.add_argument("path", nargs="?", type=Path, default=Path("styles.css"))

    for target in (st, css):
        target.add_argument(
            "--check", action="store_true", help="exit 1 with a diff instead of writing"
        )

    commands.add_parser("contrast", help="measure every colour pair against WCAG AA")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)

    if args.command == "contrast":
        print(contrast.report())
        return 1 if contrast.violations() else 0

    if args.target == "streamlit":
        body, markers = render.streamlit(args.font_prefix), TOML
    else:
        body, markers = render.css(), CSS

    try:
        diff = sync(args.path, body, markers, check=args.check)
    except SyncError as err:
        print(f"brand: {err}", file=sys.stderr)
        return 2

    if diff is None:
        print(f"{args.path}: up to date")
        return 0
    if args.check:
        sys.stdout.write(diff)
        print(f"\n{args.path}: out of date — run `brand sync {args.target}`", file=sys.stderr)
        return 1
    print(f"{args.path}: updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
