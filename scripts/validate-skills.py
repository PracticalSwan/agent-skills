#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)


def parse_frontmatter(skill_path: Path) -> dict[str, str]:
    text = skill_path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
      raise ValueError(f"{skill_path} is missing YAML frontmatter.")

    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("'").strip('"')

    if "name" not in metadata or "description" not in metadata:
        raise ValueError(f"{skill_path} must define both name and description.")
    return metadata


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    registry = json.loads((repo_root / "scripts" / "skill-registry.json").read_text(encoding="utf-8"))
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
        if metadata["name"] != skill_dir.name:
            issues.append(f"{skill_dir.name}: frontmatter name '{metadata['name']}' does not match folder name.")

        changelog_path = skill_dir / "CHANGELOG.md"
        is_reference_install = skill_dir.name in registry["reference_installs"]
        if changelog_path.exists():
            changelog = changelog_path.read_text(encoding="utf-8")
            if "### Verified" in changelog:
                issues.append(f"{skill_dir.name}: CHANGELOG.md still uses the banned '### Verified' heading.")
        elif is_reference_install:
            issues.append(f"{skill_dir.name}: reference install is missing CHANGELOG.md.")

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
