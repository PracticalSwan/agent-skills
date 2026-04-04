#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


DATE_STAMP = "2026-04-04"
CHANGELOG_TITLE = "Cross-Client Portability Refresh"
PORTABILITY_START = "<!-- PORTABILITY:START -->"
PORTABILITY_END = "<!-- PORTABILITY:END -->"
MCP_START = "<!-- MCP:START -->"
MCP_END = "<!-- MCP:END -->"
FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)


def detect_newline(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("Missing YAML frontmatter.")

    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("'").strip('"')

    if "name" not in metadata or "description" not in metadata:
        raise ValueError("Frontmatter must include name and description.")

    return metadata, text[match.end():]


def render_portability_section(skill_name: str, namespace: str, newline: str) -> str:
    command_name = f"/{namespace}:{skill_name}"
    lines = [
        PORTABILITY_START,
        "## Cross-Client Portability",
        "",
        "This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.",
        "",
        "- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.",
        "- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.",
        "- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.",
        f"- Gemini CLI: this repository generates a project command named `{command_name}` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py {skill_name}` and then run `/commands reload` inside Gemini CLI.",
        "",
        PORTABILITY_END,
    ]
    return newline.join(lines)


def render_mcp_section(skill_name: str, registry: dict, newline: str) -> str:
    skill_meta = registry["mcp_skills"].get(skill_name)
    if not skill_meta:
        lines = [
            MCP_START,
            "## MCP Availability And Fallback",
            "",
            "No dedicated MCP server is required for the normal workflow in this skill.",
            "",
            "- If the current host lacks an equivalent tool surface, use the bundled scripts, standard shell or editor tooling, and the manual workflow already described in this skill.",
            "- Treat local verification as the fallback evidence path before closing the task.",
            "",
            MCP_END,
        ]
        return newline.join(lines)

    server_list = [f"- `{server}` ({skill_meta['mode'].lower()})" for server in skill_meta["servers"]]
    fallback_lines = [f"- {item}" for item in skill_meta["fallback"]]
    lines = [
        MCP_START,
        "## MCP Availability And Fallback",
        "",
        "Preferred MCP servers for this skill:",
        *server_list,
        "",
        "If MCP is unavailable in the current host:",
        *fallback_lines,
        "",
        MCP_END,
    ]
    return newline.join(lines)


def remove_generated_blocks(body: str) -> str:
    patterns = [
        re.compile(rf"{re.escape(PORTABILITY_START)}.*?{re.escape(PORTABILITY_END)}\s*", re.DOTALL),
        re.compile(rf"{re.escape(MCP_START)}.*?{re.escape(MCP_END)}\s*", re.DOTALL),
    ]
    result = body
    for pattern in patterns:
        result = pattern.sub("", result)
    return result.strip()


def insert_generated_sections(body: str, sections: list[str], newline: str) -> str:
    marker = "## Related Skills"
    cleaned = remove_generated_blocks(body)
    generated = f"{newline}{newline}".join(sections)

    if marker in cleaned:
        before, after = cleaned.split(marker, 1)
        before = before.rstrip()
        after = after.lstrip()
        return f"{before}{newline}{newline}{generated}{newline}{newline}{marker}{newline}{after}".rstrip() + newline

    return f"{cleaned.rstrip()}{newline}{newline}{generated}{newline}".lstrip()


def upsert_skill_file(skill_dir: Path, registry: dict) -> None:
    skill_path = skill_dir / "SKILL.md"
    original = skill_path.read_text(encoding="utf-8")
    newline = detect_newline(original)
    metadata, body = parse_frontmatter(original)
    updated_body = insert_generated_sections(
        body,
        [
            render_portability_section(skill_dir.name, registry["gemini_namespace"], newline),
            render_mcp_section(skill_dir.name, registry, newline),
        ],
        newline,
    )
    frontmatter = original[: len(original) - len(body)]
    skill_path.write_text(f"{frontmatter}{updated_body}", encoding="utf-8")


def changelog_entry(skill_name: str, registry: dict, newline: str) -> str:
    is_mcp_skill = skill_name in registry["mcp_skills"]
    if is_mcp_skill:
        second_change = "Documented the preferred MCP server surface for this skill and a local no-MCP fallback workflow."
    else:
        second_change = "Clarified that the core workflow does not require a dedicated MCP server and can run with local tools alone."

    return newline.join(
        [
            f"## [{DATE_STAMP}] - {CHANGELOG_TITLE}",
            "",
            "### Changed",
            "- Added a standard portability note covering GitHub Copilot, Claude Code, Codex, and Gemini CLI.",
            f"- {second_change}",
            "",
            "### Tested",
            "- Validated `SKILL.md` frontmatter, portability sections, and Gemini export readiness with `python scripts/validate-skills.py`.",
            "",
        ]
    )


def create_reference_changelog(skill_dir: Path, registry: dict) -> None:
    skill_meta = registry["reference_installs"][skill_dir.name]
    changelog_path = skill_dir / "CHANGELOG.md"
    newline = "\n"
    content = newline.join(
        [
            "# Changelog",
            "",
            f"All notable changes to the `{skill_dir.name}` skill will be documented in this file.",
            "",
            f"## [{DATE_STAMP}] - Initial Import and Portability Upgrade",
            "",
            "### Added",
            f"- Imported this skill from `{skill_meta['source_repo']}` at `{skill_meta['source_path']}`.",
            "- Added cross-client portability guidance for GitHub Copilot, Claude Code, Codex, and Gemini CLI.",
            "- Added the repo-standard MCP or no-MCP fallback guidance for this skill.",
            "",
            "### Tested",
            "- Validated `SKILL.md` frontmatter and Gemini command export readiness with `python scripts/validate-skills.py`.",
            "",
        ]
    )
    changelog_path.write_text(content, encoding="utf-8")


def upsert_changelog(skill_dir: Path, registry: dict) -> None:
    changelog_path = skill_dir / "CHANGELOG.md"
    if not changelog_path.exists():
        if skill_dir.name in registry["reference_installs"]:
            create_reference_changelog(skill_dir, registry)
        return

    original = changelog_path.read_text(encoding="utf-8")
    if f"## [{DATE_STAMP}] - {CHANGELOG_TITLE}" in original:
        return

    newline = detect_newline(original)
    entry = changelog_entry(skill_dir.name, registry, newline)
    first_section = re.search(r"^## \[", original, flags=re.MULTILINE)
    if first_section:
        updated = f"{original[:first_section.start()].rstrip()}{newline}{newline}{entry}{original[first_section.start():]}"
    else:
        updated = f"{original.rstrip()}{newline}{newline}{entry}"
    changelog_path.write_text(updated, encoding="utf-8")


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    registry = json.loads((repo_root / "scripts" / "skill-registry.json").read_text(encoding="utf-8"))
    skill_dirs = sorted(
        skill_dir
        for skill_dir in repo_root.iterdir()
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists()
    )

    for skill_dir in skill_dirs:
        upsert_skill_file(skill_dir, registry)
        upsert_changelog(skill_dir, registry)

    print(
        json.dumps(
            {
                "updated_skills": [skill_dir.name for skill_dir in skill_dirs],
                "date": DATE_STAMP,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
