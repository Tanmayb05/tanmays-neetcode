#!/usr/bin/env python3
"""Validate repository layout and filename conventions."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content" / "problems"
OUTPUT_DIR = ROOT / "site" / "problems"

NAME_RE = re.compile(r"^lc-\d+-[a-z0-9]+(?:-[a-z0-9]+)*$")


def fail(msg: str) -> None:
    raise SystemExit(f"[FAIL] {msg}")


def validate_required_dirs() -> None:
    required = [
        CONTENT_DIR,
        OUTPUT_DIR,
        ROOT / "templates",
        ROOT / "tools",
        ROOT / "docs",
        ROOT / "examples" / "context",
    ]
    for d in required:
        if not d.exists() or not d.is_dir():
            fail(f"Missing required directory: {d.relative_to(ROOT)}")


def validate_names() -> tuple[set[str], set[str]]:
    md_files = sorted(CONTENT_DIR.glob("*.md"))
    html_files = sorted(OUTPUT_DIR.glob("*.html"))

    if not md_files:
        fail("No markdown files found in content/problems")

    md_stems = set()
    for f in md_files:
        if not NAME_RE.match(f.stem):
            fail(f"Invalid markdown filename: {f.name}")
        md_stems.add(f.stem)

    html_stems = set()
    for f in html_files:
        if not NAME_RE.match(f.stem):
            # allow non-problem sample outputs during transition
            if f.stem.startswith("sample-"):
                continue
            fail(f"Invalid HTML filename: {f.name}")
        html_stems.add(f.stem)

    return md_stems, html_stems


def validate_matching_outputs(md_stems: set[str], html_stems: set[str]) -> None:
    missing = sorted(md_stems - html_stems)
    if missing:
        fail("Missing generated HTML for: " + ", ".join(missing))


def main() -> None:
    validate_required_dirs()
    md_stems, html_stems = validate_names()
    validate_matching_outputs(md_stems, html_stems)
    print("[OK] Structure and naming checks passed.")


if __name__ == "__main__":
    main()
