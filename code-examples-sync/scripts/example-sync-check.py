#!/usr/bin/env python3
"""Audit Markdown code fences for obvious drift indicators."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

FENCE_RE = re.compile(r"```(?P<lang>[^\n`]*)\n(?P<body>.*?)```", re.DOTALL)
PLACEHOLDERS = ("TODO", "your-api-key", "example.com", "lorem ipsum")


def inspect_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    findings: list[str] = []
    for index, match in enumerate(FENCE_RE.finditer(text), start=1):
        lang = match.group("lang").strip()
        body = match.group("body")
        if not lang:
            findings.append(f"{path}: code fence #{index} has no language tag")
        for token in PLACEHOLDERS:
            if token.lower() in body.lower():
                findings.append(f"{path}: code fence #{index} contains placeholder '{token}'")
                break
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
            findings.extend(inspect_file(file_path))

    if findings:
        print("\n".join(findings))
        return 1

    print("No obvious code example drift markers found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
