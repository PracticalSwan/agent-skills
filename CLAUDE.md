# CLAUDE.md

This repository contains shared skills for GitHub Copilot, Claude Code, Codex, and Gemini CLI.

## Repository Role

- Main branch: `C:\Users\LOQ\.copilot\skills`
- New maintained skills must be added or imported here first
- Maintained skills live here and are synced outward to downstream targets
- Copied official superpowers are tracked here for discovery and Codex sync, but they are not maintained the same way

## Current Counts

- `60` total skill folders
- `46` maintained skills
- `14` copied official superpowers

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
2. Update `REFERENCE_SOURCES.md` when the source was external
3. Update root docs and the relevant changelogs
4. Then sync it to the downstream targets

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
