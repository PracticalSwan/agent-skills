#!/usr/bin/env python3
"""Validate local Markdown links."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def check(path: Path) -> list[str]:
    findings: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for match in LINK_RE.finditer(text):
        target = match.group(1).strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        clean_target = target.split("#", 1)[0]
        if not clean_target:
            continue
        candidate = (path.parent / clean_target).resolve()
        if not candidate.exists():
            findings.append(f"{path}: missing target {target}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Markdown files or directories")
    args = parser.parse_args()

    findings: list[str] = []
    for raw in args.paths:
        path = Path(raw)
        files = [path] if path.is_file() else sorted(path.rglob("*.md"))
        for file_path in files:
            findings.extend(check(file_path))

    if findings:
        print("\n".join(findings))
        return 1

    print("All checked Markdown links resolved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
