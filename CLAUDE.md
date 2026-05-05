# CLAUDE.md

This repository contains shared skills for GitHub Copilot, Claude Code, Codex, and Gemini CLI.

## Repository Role

- Main branch: `C:\Users\LOQ\.copilot\skills`
- New maintained skills must be added or imported here first
- Maintained skills live here and are synced outward to downstream targets
- Copied official superpowers are tracked here for discovery and Codex sync, but they are not maintained the same way

## Current Counts

Snapshot date: `2026-05-05`. Local overlay totals can differ by machine.

- Git-tracked catalog in this repository:
	- `71` tracked skill folders
	- `57` tracked maintained skills
	- `14` tracked copied official superpowers
- Live local workspace snapshot (includes local-only overlays such as `gws-*` and `recipe-*` when present):
	- `129` local skill folders detected
	- `115` local maintained skills detected
	- `14` local copied official superpowers detected

Copied official superpowers are identified by the explicit `copied_official_superpowers` list in `scripts/skill-registry.json`, not by whether a skill folder has a `CHANGELOG.md`.

Most tracked maintained skills are currently aligned on `version: "1.2"` with `last_updated: 2026-04-25`.
The tracked imports `docx`, `jupyter-notebook`, `pptx`, and `xlsx` are present in git but still need catalog normalization before they match that schema baseline.

## Downstream Sync Targets

Maintained skills sync to:

- `C:\Users\LOQ\.codex\skills`
- `C:\Users\LOQ\.agents\skills`
- `C:\Users\LOQ\.claude\skills`

Treat those paths as synced mirrors or branch targets, not as the place to author new maintained skills.
Host-provided or plugin-managed skills that are not part of this maintained catalog should stay external unless you intentionally vendor them into this repo.

The full current skill catalog syncs to:

- `C:\Users\LOQ\.gemini\antigravity\global_skills`

Copied official superpowers sync only to:

- `C:\Users\LOQ\.agents\skills\superpowers`

Do not mirror copied official superpowers into `C:\Users\LOQ\.claude\skills` unless you explicitly want local overrides over Claude's plugin-managed copies.

## Gemini CLI Support

Gemini CLI uses generated command files from:

- `C:\Users\LOQ\.copilot\skills\.gemini\commands\skills`
- `C:\Users\LOQ\.gemini\antigravity\global_skills`

After editing skills:

1. Run `python scripts/export-gemini-skill.py --all`
2. Reload commands in Gemini CLI with `/commands reload`

`SKILL.md` remains the source of truth. The Gemini command files are generated artifacts.

## Workspace-Aware Sync

The sync script can also discover workspace-local skill roots under a search root when they live inside:

- `.agent\skills`
- `.agents\skills`
- `.claude\skills`

Use:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\sync-skills.ps1 -WorkspaceSearchRoot "C:\Assumption University"
```

To skip workspace-local targets and sync only the personal global roots, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\sync-skills.ps1 -SkipWorkspaceRoots
```

## Catalog Skill Expectations

Every skill folder in this catalog should have:

- `SKILL.md`
- `CHANGELOG.md`

Recommended support folders:

- `references/`
- `scripts/`

Optional:

- `examples/`
- `LICENSE.txt`

## SKILL.md Rules

Every `SKILL.md` in this repo should:

- use valid YAML frontmatter
- keep the `name` aligned with the folder name
- include the catalog frontmatter fields: `name`, `version`, `last_updated`, `tags`, and `description`
- use only approved extra top-level metadata fields when needed: `license`, `compatibility`, and `metadata`
- use activation-focused descriptions
- include the generated portability section
- include the MCP or no-MCP fallback section
- include `## Anti-Patterns`
- include `## Verification Protocol`
- end with `## Related Skills`

## MCP Rules

When editing MCP-aware skills:

1. Name the preferred MCP server explicitly.
2. Add a practical fallback path for environments without that MCP surface.
3. Avoid claiming a host-specific tool wrapper exists unless you verified it.
4. Prefer local scripts, CLIs, or browser workflows as the fallback evidence path.

The MCP mapping source lives in `scripts/skill-registry.json`.

## Validation Workflow

After meaningful changes:

1. Run `python scripts/validate-skills.py`
2. Run `python scripts/export-gemini-skill.py --all`
3. Re-run validation if the export changed
4. Sync outward if the repo is in a good state

For a catalog-wide documentation refresh, treat the export and sync steps as required even when the inventory counts stay the same.

The validator now expects the catalog frontmatter fields plus the portability, MCP, Anti-Patterns, Related Skills, and `CHANGELOG.md` baseline.
Catalog policy also expects each `SKILL.md` to include `## Verification Protocol` immediately after `## Anti-Patterns`.
New changelog entries should use `Added`, `Changed`, and `Fixed` sections only; do not add a `### Tested` section.
The tracked raw imports `docx`, `jupyter-notebook`, `pptx`, and `xlsx` are the current known exceptions until they are modernized in this repo.

After adding a new maintained skill:

1. Install or import it into this repo first
2. Prefer the canonical upstream source when a discovery list points to a stronger maintained original
3. Update `REFERENCE_SOURCES.md` and `scripts/skill-registry.json` when the source was external
4. Smoke-test any bundled helper scripts or local fallback workflow
5. Update root docs and the relevant changelogs
6. Then sync it to the downstream targets

## Documentation Rules

When repo behavior, counts, sync flow, portability, or supported clients change:

- update `README.md`
- update `CHANGELOG.md`
- update `CLAUDE.md`
- update `LESSON.md`
- update `GEMINI.md` if Gemini CLI behavior changed

## Codex Notes

- Treat `C:\Users\LOQ\.codex\skills` as the primary Codex install root.
- Treat `C:\Users\LOQ\.agents\skills` as a shared mirror that other local workflows can reuse.
- Do not describe the shared mirror as the only Codex path in repo docs or skill guidance.
- The Codex install root can contain extra local skills outside this catalog, so verify sync by checking the expected maintained set rather than raw folder totals alone.

## Related Repo Files

- `README.md`: catalog and maintenance commands
- `CHANGELOG.md`: repo-wide change history
- `GEMINI.md`: Gemini CLI usage guidance
- `LESSON.md`: maintenance lessons and gotchas
