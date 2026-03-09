#!/usr/bin/env python3
"""Find front-end patterns that often correlate with visual defects."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

PATTERNS = {
    r"\bwidth:\s*[0-9]{4,}px": "Very wide fixed pixel width",
    r"\bheight:\s*[0-9]{4,}px": "Very tall fixed pixel height",
    r"\boverflow:\s*hidden": "Potential clipping risk",
    r"\b100vw\b": "Viewport-width layout can cause horizontal scroll",
    r"\bposition:\s*fixed": "Fixed positioning can obscure content",
    r"\bmin-width:\s*[0-9]{4,}px": "Large minimum width can break mobile layout",
}

FILE_GLOBS = ("*.css", "*.scss", "*.sass", "*.tsx", "*.jsx", "*.ts", "*.js")


def scan(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    findings: list[str] = []
    for pattern, label in PATTERNS.items():
        for match in re.finditer(pattern, text, re.IGNORECASE):
            line = text.count("\n", 0, match.start()) + 1
            findings.append(f"{path}:{line}: {label}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Project root to scan")
    args = parser.parse_args()

    root = Path(args.root)
    files: list[Path] = []
    for glob in FILE_GLOBS:
        files.extend(root.rglob(glob))

    findings: list[str] = []
    for path in sorted(set(files)):
        findings.extend(scan(path))

    if findings:
        print("\n".join(findings))
        return 1

    print("No high-signal CSS risk patterns found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
