# AGENTS.md

This repository contains shared skills for GitHub Copilot, Claude Code, Codex,
and Gemini CLI, and this file defines the workspace-specific rules that should
apply to any AI agent operating in `C:\Users\LOQ\.copilot\skills`.

## Required Session Start Rule

- Every new session in this workspace must begin by reading `LESSON.md`.
- Treat `LESSON.md` as required startup context before analysis, planning,
  edits, validation, reviews, or advisory work.
- If `LESSON.md` is missing or unreadable, stop and report that blocker before
  continuing.

## Required Completion, Sync, And Publish Rule

- For every user-requested mutation task in this workspace, complete the
  requested work in `C:\Users\LOQ\.copilot\skills` first.
- After the work is complete, run the repo validation and Gemini export, then
  sync outward to the downstream skill folders every time.
- If the AI agent judges the result satisfactory, commit and push to GitHub
  without asking for another confirmation.
- Treat work as satisfactory only when validation/export pass, sync completes,
  the task is complete, no requested step was skipped, no required command was
  rejected, no unresolved secret/security/privacy issue remains, and the final
  diff matches the user's request.
- Elevate to the user before commit or push when there are security concerns,
  incomplete work, skipped steps, rejected or blocked required commands,
  validation/export/sync failures, unexpected unrelated dirty files that make
  staging unsafe, or any other reason the work is not satisfactory.
- For read-only or advisory tasks with no file changes, do not create empty
  sync, commit, or push churn; report that no mutation workflow was needed.

## Workspace Role

- Main branch: `C:\Users\LOQ\.copilot\skills`
- New maintained skills must be added or imported here first.
- Maintained skills live here and are synced outward to downstream targets.
- Copied official superpowers are tracked here for discovery and cross-client
  sync, but they are not maintained the same way as the catalog's maintained
  skills.

## Current Counts

Snapshot date: `2026-07-11`. Local overlay totals can differ by machine.

- Git-tracked catalog in this repository:
  - `134` tracked skill folders
  - `102` tracked maintained skills
  - `32` tracked copied official Superpowers
- Live local workspace snapshot, including local-only overlays such as
  `gws-*` and `recipe-*` when present:
  - `192` local skill folders detected
  - `160` local maintained skills detected
  - `32` local copied official Superpowers detected

Copied official superpowers are identified by the explicit
`copied_official_superpowers` list in `scripts/skill-registry.json`, not by
whether a skill folder has a `CHANGELOG.md`.

All `134` tracked skills are aligned on catalog `version: "1.3"` and
`last_updated: 2026-07-11`. The `58` local-only Google Workspace overlays keep
their upstream `version: "0.22.5"` while sharing the same 2026-07-11 section
and validation baseline.

The tracked imports `docx`, `jupyter-notebook`, `pptx`, and `xlsx` now have
finalized canonical provenance. Child-path promotion is handled by
`scripts/promote-child-skills.py`, while `scripts/update-skill-registry.py`
refreshes provenance and the reference-source report.

## Source Of Truth

- Edit maintained skill content in `C:\Users\LOQ\.copilot\skills` first.
- Treat `SKILL.md` as the source of truth for skill behavior and wording.
- Do not hand-edit generated Gemini command files under `.gemini/commands`.
- Treat downstream skill roots as synced mirrors or deployment targets, not as
  the place to author maintained content.

## Downstream Sync Targets

The only approved downstream sync destinations are these five personal-global
roots:

- `C:\Users\LOQ\.agents\skills`
- `C:\Users\LOQ\.codex\skills`
- `C:\Users\LOQ\.claude\skills`
- `C:\Users\LOQ\.gemini\antigravity\global_skills`
- `C:\Users\LOQ\.gemini\antigravity-cli\skills`

There must be no downstream sync to any other path. The sync script enforces
this allowlist and refuses to write anywhere else.

Per-target routing:

- Maintained skills sync to `C:\Users\LOQ\.codex\skills`,
  `C:\Users\LOQ\.agents\skills`, and `C:\Users\LOQ\.claude\skills`.
- Copied official superpowers sync only to the `superpowers` subfolder of the
  shared mirror: `C:\Users\LOQ\.agents\skills\superpowers` (inside the approved
  `.agents\skills` root, not a separate destination).
- The full current skill catalog (maintained plus copied official superpowers)
  syncs to both Gemini roots: `C:\Users\LOQ\.gemini\antigravity\global_skills`
  and `C:\Users\LOQ\.gemini\antigravity-cli\skills`.

Host-provided or plugin-managed skills that are not part of this maintained
catalog should stay external unless you intentionally vendor them into this
repo.

## Upstream-Only Skill Sources

Workspace-local skill roots (`.agent\skills`, `.agents\skills`, and
`.claude\skills` under project trees such as `C:\Assumption University`) are
upstream sources only, never downstream sync destinations. The sync script no
longer writes to them.

When a child or categorized skill root contains a skill absent from this
parent, audit its activation boundary and provenance, then promote it upstream
with `scripts/promote-child-skills.py`. Flatten nested folders by the normalized
lowercase hyphen-case skill name; do not copy invalid underscore or title-style
names into the parent unchanged. Then refresh provenance with
`scripts/update-skill-registry.py`.

The only downstream sync call is to the five approved personal-global roots:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\sync-skills.ps1
```

## Skill Catalog Expectations

Every maintained skill folder in this catalog should have:

- `SKILL.md`
- `CHANGELOG.md`

Recommended support folders:

- `references/`
- `scripts/`

Optional:

- `examples/`
- `LICENSE.txt`

Every `SKILL.md` in this repo should:

- use valid YAML frontmatter
- keep the `name` aligned with the folder name
- include the catalog frontmatter fields: `name`, `version`, `last_updated`,
  `tags`, and `description`
- use only approved extra top-level metadata fields when needed: `license`,
  `compatibility`, and `metadata`
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
4. Prefer local scripts, CLIs, or browser workflows as the fallback evidence
   path.

The MCP mapping source lives in `scripts/skill-registry.json`.

## Validation Workflow

After meaningful changes:

1. Run `python scripts/validate-skills.py`.
2. Run `python scripts/export-gemini-skill.py --all`.
3. Re-run validation if the export changed.
4. Sync outward if the repo is in a good state.

For a catalog-wide documentation refresh, treat the export and sync steps as
required even when the inventory counts stay the same.

The validator now expects the catalog frontmatter fields plus the portability,
MCP, Anti-Patterns, Related Skills, and `CHANGELOG.md` baseline. Catalog policy
also expects each `SKILL.md` to include `## Verification Protocol`
immediately after `## Anti-Patterns`.

Changelog entries should use `Added`, `Changed`, and `Fixed` sections only;
the validator rejects both `### Tested` and `### Verified` headings.

The tracked imports `docx`, `jupyter-notebook`, `pptx`, and `xlsx` now validate
against the shared catalog structure and have finalized provenance metadata.

After adding a new maintained skill:

1. Install or import it into this repo first.
2. Prefer the canonical upstream source when a discovery list points to a
   stronger maintained original.
3. Update `REFERENCE_SOURCES.md` and `scripts/skill-registry.json` when the
   source was external.
4. Smoke-test any bundled helper scripts or local fallback workflow.
5. Update root docs and the relevant changelogs.
6. Then sync it to the downstream targets.

## Documentation Rules

When repo behavior, counts, sync flow, portability, supported clients, or
workspace startup rules change:

- update `README.md`
- update `AGENTS.md`
- update `CHANGELOG.md`
- update `CLAUDE.md`
- update `LESSON.md`
- update `GEMINI.md` if Gemini CLI behavior changed

## Agent-Specific Notes

- GitHub Copilot should treat this file and the workspace root docs as the
  portable instruction source when folder-based skill discovery is limited.
- Claude Code should follow this file alongside `CLAUDE.md`, with the narrower
  local instruction taking precedence if they differ.
- Codex should treat `C:\Users\LOQ\.codex\skills` as the primary Codex install
  root and `C:\Users\LOQ\.agents\skills` as a shared mirror for cross-client
  reuse.
- Gemini CLI should use generated command files from
  `C:\Users\LOQ\.copilot\skills\.gemini\commands\skills` and reload commands
  after export.
- Antigravity should consume the synced global skill catalog from
  `C:\Users\LOQ\.gemini\antigravity\global_skills` and the Antigravity CLI from
  `C:\Users\LOQ\.gemini\antigravity-cli\skills`, rather than treating this repo
  as a manual copy source.

## Related Repo Files

- `README.md`: catalog and maintenance commands
- `CHANGELOG.md`: repo-wide change history
- `CLAUDE.md`: Claude Code usage guidance
- `CONTRIBUTING.md`: contribution workflow and repo validation expectations
- `GEMINI.md`: Gemini CLI usage guidance
- `LESSON.md`: maintenance lessons and gotchas
- `SECURITY.md`: vulnerability reporting and sensitive-disclosure guidance
