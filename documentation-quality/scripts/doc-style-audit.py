#!/usr/bin/env python3
"""Audit Markdown files for a few high-signal style issues."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

HEADING_RE = re.compile(r"^(#+)\s+")


def audit(path: Path) -> list[str]:
    findings: list[str] = []
    previous_level = 0
    for index, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        if "\t" in line:
            findings.append(f"{path}:{index}: contains tab characters")
        if line.rstrip() != line:
            findings.append(f"{path}:{index}: trailing whitespace")
        if len(line) > 140:
            findings.append(f"{path}:{index}: line exceeds 140 characters")
        match = HEADING_RE.match(line)
        if match:
            level = len(match.group(1))
            if previous_level and level > previous_level + 1:
                findings.append(f"{path}:{index}: heading jumps from H{previous_level} to H{level}")
            previous_level = level
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
            findings.extend(audit(file_path))

    if findings:
        print("\n".join(findings))
        return 1

    print("No style issues found by the lightweight audit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
