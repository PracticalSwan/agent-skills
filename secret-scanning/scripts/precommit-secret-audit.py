#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path


IGNORE_DIRS = {
    ".git",
    ".next",
    ".serena",
    ".turbo",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "out",
    "tmp",
}

TEXT_SUFFIXES = {
    ".c",
    ".conf",
    ".cs",
    ".css",
    ".env",
    ".go",
    ".ini",
    ".java",
    ".js",
    ".json",
    ".jsx",
    ".mjs",
    ".php",
    ".properties",
    ".ps1",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".sql",
    ".tf",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}

PATTERNS = {
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "github_pat": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,255}\b"),
    "slack_token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "connection_string": re.compile(r"(?:AccountKey|SharedAccessKey|Password)\s*=\s*[^;\n]+", re.IGNORECASE),
    "secret_assignment": re.compile(
        r"\b(?:api[_-]?key|secret|token|password|client[_-]?secret)\b\s*[:=]\s*['\"][^'\"]{8,}['\"]",
        re.IGNORECASE,
    ),
}


def iter_text_files(paths: list[Path], include_docs: bool) -> list[Path]:
    results: list[Path] = []
    for start in paths:
        if start.is_file():
            candidates = [start]
        else:
            candidates = [p for p in start.rglob("*") if p.is_file()]
        for path in candidates:
            if any(part in IGNORE_DIRS for part in path.parts):
                continue
            suffix = path.suffix.lower()
            if suffix not in TEXT_SUFFIXES and not (include_docs and suffix == ".md"):
                continue
            if suffix == ".md" and not include_docs:
                continue
            results.append(path)
    return sorted(set(results))


def shannon_entropy(value: str) -> float:
    counts = {char: value.count(char) for char in set(value)}
    length = len(value)
    return -sum((count / length) * math.log2(count / length) for count in counts.values())


def scan_file(path: Path, include_entropy: bool) -> list[dict]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []

    findings: list[dict] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        matched_on_line = False
        for name, pattern in PATTERNS.items():
            match = pattern.search(line)
            if match:
                matched_on_line = True
                findings.append(
                    {
                        "file": path.as_posix(),
                        "line": line_number,
                        "type": name,
                        "snippet": line.strip()[:160],
                    }
                )
        if include_entropy and not matched_on_line:
            for token in re.findall(r"[A-Za-z0-9_=.-]{24,}", line):
                if token.startswith(("http", "https", "./", "../")):
                    continue
                if shannon_entropy(token) >= 4.2 and any(char.isdigit() for char in token) and any(char.isalpha() for char in token):
                    findings.append(
                        {
                            "file": path.as_posix(),
                            "line": line_number,
                            "type": "high_entropy_token",
                            "snippet": token[:160],
                        }
                    )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a local pre-commit audit for obvious secrets.")
    parser.add_argument("--path", action="append", default=[], help="File or directory to scan. Repeat as needed.")
    parser.add_argument("--include-docs", action="store_true", help="Scan Markdown files as well.")
    parser.add_argument("--no-entropy", action="store_true", help="Disable the high-entropy token heuristic.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable text.")
    args = parser.parse_args()

    roots = [Path(value).resolve() for value in (args.path or ["."])]
    findings: list[dict] = []
    for file_path in iter_text_files(roots, args.include_docs):
        findings.extend(scan_file(file_path, include_entropy=not args.no_entropy))

    if args.json:
        print(json.dumps({"findings": findings}, indent=2))
    else:
        if not findings:
            print("No obvious secret patterns found.")
        else:
            print("Potential secrets found:")
            for finding in findings:
                print(f"- {finding['type']} @ {finding['file']}:{finding['line']} :: {finding['snippet']}")

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
