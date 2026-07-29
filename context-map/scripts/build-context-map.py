#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path


IGNORE_DIRS = {
    ".git",
    ".next",
    ".serena",
    ".turbo",
    ".venv",
    "__pycache__",
    "bin",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "obj",
    "out",
    "tmp",
}

TEXT_SUFFIXES = {
    ".c",
    ".cs",
    ".css",
    ".go",
    ".java",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".mjs",
    ".php",
    ".ps1",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".sql",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}

IMPORT_RE = re.compile(
    r"(?:^|\s)(?:from|import)\s+['\"]([^'\"]+)['\"]|require\(\s*['\"]([^'\"]+)['\"]\s*\)",
    re.MULTILINE,
)


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if is_text_file(path):
            files.append(path)
    return files


def score_file(path: Path, text: str, terms: list[str]) -> int:
    path_text = path.as_posix().lower()
    lowered_text = text.lower()
    score = 0
    for term in terms:
        score += path_text.count(term) * 5
        score += lowered_text.count(term)
    return score


def summarize_role(path: Path) -> str:
    name = path.name.lower()
    lowered = path.as_posix().lower()
    if "test" in name or "spec" in name or "__tests__" in lowered:
        return "Test or verification file"
    if path.suffix.lower() in {".md", ".txt"}:
        return "Documentation or notes"
    if name in {"package.json", "pyproject.toml", "go.mod", "pom.xml", "composer.json"}:
        return "Project manifest or dependency config"
    if path.suffix.lower() in {".yml", ".yaml", ".json", ".toml"}:
        return "Configuration or metadata"
    return "Primary implementation candidate"


def collect_imports(text: str) -> list[str]:
    imports: list[str] = []
    for match in IMPORT_RE.finditer(text):
        value = match.group(1) or match.group(2)
        if value:
            imports.append(value)
    return imports[:8]


def classify(path: Path) -> str:
    lowered = path.as_posix().lower()
    if "test" in lowered or "spec" in lowered:
        return "test"
    if path.suffix.lower() in {".md", ".txt"}:
        return "reference"
    if path.name.lower() in {"package.json", "pyproject.toml", "go.mod", "pom.xml", "composer.json"}:
        return "dependency"
    if path.suffix.lower() in {".json", ".toml", ".yaml", ".yml"}:
        return "dependency"
    return "edit"


def build_map(root: Path, queries: list[str], limit: int) -> str:
    terms = [term.lower() for term in queries if term.strip()]
    scores: dict[Path, tuple[int, str]] = {}

    for path in iter_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        score = score_file(path, text, terms)
        if score <= 0:
            continue
        scores[path] = (score, text)

    ranked = sorted(scores.items(), key=lambda item: (-item[1][0], item[0].as_posix()))[: max(limit * 3, 12)]
    buckets: dict[str, list[tuple[Path, str]]] = defaultdict(list)

    for path, (_, text) in ranked:
        buckets[classify(path)].append((path, text))

    def table(rows: list[str]) -> str:
        return "\n".join(rows) if len(rows) > 2 else "None found."

    edit_rows = [
        "| File | Why it matters | Expected change |",
        "|------|----------------|-----------------|",
    ]
    for path, text in buckets["edit"][:limit]:
        imports = collect_imports(text)
        why = summarize_role(path)
        expected = "Inspect implementation and confirm whether logic, types, or callers must move"
        if imports:
            expected = f"Inspect implementation; imported modules include {', '.join(imports[:2])}"
        edit_rows.append(f"| {path.as_posix()} | {why} | {expected} |")

    dep_rows = [
        "| File | Relationship |",
        "|------|--------------|",
    ]
    for path, text in (buckets["dependency"] + buckets["reference"])[:limit]:
        relation = summarize_role(path)
        imports = collect_imports(text)
        if imports:
            relation = f"Likely wiring or shared dependency; references {', '.join(imports[:2])}"
        dep_rows.append(f"| {path.as_posix()} | {relation} |")

    test_rows = [
        "| File | Coverage |",
        "|------|----------|",
    ]
    for path, _ in buckets["test"][:limit]:
        test_rows.append(f"| {path.as_posix()} | Existing verification path touching the requested area |")

    reference_rows = [
        "| File | Pattern to reuse |",
        "|------|------------------|",
    ]
    for path, _ in buckets["reference"][:limit]:
        reference_rows.append(f"| {path.as_posix()} | Nearby documentation or example that can anchor the implementation |")

    risk_flags = []
    lowered_paths = [path.as_posix().lower() for path, _ in ranked]
    if any(any(token in value for token in ("auth", "permission", "secret", "token")) for value in lowered_paths):
        risk_flags.append("- Authentication, authorization, or secrets may be involved.")
    if any(any(token in value for token in ("schema", "migration", "sql", "model")) for value in lowered_paths):
        risk_flags.append("- Schema or persistence changes may expand the blast radius.")
    if any(any(token in value for token in ("readme", "changelog", "docs")) for value in lowered_paths):
        risk_flags.append("- Documentation may need to move with the code change.")
    if any(path.endswith(("package.json", "pyproject.toml", "go.mod", "pom.xml")) for path in lowered_paths):
        risk_flags.append("- Dependency or build configuration updates may be required.")
    if not risk_flags:
        risk_flags.append("- No special risk markers found from filename heuristics; confirm manually after deeper reads.")

    return "\n".join(
        [
            "## Context Map",
            "",
            "### Query",
            f"- {', '.join(queries)}",
            "",
            "### Likely Edit Targets",
            table(edit_rows),
            "",
            "### Nearby Dependencies",
            table(dep_rows),
            "",
            "### Verification Files",
            table(test_rows),
            "",
            "### Reference Patterns",
            table(reference_rows),
            "",
            "### Risks",
            *risk_flags,
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a starter Markdown context map for a task.")
    parser.add_argument("--root", default=".", help="Repository root to scan.")
    parser.add_argument("--query", action="append", required=True, help="Query term to search for. Repeat as needed.")
    parser.add_argument("--limit", type=int, default=6, help="Maximum rows per section.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    print(build_map(root, args.query, args.limit))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
