#!/usr/bin/env python3
from __future__ import annotations

import json
import re
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
SKIP_SCAN_DIRS = {".git", ".serena"}
SKIP_BYTECODE_DIRS = {".git", ".serena", ".venv", "venv", "env", "__pycache__"}
BAD_TEXT_MARKERS = {
    "\u00e2\u20ac\u201d": "mojibake em dash",
    "\u00e2\u0153\u201c": "mojibake check mark",
    "\ufffd": "replacement character",
}
STALE_REFERENCES = {"../nestjs/SKILL.md": "removed nestjs skill"}
REMOVED_CLIENT_RE = re.compile(r"\b(?:Gemini\s+CLI|Antigravity(?:\s+CLI)?)\b", re.IGNORECASE)
VALID_SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ACTIVE_ROOT_DOCS = [
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "CONTRIBUTING.md",
    "LESSON.md",
    "SECURITY.md",
    "REFERENCE_SOURCES.md",
]


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
    codex_system_managed = registry.get("codex_system_managed_skills")
    codex_local_only = registry.get("codex_local_only_skill_names")
    skill_dirs = sorted(
        skill_dir
        for skill_dir in repo_root.iterdir()
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists()
    )
    skill_names = {skill_dir.name for skill_dir in skill_dirs}

    issues: list[str] = []

    if not isinstance(codex_system_managed, list) or not codex_system_managed:
        issues.append("scripts/skill-registry.json must define codex_system_managed_skills.")
        codex_system_managed = []
    elif codex_system_managed != sorted(set(codex_system_managed)):
        issues.append("codex_system_managed_skills must be unique and sorted.")

    unknown_system_skills = sorted(set(codex_system_managed) - skill_names)
    if unknown_system_skills:
        issues.append(
            "codex_system_managed_skills names missing from the parent catalog: "
            + ", ".join(unknown_system_skills)
            + "."
        )
    system_superpower_overlap = sorted(set(codex_system_managed) & superpower_skills)
    if system_superpower_overlap:
        issues.append(
            "Codex system-managed skills cannot also be copied official Superpowers: "
            + ", ".join(system_superpower_overlap)
            + "."
        )

    if not isinstance(codex_local_only, list) or not codex_local_only:
        issues.append("scripts/skill-registry.json must define codex_local_only_skill_names.")
        codex_local_only = []
    elif codex_local_only != sorted(set(codex_local_only)):
        issues.append("codex_local_only_skill_names must be unique and sorted.")
    local_only_parent_overlap = sorted(set(codex_local_only) & skill_names)
    if local_only_parent_overlap:
        issues.append(
            "Codex-local-only skills must not exist in the parent catalog: "
            + ", ".join(local_only_parent_overlap)
            + "."
        )
    local_sets = registry.get("codex_local_only_skill_sets", {})
    blender_set = local_sets.get("blender_skills") if isinstance(local_sets, dict) else None
    if not isinstance(blender_set, dict):
        issues.append("codex_local_only_skill_sets.blender_skills must be defined.")
    else:
        expected = {
            "checkout": "C:/Users/LOQ/.codex/vendor/blender-skills",
            "install_root": "C:/Users/LOQ/.codex/skills",
            "scope": "codex-only",
            "never_promote_to_parent": True,
            "never_sync_to_shared": True,
            "never_sync_to_claude": True,
        }
        for key, value in expected.items():
            if blender_set.get(key) != value:
                issues.append(f"Blender Codex-local-only policy mismatch for {key}: {blender_set.get(key)!r}.")

    for skill_dir in skill_dirs:
        skill_path = skill_dir / "SKILL.md"
        try:
            metadata = parse_frontmatter(skill_path)
        except ValueError as exc:
            issues.append(str(exc))
            continue

        body = skill_path.read_text(encoding="utf-8")
        if REMOVED_CLIENT_RE.search(body):
            issues.append(
                f"{skill_dir.name}: active SKILL.md still names removed Gemini or Antigravity support."
            )
        if "## Cross-Client Portability" not in body:
            issues.append(f"{skill_dir.name}: missing Cross-Client Portability section.")
        if "## MCP Availability And Fallback" not in body:
            issues.append(f"{skill_dir.name}: missing MCP Availability And Fallback section.")
        if "## Anti-Patterns" not in body:
            issues.append(f"{skill_dir.name}: missing Anti-Patterns section.")
        if "## Verification Protocol" not in body:
            issues.append(f"{skill_dir.name}: missing Verification Protocol section.")
        if "## Related Skills" not in body:
            issues.append(f"{skill_dir.name}: missing Related Skills section.")
        if "Preferred MCP Server:" not in body:
            issues.append(f"{skill_dir.name}: MCP section is missing the Preferred MCP Server line.")
        if "Fallback prompt:" not in body:
            issues.append(f"{skill_dir.name}: MCP section is missing the fallback prompt line.")
        if metadata["name"] != skill_dir.name:
            issues.append(f"{skill_dir.name}: frontmatter name '{metadata['name']}' does not match folder name.")
        if not VALID_SKILL_NAME_RE.fullmatch(skill_dir.name):
            issues.append(f"{skill_dir.name}: folder name must use lowercase hyphen-case.")
        unknown_keys = sorted(set(metadata) - ALLOWED_FRONTMATTER_KEYS)
        if unknown_keys:
            issues.append(f"{skill_dir.name}: unsupported top-level frontmatter keys: {', '.join(unknown_keys)}.")

        changelog_path = skill_dir / "CHANGELOG.md"
        if changelog_path.exists():
            changelog = changelog_path.read_text(encoding="utf-8")
            for banned_heading in ("### Tested", "### Verified"):
                if re.search(rf"(?m)^{re.escape(banned_heading)}\s*$", changelog):
                    issues.append(
                        f"{skill_dir.name}: CHANGELOG.md still uses the banned '{banned_heading[4:]}' heading."
                    )
        else:
            issues.append(f"{skill_dir.name}: skill folder is missing CHANGELOG.md.")

        if skill_dir.name in superpower_skills and skill_dir.name in registry["reference_installs"]:
            issues.append(
                f"{skill_dir.name}: copied official superpower should not also be listed under reference_installs."
            )

        headings = re.findall(r"(?m)^## (.+?)\s*$", body)
        if "Anti-Patterns" in headings and "Verification Protocol" in headings:
            anti_index = headings.index("Anti-Patterns")
            verification_index = headings.index("Verification Protocol")
            if verification_index != anti_index + 1:
                issues.append(
                    f"{skill_dir.name}: Verification Protocol must immediately follow Anti-Patterns."
                )
        if headings and headings[-1] != "Related Skills":
            issues.append(f"{skill_dir.name}: Related Skills must be the final level-two section.")

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

    if "gemini_namespace" in registry:
        issues.append("scripts/skill-registry.json still defines removed Gemini command metadata.")

    for doc_name in ACTIVE_ROOT_DOCS:
        doc_path = repo_root / doc_name
        if not doc_path.is_file():
            issues.append(f"{doc_path}: required active root documentation is missing.")
            continue
        if REMOVED_CLIENT_RE.search(doc_path.read_text(encoding="utf-8")):
            issues.append(f"{doc_path}: active root documentation still names a removed client.")

    sync_script = (repo_root / "scripts" / "sync-skills.ps1").read_text(encoding="utf-8")
    for required_root in (
        r"C:\Users\LOQ\.agents\skills",
        r"C:\Users\LOQ\.codex\skills",
        r"C:\Users\LOQ\.claude\skills",
    ):
        if required_root not in sync_script:
            issues.append(f"scripts/sync-skills.ps1 is missing approved downstream root {required_root}.")

    removed_paths = [
        repo_root / ".gemini",
        repo_root / "GEMINI.md",
        repo_root / "scripts" / "export-gemini-skill.py",
        repo_root / "using-superpowers" / "references" / "antigravity-tools.md",
    ]
    for removed_path in removed_paths:
        if removed_path.exists():
            issues.append(f"{removed_path}: removed Gemini or Antigravity support surface still exists.")

    if issues:
        print(json.dumps({"status": "failed", "issues": issues}, indent=2))
        return 1

    print(
        json.dumps(
            {
                "status": "ok",
                "skills": len(skill_dirs),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
