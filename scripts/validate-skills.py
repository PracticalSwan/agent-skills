#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)
ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "version",
    "last_updated",
    "tags",
    "license",
    "metadata",
    "compatibility",
}
REQUIRED_FRONTMATTER_KEYS = {"name", "description", "version", "last_updated", "tags"}
SKIP_SCAN_DIRS = {".git", ".gemini", ".serena"}
SKIP_BYTECODE_DIRS = {".git", ".gemini", ".serena", ".venv", "venv", "env", "__pycache__"}
BAD_TEXT_MARKERS = {
    "\u00e2\u20ac\u201d": "mojibake em dash",
    "\u00e2\u0153\u201c": "mojibake check mark",
    "\ufffd": "replacement character",
}
STALE_REFERENCES = {"../nestjs/SKILL.md": "removed nestjs skill"}


def parse_frontmatter(skill_path: Path) -> dict[str, str]:
    text = skill_path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
      raise ValueError(f"{skill_path} is missing YAML frontmatter.")

    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if line.startswith((" ", "\t")):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("'").strip('"')

    missing_required = sorted(REQUIRED_FRONTMATTER_KEYS - set(metadata))
    if missing_required:
        raise ValueError(
            f"{skill_path} is missing required frontmatter keys: {', '.join(missing_required)}."
        )
    return metadata


def iter_source_markdown(repo_root: Path) -> list[Path]:
    return sorted(
        path
        for path in repo_root.rglob("*.md")
        if not any(part in SKIP_SCAN_DIRS for part in path.parts)
    )


def has_generated_bytecode(repo_root: Path) -> list[Path]:
    return sorted(
        path
        for path in repo_root.rglob("*.pyc")
        if not any(part in SKIP_BYTECODE_DIRS for part in path.parts)
    )


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    registry = json.loads((repo_root / "scripts" / "skill-registry.json").read_text(encoding="utf-8"))
    superpower_skills = set(registry["copied_official_superpowers"])
    skill_dirs = sorted(
        skill_dir
        for skill_dir in repo_root.iterdir()
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists()
    )

    issues: list[str] = []

    for skill_dir in skill_dirs:
        skill_path = skill_dir / "SKILL.md"
        try:
            metadata = parse_frontmatter(skill_path)
        except ValueError as exc:
            issues.append(str(exc))
            continue

        body = skill_path.read_text(encoding="utf-8")
        if "## Cross-Client Portability" not in body:
            issues.append(f"{skill_dir.name}: missing Cross-Client Portability section.")
        if "## MCP Availability And Fallback" not in body:
            issues.append(f"{skill_dir.name}: missing MCP Availability And Fallback section.")
        if "## Anti-Patterns" not in body:
            issues.append(f"{skill_dir.name}: missing Anti-Patterns section.")
        if "## Related Skills" not in body:
            issues.append(f"{skill_dir.name}: missing Related Skills section.")
        if "Preferred MCP Server:" not in body:
            issues.append(f"{skill_dir.name}: MCP section is missing the Preferred MCP Server line.")
        if "Fallback prompt:" not in body:
            issues.append(f"{skill_dir.name}: MCP section is missing the fallback prompt line.")
        if metadata["name"] != skill_dir.name:
            issues.append(f"{skill_dir.name}: frontmatter name '{metadata['name']}' does not match folder name.")
        unknown_keys = sorted(set(metadata) - ALLOWED_FRONTMATTER_KEYS)
        if unknown_keys:
            issues.append(f"{skill_dir.name}: unsupported top-level frontmatter keys: {', '.join(unknown_keys)}.")

        changelog_path = skill_dir / "CHANGELOG.md"
        if changelog_path.exists():
            changelog = changelog_path.read_text(encoding="utf-8")
            if "### Verified" in changelog:
                issues.append(f"{skill_dir.name}: CHANGELOG.md still uses the banned '### Verified' heading.")
        else:
            issues.append(f"{skill_dir.name}: skill folder is missing CHANGELOG.md.")

        if skill_dir.name in superpower_skills and skill_dir.name in registry["reference_installs"]:
            issues.append(
                f"{skill_dir.name}: copied official superpower should not also be listed under reference_installs."
            )

    for markdown_file in iter_source_markdown(repo_root):
        text = markdown_file.read_text(encoding="utf-8")
        is_changelog = markdown_file.name == "CHANGELOG.md"
        if not is_changelog and re.search(r"^## Skill Paths\s*$", text, re.MULTILINE):
            issues.append(f"{markdown_file}: contains obsolete '## Skill Paths' section.")
        for marker, label in BAD_TEXT_MARKERS.items():
            if marker in text:
                issues.append(f"{markdown_file}: contains {label}.")
        for stale_ref, label in STALE_REFERENCES.items():
            if not is_changelog and stale_ref in text:
                issues.append(f"{markdown_file}: contains stale reference to {label}.")

    for pyc_file in has_generated_bytecode(repo_root):
        issues.append(f"{pyc_file}: generated Python bytecode should not be committed or left in the repo.")

    commands_root = repo_root / ".gemini" / "commands" / registry["gemini_namespace"]
    if commands_root.exists():
        command_files = sorted(commands_root.rglob("*.toml"))
        if len(command_files) != len(skill_dirs):
            issues.append(
                f"Gemini command count mismatch: found {len(command_files)} TOML files for {len(skill_dirs)} skills."
            )
        for command_file in command_files:
            try:
                data = tomllib.loads(command_file.read_text(encoding="utf-8"))
            except tomllib.TOMLDecodeError as exc:
                issues.append(f"{command_file}: invalid TOML ({exc}).")
                continue
            if "description" not in data or "prompt" not in data:
                issues.append(f"{command_file}: missing description or prompt.")
    else:
        issues.append(f"{commands_root} does not exist. Run scripts/export-gemini-skill.py first.")

    if issues:
        print(json.dumps({"status": "failed", "issues": issues}, indent=2))
        return 1

    print(
        json.dumps(
            {
                "status": "ok",
                "skills": len(skill_dirs),
                "gemini_commands": len(list(commands_root.rglob('*.toml'))),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
