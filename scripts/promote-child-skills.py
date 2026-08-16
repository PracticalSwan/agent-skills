#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)
VALID_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CATEGORY = r"(?:architecture|collaboration|debugging|meta|problem-solving|research|testing)"
CATEGORIZED_PATH_RE = re.compile(
    rf"(?:\$\{{SUPERPOWERS_SKILLS_ROOT\}}/)?skills/{CATEGORY}/"
    r"(?P<name>[a-z0-9]+(?:-[a-z0-9]+)*)(?P<suffix>/[A-Za-z0-9_.\-/]+)?"
)
CLAUDE_PATH_RE = re.compile(
    rf"~/\.claude/skills/{CATEGORY}/"
    r"(?P<name>[a-z0-9]+(?:-[a-z0-9]+)*)(?P<suffix>/[A-Za-z0-9_.\-/]+)?"
)
ROOT_SKILL_PATH_RE = re.compile(
    r"(?:\$\{SUPERPOWERS_SKILLS_ROOT\}/)?skills/"
    r"(?P<name>using-skills)(?P<suffix>/[A-Za-z0-9_.\-/]+)?"
)


def read_name(skill_path: Path) -> str:
    text = skill_path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError(f"{skill_path} is missing YAML frontmatter.")
    for line in match.group(1).splitlines():
        if line.startswith((" ", "\t")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        if key.strip() == "name":
            return value.strip().strip("'\"")
    raise ValueError(f"{skill_path} is missing a frontmatter name.")


def assert_destination(repo_root: Path, name: str) -> Path:
    if not VALID_NAME_RE.fullmatch(name):
        raise ValueError(f"Invalid destination skill name: {name}")
    destination = (repo_root / name).resolve()
    destination.relative_to(repo_root)
    return destination


def replace_skill(source: Path, destination: Path, preserve_skill: bool) -> str:
    source = source.resolve()
    if not (source / "SKILL.md").is_file():
        raise ValueError(f"Source skill is missing SKILL.md: {source}")

    preserved: dict[str, bytes] = {}
    if destination.exists():
        for filename in ["CHANGELOG.md", *( ["SKILL.md"] if preserve_skill else [])]:
            candidate = destination / filename
            if candidate.is_file():
                preserved[filename] = candidate.read_bytes()
        shutil.rmtree(destination)
        action = "refreshed"
    else:
        action = "imported"

    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns(
            ".git",
            ".DS_Store",
            "__pycache__",
            "*.pyc",
        ),
    )
    for filename, content in preserved.items():
        (destination / filename).write_bytes(content)
    return action


def replace_support_path(source: Path, destination_skill: Path, relative_path: str) -> str:
    source = source.resolve()
    relative = Path(relative_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"Support destination must stay inside a skill folder: {relative_path}")
    destination = (destination_skill / relative).resolve()
    destination.relative_to(destination_skill.resolve())
    if not source.exists():
        raise ValueError(f"Support source does not exist: {source}")

    if destination.exists():
        if destination.is_dir():
            shutil.rmtree(destination)
        else:
            destination.unlink()
        action = "support-refreshed"
    else:
        action = "support-imported"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.copytree(
            source,
            destination,
            ignore=shutil.ignore_patterns(
                ".git",
                ".DS_Store",
                "__pycache__",
                "*.pyc",
            ),
        )
    else:
        shutil.copy2(source, destination)
    return action


def refresh_core(source_skill: Path, destination_skill: Path, tail_heading: str) -> None:
    source_text = source_skill.read_text(encoding="utf-8")
    destination_text = destination_skill.read_text(encoding="utf-8")
    source_match = FRONTMATTER_RE.match(source_text)
    destination_match = FRONTMATTER_RE.match(destination_text)
    if not source_match or not destination_match:
        raise ValueError("Core refresh requires frontmatter in source and destination skills.")

    destination_body = destination_text[destination_match.end() :]
    tail_index = destination_body.find(tail_heading)
    if tail_index < 0:
        raise ValueError(f"Tail heading {tail_heading!r} was not found in {destination_skill}.")

    source_body = source_text[source_match.end() :].rstrip()
    tail = destination_body[tail_index:].lstrip()
    merged = destination_text[: destination_match.end()] + source_body + "\n\n" + tail
    destination_skill.write_text(merged.rstrip() + "\n", encoding="utf-8")


def discover_skills(root: Path) -> list[tuple[Path, str]]:
    discovered: list[tuple[Path, str]] = []
    seen: dict[str, Path] = {}
    for skill_path in sorted(root.rglob("SKILL.md")):
        source = skill_path.parent
        declared_name = read_name(skill_path)
        name = declared_name if VALID_NAME_RE.fullmatch(declared_name) else source.name
        if not VALID_NAME_RE.fullmatch(name):
            raise ValueError(
                f"Discovered skill name and source folder are not folder-safe: "
                f"{declared_name} ({skill_path})"
            )
        if name in seen:
            raise ValueError(f"Duplicate discovered skill name {name}: {seen[name]} and {source}")
        seen[name] = source
        discovered.append((source, name))
    return discovered


def normalize_flattened_references(repo_root: Path, skill_names: set[str]) -> list[str]:
    updated: list[str] = []
    text_suffixes = {".md", ".txt", ".sh"}

    def rewrite(path: Path, text: str, pattern: re.Pattern[str]) -> str:
        def replacement(match: re.Match[str]) -> str:
            name = match.group("name")
            suffix = match.group("suffix") or ""
            if name not in skill_names:
                return match.group(0)
            if not suffix:
                return name
            target = repo_root / name / suffix.lstrip("/")
            return Path(os.path.relpath(target, path.parent)).as_posix()

        return pattern.sub(replacement, text)

    for name in sorted(skill_names):
        skill_dir = repo_root / name
        if not skill_dir.is_dir():
            continue
        for path in sorted(p for p in skill_dir.rglob("*") if p.is_file()):
            if path.suffix.lower() not in text_suffixes:
                continue
            try:
                original = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            text = rewrite(path, original, CATEGORIZED_PATH_RE)
            text = rewrite(path, text, CLAUDE_PATH_RE)
            text = rewrite(path, text, ROOT_SKILL_PATH_RE)
            text = text.replace("${SUPERPOWERS_SKILLS_ROOT}", "<catalog-root>")
            if text != original:
                path.write_text(text, encoding="utf-8")
                updated.append(str(path.relative_to(repo_root)))
    return updated


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Promote child or nested skill folders into the top-level catalog safely."
    )
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument(
        "--map",
        nargs=2,
        action="append",
        metavar=("SOURCE", "DESTINATION"),
        default=[],
        help="Import or refresh one skill folder under a top-level destination name.",
    )
    parser.add_argument(
        "--discover",
        action="append",
        default=[],
        metavar="ROOT",
        help="Recursively discover SKILL.md folders and flatten them by frontmatter name.",
    )
    parser.add_argument(
        "--preserve-skill",
        action="append",
        default=[],
        metavar="DESTINATION",
        help="Preserve the destination SKILL.md while replacing its support files.",
    )
    parser.add_argument(
        "--core-refresh",
        nargs=3,
        action="append",
        default=[],
        metavar=("SOURCE_SKILL", "DESTINATION", "TAIL_HEADING"),
        help="Replace a destination skill's core body while preserving its catalog tail.",
    )
    parser.add_argument(
        "--support-map",
        nargs=3,
        action="append",
        default=[],
        metavar=("SOURCE", "DESTINATION", "RELATIVE_PATH"),
        help="Replace one file or support directory inside an existing destination skill.",
    )
    parser.add_argument(
        "--normalize-flattened",
        nargs="*",
        default=[],
        metavar="SKILL",
        help="Rewrite categorized Superpowers paths for flattened top-level skill folders.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    registry = json.loads((repo_root / "scripts" / "skill-registry.json").read_text(encoding="utf-8"))
    codex_local_only_names = set(registry.get("codex_local_only_skill_names", []))
    preserve_skill = set(args.preserve_skill)
    requested: list[tuple[Path, str]] = [
        (Path(source).resolve(), destination) for source, destination in args.map
    ]
    blocked_explicit = sorted(destination for _, destination in requested if destination in codex_local_only_names)
    if blocked_explicit:
        raise ValueError("Refusing to promote Codex-local-only skills: " + ", ".join(blocked_explicit))
    for discover_root in args.discover:
        requested.extend(
            (source, name)
            for source, name in discover_skills(Path(discover_root).resolve())
            if name not in codex_local_only_names
        )

    unique: dict[str, Path] = {}
    for source, destination in requested:
        if destination in unique and unique[destination] != source:
            raise ValueError(
                f"Destination {destination} has multiple sources: {unique[destination]} and {source}"
            )
        unique[destination] = source

    summary: list[dict[str, str]] = []
    for destination_name, source in sorted(unique.items()):
        destination = assert_destination(repo_root, destination_name)
        action = replace_skill(source, destination, destination_name in preserve_skill)
        summary.append(
            {
                "name": destination_name,
                "action": action,
                "source": str(source),
            }
        )

    for source_skill, destination_name, tail_heading in args.core_refresh:
        destination = assert_destination(repo_root, destination_name) / "SKILL.md"
        refresh_core(Path(source_skill).resolve(), destination, tail_heading)
        summary.append(
            {
                "name": destination_name,
                "action": "core-refreshed",
                "source": str(Path(source_skill).resolve()),
            }
        )

    for source_path, destination_name, relative_path in args.support_map:
        destination = assert_destination(repo_root, destination_name)
        if not (destination / "SKILL.md").is_file():
            raise ValueError(f"Support destination is not an existing skill: {destination}")
        action = replace_support_path(Path(source_path), destination, relative_path)
        summary.append(
            {
                "name": destination_name,
                "action": action,
                "source": str(Path(source_path).resolve()),
            }
        )

    normalized_paths = normalize_flattened_references(repo_root, set(args.normalize_flattened))

    print(
        json.dumps(
            {
                "promoted": summary,
                "count": len(summary),
                "normalized_paths": normalized_paths,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
