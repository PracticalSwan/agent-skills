# AGENTS.md

This repository contains shared skills for GitHub Copilot, Claude Code, and
Codex, and this file defines the workspace-specific rules that should
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
- After the work is complete, run the repo validation, then sync outward to the
  downstream skill folders every time.
- If the AI agent judges the result satisfactory, commit and push to GitHub
  without asking for another confirmation.
- Treat work as satisfactory only when validation passes, sync completes,
  the task is complete, no requested step was skipped, no required command was
  rejected, no unresolved secret/security/privacy issue remains, and the final
  diff matches the user's request.
- Elevate to the user before commit or push when there are security concerns,
  incomplete work, skipped steps, rejected or blocked required commands,
  validation/sync failures, unexpected unrelated dirty files that make
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

Snapshot date: `2026-07-30`. Local overlay totals can differ by machine.

- Git-tracked catalog in this repository:
  - `149` tracked skill folders
  - `117` tracked maintained skills
  - `32` tracked copied official Superpowers
- Live local workspace snapshot, including local-only overlays such as
  `gws-*` and `recipe-*` when present:
  - `207` local skill folders detected
  - `175` local maintained skills detected
  - `32` local copied official Superpowers detected

Copied official superpowers are identified by the explicit
`copied_official_superpowers` list in `scripts/skill-registry.json`, not by
whether a skill folder has a `CHANGELOG.md`.

All `149` tracked skills use catalog `version: "2.0"`. The `141` pre-existing
tracked skills retain `last_updated: 2026-07-29`; the eight official Tavily
imports use `last_updated: 2026-07-30`. The `58` local-only Google Workspace
overlays keep their upstream `version: "0.22.5"` while sharing the 2026-07-29
retained-client section and validation baseline.

The tracked imports `docx`, `jupyter-notebook`, `pptx`, and `xlsx` now have
finalized canonical provenance. Child-path promotion is handled by
`scripts/promote-child-skills.py`, while `scripts/update-skill-registry.py`
refreshes provenance and the reference-source report.

The Tavily suite is sourced from `tavily-ai/skills` at commit
`ea5e8201b0d3ed9c10b70b71187589bd761fe2d2`. Keep its eight skills
self-contained, retain the local secret and prompt-injection safeguards, and
do not reintroduce removed-client integrations from upstream references.

## Source Of Truth

- Edit maintained skill content in `C:\Users\LOQ\.copilot\skills` first.
- Treat `SKILL.md` as the source of truth for skill behavior and wording.
- Treat downstream skill roots as synced mirrors or deployment targets, not as
  the place to author maintained content.

## Downstream Sync Targets

The only approved downstream sync destinations are these three personal-global
roots:

- `C:\Users\LOQ\.agents\skills`
- `C:\Users\LOQ\.codex\skills`
- `C:\Users\LOQ\.claude\skills`

There must be no downstream sync to any other path. The sync script enforces
this allowlist and refuses to write anywhere else.

Per-target routing:

- Maintained skills sync to `C:\Users\LOQ\.codex\skills`,
  `C:\Users\LOQ\.agents\skills`, and `C:\Users\LOQ\.claude\skills`.
- Copied official superpowers sync only to the `superpowers` subfolder of the
  shared mirror: `C:\Users\LOQ\.agents\skills\superpowers` (inside the approved
  `.agents\skills` root, not a separate destination).
- Skills listed in `codex_system_managed_skills` are excluded from top-level
  Codex mirror writes because Codex owns their `.system` copies. Their
  normalized parent copies still deploy to the shared and Claude roots.
- Sync removes known catalog-owned top-level shadows that violate those
  routes, including copied Superpowers outside the shared `superpowers`
  subfolder. It must preserve unknown personal skills and Codex `.system`.

Host-provided or plugin-managed skills that are not part of this maintained
catalog should stay external unless you intentionally vendor them into this
repo.

## Upstream-Only Skill Sources

Normal child discovery is limited to the personal `.codex` and `.claude`
skill roots. Project-local roots under paths such as
`C:\Assumption University` must not be scanned or used as sync destinations
unless a later user request explicitly puts them in scope.

When a child or categorized skill root contains a skill absent from this
parent, audit its activation boundary and provenance, then promote it upstream
with `scripts/promote-child-skills.py`. Flatten nested folders by the normalized
lowercase hyphen-case skill name; do not copy invalid underscore or title-style
names into the parent unchanged. Then refresh provenance with
`scripts/update-skill-registry.py`.

The only downstream sync call is to the three approved personal-global roots:

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
2. Sync outward if the repo is in a good state.

For a catalog-wide documentation refresh, treat validation and sync as required
even when the inventory counts stay the same.

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
- update `MIGRATION.md` when a breaking client or sync boundary changes

## Agent-Specific Notes

- GitHub Copilot should treat this file and the workspace root docs as the
  portable instruction source when folder-based skill discovery is limited.
- Claude Code should follow this file alongside `CLAUDE.md`, with the narrower
  local instruction taking precedence if they differ.
- Claude Code sessions using the GLM Coding Plan endpoint must not assume
  Anthropic's native Chrome integration or Codex-only tools are available.
  Use only active, healthy external MCP/browser tools and preserve manual
  fallbacks.
- Codex should treat `C:\Users\LOQ\.codex\skills` as the primary Codex install
  root and `C:\Users\LOQ\.agents\skills` as a shared mirror for cross-client
  reuse.
- Codex system-managed skill folders remain authoritative in
  `C:\Users\LOQ\.codex\skills\.system`; never overwrite them through the
  top-level mirror sync.

## Related Repo Files

- `README.md`: catalog and maintenance commands
- `CHANGELOG.md`: repo-wide change history
- `CLAUDE.md`: Claude Code usage guidance
- `CONTRIBUTING.md`: contribution workflow and repo validation expectations
- `LESSON.md`: maintenance lessons and gotchas
- `MIGRATION.md`: version 2.0 breaking migration and rollback guidance
- `SECURITY.md`: vulnerability reporting and sensitive-disclosure guidance
