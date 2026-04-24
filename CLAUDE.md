# CLAUDE.md

This repository contains shared skills for GitHub Copilot, Claude Code, Codex, and Gemini CLI.

## Repository Role

- Main branch: `C:\Users\LOQ\.copilot\skills`
- New maintained skills must be added or imported here first
- Maintained skills live here and are synced outward to downstream targets
- Copied official superpowers are tracked here for discovery and Codex sync, but they are not maintained the same way

## Current Counts

Snapshot date: `2026-04-24`. Local overlay totals can differ by machine.

- Git-tracked catalog in this repository:
	- `67` tracked skill folders
	- `53` tracked maintained skills
	- `14` tracked copied official superpowers
- Live local workspace snapshot (includes local-only overlays such as `gws-*` and `recipe-*` when present):
	- `125` local skill folders detected
	- `111` local maintained skills detected
	- `14` local copied official superpowers detected

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

## Maintained Skill Expectations

Every maintained skill should have:

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
- include the portable minimum frontmatter fields: `name` and `description`
- use only approved extra top-level metadata fields when needed: `license`, `version`, `compatibility`, and `metadata`
- use activation-focused descriptions
- include the generated portability section
- include the MCP or no-MCP fallback section

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

## Related Repo Files

- `README.md`: catalog and maintenance commands
- `CHANGELOG.md`: repo-wide change history
- `GEMINI.md`: Gemini CLI usage guidance
- `LESSON.md`: maintenance lessons and gotchas
