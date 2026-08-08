# CLAUDE.md

This repository contains shared skills for GitHub Copilot, Claude Code, and
Codex.

## Required Session Start Rule

- Every new session in this workspace must begin by reading `LESSON.md`.
- Treat `LESSON.md` as required startup context before analysis, planning, edits, validation, reviews, or advisory work.
- If `LESSON.md` is missing or unreadable, stop and report that blocker before continuing.

## Required Completion, Sync, and Publish Rule

- For every user-requested mutation task in this workspace, complete the requested work in `C:\Users\LOQ\.copilot\skills` first.
- After the work is complete, run the repo validation, then sync outward to the downstream skill folders every time.
- If the AI agent judges the result satisfactory, commit and push to GitHub without asking for another confirmation.
- Treat work as satisfactory only when validation passes, sync completes, the
  task is complete, no requested step was skipped, no required command was
  rejected, no unresolved secret/security/privacy issue remains, and the final
  diff matches the user's request.
- Elevate to the user before commit or push when there are security concerns,
  incomplete work, skipped steps, rejected or blocked required commands,
  validation/sync failures, unexpected unrelated dirty files that make staging
  unsafe, or any other reason the work is not satisfactory.
- For read-only or advisory tasks with no file changes, do not create empty sync, commit, or push churn; report that no mutation workflow was needed.

## Repository Role

- Main branch: `C:\Users\LOQ\.copilot\skills`
- New maintained skills must be added or imported here first
- Maintained skills live here and are synced outward to downstream targets
- Copied official superpowers are tracked here for discovery and Codex sync, but they are not maintained the same way

## Current Counts

Snapshot date: `2026-08-08`. Local overlay totals can differ by machine.

- Git-tracked catalog in this repository:
  - `155` tracked skill folders
  - `123` tracked maintained skills
  - `32` tracked copied official Superpowers
- Live local workspace snapshot (includes local-only overlays such as `gws-*` and `recipe-*` when present):
  - `213` local skill folders detected
  - `181` local maintained skills detected
  - `32` local copied official Superpowers detected

Copied official superpowers are identified by the explicit `copied_official_superpowers` list in `scripts/skill-registry.json`, not by whether a skill folder has a `CHANGELOG.md`.

All `155` tracked skills use catalog `version: "2.0"`. The `131` unchanged
pre-existing tracked skills retain `last_updated: 2026-07-29`; the eight
official Tavily imports use `last_updated: 2026-07-30`; the eight skills
touched by the frontend consolidation use `last_updated: 2026-08-02`; and the
eight selected Matt Pocock imports use `last_updated: 2026-08-08`. The `58`
local-only Google Workspace overlays retain upstream `version: "0.22.5"`
while sharing the 2026-07-29 retained-client section and validation baseline.
The tracked imports `docx`, `jupyter-notebook`, `pptx`, and `xlsx` now have finalized canonical provenance in `scripts/skill-registry.json`.

The Tavily suite is sourced from `tavily-ai/skills` at commit
`ea5e8201b0d3ed9c10b70b71187589bd761fe2d2`. Claude Code sessions using the
GLM Coding Plan endpoint should use the external `tvly` CLI, official SDK, or a
healthy configured Tavily MCP server; they must not assume subscription-only
browser integrations.

The selected Matt Pocock import is sourced from `mattpocock/skills` at commit
`84fdeffd12f2ee307994d1eb6feb48173b6e0502`. It adds eight cross-client gaps
for architecture, domain modeling, prototypes, primary-source research,
conflict resolution, handoffs, and agent-document writing. Keep the existing
catalog equivalents for TDD, debugging, review, implementation, planning, and
skill authoring as the canonical overlapping workflows.

`frontend-design` is the only general frontend creation and art-direction
skill. Use it instead of the retired `frontend-skill` and
`premium-frontend-ui` names. Keep `web-design-reviewer` separate for
post-implementation visual QA and keep framework, Figma, and Stitch skills for
their specialized workflows.

## Downstream Sync Targets

The only approved downstream sync destinations are these three personal-global roots:

- `C:\Users\LOQ\.agents\skills`
- `C:\Users\LOQ\.codex\skills`
- `C:\Users\LOQ\.claude\skills`

There must be no downstream sync to any other path. The sync script enforces this list and refuses to write anywhere else.

Per-target routing:

- Maintained skills sync to `C:\Users\LOQ\.codex\skills`, `C:\Users\LOQ\.agents\skills`, and `C:\Users\LOQ\.claude\skills`.
- Copied official superpowers sync only to the `superpowers` subfolder of the shared mirror: `C:\Users\LOQ\.agents\skills\superpowers` (this is inside the approved `.agents\skills` root, not a separate destination).
- The six `codex_system_managed_skills` stay authoritative under Codex
  `.system` and are skipped by top-level Codex mirror writes. Their normalized
  parent copies still sync to the shared and Claude roots.
- Sync removes known catalog-owned top-level route conflicts, but preserves
  unknown personal skills and all Codex `.system` folders.
- Sync removes the exact retired catalog copies `frontend-skill` and
  `premium-frontend-ui` from these three approved roots.

Treat those paths as synced mirrors or branch targets, not as the place to author new maintained skills.
Host-provided or plugin-managed skills that are not part of this maintained catalog should stay external unless you intentionally vendor them into this repo.

Do not mirror copied official superpowers into `C:\Users\LOQ\.claude\skills` unless you explicitly want local overrides over Claude's plugin-managed copies.

## Claude Code With GLM Coding Plan

- The GLM Coding Plan endpoint changes the model provider through Claude
  Code's Anthropic-compatible environment variables. It does not change the
  personal skill root: use `C:\Users\LOQ\.claude\skills`.
- Do not assume native Claude in Chrome is available. Anthropic's current
  native integration requires direct paid-plan and authentication
  prerequisites that third-party API endpoints do not satisfy.
- Inspect `claude mcp list` and the active session tool list before naming or
  calling a browser tool. A connected external Chrome DevTools, Puppeteer, or
  Playwright MCP can provide browser automation; a search or reader tool
  cannot publish through an authenticated LinkedIn session.
- Keep login, CAPTCHA, upload, and final-submit actions confirmation-gated.
  Stop at a manual handoff when no healthy authenticated browser surface is
  exposed.

## Upstream-Only Skill Sources

Normal child promotion is limited to the personal `.codex` and `.claude`
roots. Project-local paths such as `C:\Assumption University` are not scanned
or written unless a later user request explicitly places them in scope.

To pull a skill from such a root into this parent catalog, promote it upstream and record provenance:

- Use `python scripts/promote-child-skills.py --map <source> <name>` for an explicit child skill or `--discover <root>` to flatten a categorized skill tree. Normalize invalid underscore or title-style names to lowercase hyphen-case.
- Then run `python scripts/update-skill-registry.py` to refresh provenance, copied-official classification, and `REFERENCE_SOURCES.md`.

The only downstream sync call is to the three approved personal-global roots:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\sync-skills.ps1
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
2. Sync outward if the repo is in a good state

For a catalog-wide documentation refresh, treat validation and sync as required
even when the inventory counts stay the same.

The validator now expects the catalog frontmatter fields plus the portability, MCP, Anti-Patterns, Related Skills, and `CHANGELOG.md` baseline.
Catalog policy also expects each `SKILL.md` to include `## Verification Protocol` immediately after `## Anti-Patterns`.
Changelog entries should use `Added`, `Changed`, and `Fixed` sections only; the validator rejects `### Tested` and `### Verified` headings.
The tracked imports `docx`, `jupyter-notebook`, `pptx`, and `xlsx` now validate against the shared catalog structure and have finalized provenance metadata.

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
- update `AGENTS.md`
- update `CHANGELOG.md`
- update `CLAUDE.md`
- update `LESSON.md`
- update `MIGRATION.md` when a breaking client or sync boundary changes

## Codex Notes

- Treat `C:\Users\LOQ\.codex\skills` as the primary Codex install root.
- Treat `C:\Users\LOQ\.agents\skills` as a shared mirror that other local workflows can reuse.
- Do not describe the shared mirror as the only Codex path in repo docs or skill guidance.
- The Codex install root can contain extra local skills outside this catalog, so verify sync by checking the expected maintained set rather than raw folder totals alone.

## Related Repo Files

- `README.md`: catalog and maintenance commands
- `CHANGELOG.md`: repo-wide change history
- `CONTRIBUTING.md`: contribution workflow and repo validation expectations
- `LESSON.md`: maintenance lessons and gotchas
- `MIGRATION.md`: version 2.0 breaking migration and rollback guidance
- `SECURITY.md`: vulnerability reporting and sensitive-disclosure guidance
