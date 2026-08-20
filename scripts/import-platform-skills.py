#!/usr/bin/env python3
"""Import pinned vendor skills and normalize them for this catalog.

The source repositories are intentionally supplied by the caller.  This keeps
network fetches, authentication, and source review outside the write step while
making the actual catalog import deterministic and repeatable.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = SCRIPT_DIR / "platform_skill_manifest.py"
MANIFEST_SPEC = importlib.util.spec_from_file_location("platform_skill_manifest", MANIFEST_PATH)
if MANIFEST_SPEC is None or MANIFEST_SPEC.loader is None:  # pragma: no cover
    raise RuntimeError(f"Unable to load {MANIFEST_PATH}")
MANIFEST = importlib.util.module_from_spec(MANIFEST_SPEC)
MANIFEST_SPEC.loader.exec_module(MANIFEST)

MODERNIZE_PATH = SCRIPT_DIR / "modernize-skills.py"
MODERNIZE_SPEC = importlib.util.spec_from_file_location("modernize_skills", MODERNIZE_PATH)
if MODERNIZE_SPEC is None or MODERNIZE_SPEC.loader is None:  # pragma: no cover
    raise RuntimeError(f"Unable to load {MODERNIZE_PATH}")
MODERNIZE = importlib.util.module_from_spec(MODERNIZE_SPEC)
MODERNIZE_SPEC.loader.exec_module(MODERNIZE)
MODERNIZE.DATE_STAMP = MANIFEST.SNAPSHOT_DATE
MODERNIZE.CATALOG_VERSION = "2.0"


FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)
H1_RE = re.compile(r"(?m)^# (.+?)\s*$")


def _unquote(value: str) -> str:
    value = value.strip()
    if value.startswith(('"', "'")) and value[-1:] == value[0]:
        try:
            return json.loads(value) if value.startswith('"') else value[1:-1]
        except json.JSONDecodeError:
            return value[1:-1]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("Source SKILL.md is missing YAML frontmatter.")

    lines = match.group(1).splitlines()
    metadata: dict[str, str] = {}
    active_key: str | None = None
    block_values: list[str] = []

    def flush_block() -> None:
        nonlocal block_values, active_key
        if active_key == "description" and block_values:
            metadata[active_key] = " ".join(value.strip() for value in block_values).strip()
        block_values = []

    for line in lines:
        if line.startswith((" ", "\t")) and active_key == "description":
            block_values.append(line)
            continue
        if ":" not in line:
            continue
        flush_block()
        key, raw_value = line.split(":", 1)
        active_key = key.strip()
        value = raw_value.strip()
        if active_key == "description" and value in {">", ">-", "|", "|-"}:
            continue
        metadata[active_key] = _unquote(value)
    flush_block()

    if not metadata.get("description"):
        metadata["description"] = "Use the imported workflow within its documented scope."
    return metadata, text[match.end() :]


def render_frontmatter(name: str, metadata: dict[str, str], tags: str) -> str:
    lines = [
        "---",
        f"name: {name}",
        'version: "2.0"',
        f"last_updated: {MANIFEST.SNAPSHOT_DATE}",
        f"tags: {tags}",
        f"description: {json.dumps(metadata['description'].strip(), ensure_ascii=False)}",
    ]
    for key in ("license", "compatibility"):
        value = metadata.get(key, "").strip()
        if value and value not in {">", ">-", "|", "|-"}:
            lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    return "\n".join(lines) + "\n---\n\n"


def related_section(repo_root: Path, name: str, spec: dict[str, object]) -> str:
    configured = list(spec.get("related", ()))
    candidates = configured or ("verification-before-completion", "documentation-verification")
    links: list[str] = []
    for related in candidates:
        if related == name or not (repo_root / related / "SKILL.md").is_file():
            continue
        links.append(
            f"- [{related}](../{related}/SKILL.md): Use it when the task also needs its adjacent workflow."
        )
        if len(links) == 3:
            break
    if not links:
        links.append(
            "- [verification-before-completion](../verification-before-completion/SKILL.md): Use it to verify the completed workflow."
        )
    return "## Related Skills\n\n" + "\n".join(links)


def replace_related(body: str, section: str) -> str:
    marker = re.search(r"(?ms)^## Related Skills\s*$.*\Z", body)
    if marker:
        return body[: marker.start()].rstrip() + "\n\n" + section + "\n"
    return body.rstrip() + "\n\n" + section + "\n"


def windows_cli_section(name: str, vendor: str) -> str:
    if vendor == "Vercel":
        command = "vercel"
    elif vendor == "Netlify":
        command = "netlify"
    else:
        command = vendor.lower()
    return f"""## Windows CLI Compatibility

- Resolve `{command}` with PowerShell `Get-Command` before invoking it; use the
  installed `.cmd` or `.ps1` shim when PowerShell does not resolve the bare name.
- Keep tokens and environment values in an approved secret store or local
  environment. Never paste them into commands, logs, or committed config.
- Treat an unavailable CLI or unauthenticated session as a reported blocker;
  use the documented manual or API fallback instead of installing a runtime
  implicitly.
"""


def needs_windows_cli_section(name: str, vendor: str) -> bool:
    if vendor == "Vercel":
        return name in {"deploy-to-vercel", "vercel-cli-with-tokens", "vercel-optimize"}
    if vendor == "Netlify":
        return name in {"netlify-config", "netlify-database", "netlify-deploy"}
    return False


def normalize_skill(repo_root: Path, destination: Path, name: str, spec: dict[str, object], registry: dict) -> None:
    skill_path = destination / "SKILL.md"
    source_text = skill_path.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(source_text)
    title_match = H1_RE.search(body)
    title = title_match.group(1) if title_match else name.replace("-", " ").title()
    body = MODERNIZE.normalize_sections(body, name, title, registry)
    body = replace_related(body, related_section(repo_root, name, spec))
    if needs_windows_cli_section(name, str(spec["vendor"])):
        body = body.replace(
            "<!-- PORTABILITY:START -->",
            windows_cli_section(name, str(spec["vendor"])) + "\n<!-- PORTABILITY:START -->",
            1,
        )
    skill_path.write_text(
        render_frontmatter(name, metadata, MANIFEST.tags_for(name, str(spec["vendor"]))) + body,
        encoding="utf-8",
    )

    changelog = destination / "CHANGELOG.md"
    source_repo, source_commit = MANIFEST.SOURCE_COMMITS[spec["source_key"]]
    changelog.write_text(
        f"""# Changelog

All notable changes to the `{name}` skill are documented here.

## [{MANIFEST.SNAPSHOT_DATE}] - Vendor Skill Import

### Added

- Imported the canonical `{spec['source_path']}` workflow from `{source_repo}` at commit `{source_commit}`.
- Normalized catalog metadata, retained-client portability, MCP fallback, safety, verification, and related-skill routing.

### Changed

- Preserved the upstream workflow and support files while adding this catalog's cross-client wrapper.

### Fixed

- Added explicit fallback and approval boundaries so the skill does not assume unavailable host tools or credentials.
""",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=True, help="Directory containing the pinned source clones.")
    parser.add_argument("--repo-root", default=str(SCRIPT_DIR.parent))
    parser.add_argument("--force", action="store_true", help="Replace existing destination folders.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    source_root = Path(args.source_root).resolve()
    registry_path = repo_root / "scripts" / "skill-registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry.setdefault("mcp_skills", {})
    for name, spec in MANIFEST.PLATFORM_SKILLS.items():
        server = spec.get("mcp_server")
        if server:
            registry["mcp_skills"][name] = {
                "mode": "Preferred",
                "servers": [server],
                "fallback": list(
                    MANIFEST.MCP_FALLBACKS.get(
                        server,
                        (
                            f"Use official {spec['vendor']} documentation, CLI, or SDKs when the {server} surface is unavailable.",
                            "Do not claim an MCP operation was used when the active host does not expose it.",
                        ),
                    )
                ),
            }

    copied: list[str] = []
    skipped: list[str] = []
    source_dirs: dict[str, Path] = {}
    for name, spec in MANIFEST.PLATFORM_SKILLS.items():
        clone_dir = MANIFEST.SOURCE_CLONE_DIRS[spec["source_key"]]
        source_dir = source_root / clone_dir / Path(str(spec["source_path"]))
        if not (source_dir / "SKILL.md").is_file():
            raise FileNotFoundError(f"Missing pinned source skill for {name}: {source_dir}")
        destination = repo_root / name
        if destination.exists():
            if not args.force:
                skipped.append(name)
                continue
            shutil.rmtree(destination)
        shutil.copytree(source_dir, destination)
        source_dirs[name] = source_dir
        copied.append(name)

        if bool(spec.get("copy_repo_license")):
            source_license = source_root / clone_dir / "LICENSE"
            if source_license.is_file() and not (destination / "LICENSE.txt").exists():
                shutil.copy2(source_license, destination / "LICENSE.txt")

    for name in copied:
        normalize_skill(repo_root, repo_root / name, name, MANIFEST.PLATFORM_SKILLS[name], registry)

    print(
        json.dumps(
            {
                "status": "ok",
                "snapshot": MANIFEST.SNAPSHOT_DATE,
                "copied": copied,
                "skipped_existing": skipped,
                "cli_skills_not_installed": list(MANIFEST.CLI_SKILLS_NOT_INSTALLED),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
