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

## Codex-Only Blender Skills Overlay

- The `arjun988/blender-skills` pack is an explicit exception to normal child promotion.
- Its 94 upstream skills plus the separately protected local
  `raw-scan-to-aaa-preserve-texture` entry (95 protected names total) must
  remain installed only under `C:\Users\LOQ\.codex\skills`, with its source
  checkout under `C:\Users\LOQ\.codex\vendor\blender-skills`.
- Never promote these skill names into this parent catalog and never sync them to `C:\Users\LOQ\.agents\skills` or `C:\Users\LOQ\.claude\skills`.
- `scripts/skill-registry.json` records the protected names and the Codex-only source configuration; generic promotion and sync tooling must honor that boundary.
- During parent source-maintenance or "update all skills" work, run `scripts/update-codex-local-blender-skills.ps1`. It fetches upstream, refreshes only the owned Codex copies and shared Blender references, updates the ownership manifest and source commit, and verifies that no Blender skill escaped to a forbidden root.

## Current Counts

Snapshot date: `2026-08-31`. Local overlay totals can differ by machine.

- Git-tracked catalog in this repository:
  - `237` tracked skill folders
  - `205` tracked maintained skills
  - `32` tracked copied official Superpowers
- Live local workspace snapshot, including local-only overlays such as
  `gws-*` and `recipe-*` when present:
  - `295` local skill folders detected
  - `263` local maintained skills detected
  - `32` local copied official Superpowers detected

Copied official superpowers are identified by the explicit
`copied_official_superpowers` list in `scripts/skill-registry.json`, not by
whether a skill folder has a `CHANGELOG.md`.

All `237` tracked skills use catalog `version: "2.0"`. The `166` pre-existing
tracked skills retain their prior catalog baselines; the 66 platform skills
retain their import provenance, and five Codex Router skills were promoted
from the personal Codex root. The catalog-wide maintenance baseline is
`last_updated: 2026-08-31`. The `58` local-only Google
Workspace overlays keep their upstream `version: "0.22.5"`
while receiving the same retained-client sections and maintenance date.

The tracked imports `docx`, `jupyter-notebook`, `pptx`, and `xlsx` now have
finalized canonical provenance. Child-path promotion is handled by
`scripts/promote-child-skills.py`, while `scripts/update-skill-registry.py`
refreshes provenance and the reference-source report.

The Tavily suite is sourced from `tavily-ai/skills` at commit
`ea5e8201b0d3ed9c10b70b71187589bd761fe2d2`. Keep its eight skills
self-contained, retain the local secret and prompt-injection safeguards, and
do not reintroduce removed-client integrations from upstream references.

The selected Matt Pocock skills are sourced from `mattpocock/skills` at the
current audited commit `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76`. The import
keeps only eight
cross-client workflows that fill gaps for the user's OCR, storefront,
Three.js, and multi-repository work. Existing TDD, debugging, review,
implementation, planning, and skill-authoring equivalents remain canonical.

The 2026-08-14 source refresh audited current upstream heads and updated the
mapped `avoid-ai-writing`, Stitch, Xquik, and Matt Pocock domain-modeling
workflows, plus the affected copied Superpowers workflows. Exact-path audits
left unchanged mapped skills untouched, and imported support material was
reviewed for removed-client paths, credential handling, and no-MCP fallbacks.

The 2026-08-16 child reconciliation compared the eleven newly installed
`.codex` skill trees byte-for-byte with their official upstream paths and
promoted them into the parent: Supabase, Gemini API, Vercel React performance,
and the web-quality audit router plus five focused leaves. The web-quality
leaves remain distinct; the analyzer documents a Windows/manual fallback, and
Supabase/Gemini MCP configuration remains opt-in and authorization-gated.

`frontend-design` is the only general frontend creation and art-direction
skill. The retired names `frontend-skill` and `premium-frontend-ui` redirect
conceptually to `frontend-design`; `web-design-reviewer` remains the separate
post-implementation visual QA skill. Keep framework, Figma, and Stitch skills
separate because they own narrower implementation or tool-specific workflows.

The 2026-08-16 related-skill consolidation audit found no safe content merges.
`supabase` and `supabase-postgres-best-practices`, `gemini-api-dev` and
`gemini-interactions-api`, and the React/web-quality groups remain separate
with explicit routing links because their activation boundaries and evidence
paths differ. Plugin-managed Supabase and React copies remain external; the
parent catalog is canonical for maintained cross-client content.

## 2026-08-20 VoltAgent Platform Import

The VoltAgent repository is a discovery index; canonical vendor repositories
were pinned before import. The 66-skill selection is recorded in
`scripts/platform_skill_manifest.py`: 8 Vercel, 15 Netlify, 7 MongoDB, the
existing current 2-skill Supabase import, 12 Figma, and 24 non-CLI Hugging Face
skills. Source commits and paths are regenerated into `REFERENCE_SOURCES.md`.

CLI gating was based on commands present on this laptop: `vercel`, `netlify`,
and `supabase` were present; `hf`, `huggingface-cli`, `mongosh`, `mongo`, and
`figma` were absent. Therefore Vercel, Netlify, and existing Supabase CLI
guidance is included, while no Hugging Face, MongoDB, or Figma CLI skill was
installed. The importer is repeatable with
`python scripts/import-platform-skills.py --source-root <pinned-clones>`.

## 2026-08-31 Catalog Freshness And Corpus Refresh

- Rechecked all 24 recorded source heads against live remotes. Only
  `avoid-ai-writing` had a new installed-path change: its corpus manifest now
  records small documentation and conversational pre-LLM seeds, and its
  selector-aware extraction helper and tests were refreshed.
- `awesome-copilot` and NVIDIA moved only outside the installed mappings, so
  their provenance pins were updated without broad content rewrites.
- Re-audited `.codex`, `.agents`, and `.claude`; no eligible child-only skills
  remained. The protected Blender/local-only set, Codex `.system`, Superpowers,
  and project-specific paths were not promoted or overwritten.

## 2026-08-29 Catalog Refresh And Mirror Repair

- Re-audited all 24 recorded source heads against live remotes. Refreshed the
  exact mapped paths for `avoid-ai-writing` 3.28.0, `x-twitter-scraper`, both
  Gemini workflows, `react-view-transitions`, and the web-quality support
  trees. Head movement outside installed paths was recorded without broad
  rewrites.
- Updated the catalog to the current 69-category detector, rendered-Markdown
  masking, Gemini transcription/Omni/embedding guidance, current React view
  transition troubleshooting, and field/agentic web-quality references.
- The current Xquik source removed its MCP setup surface, so the registry now
  uses the honest no-MCP fallback instead of advertising an obsolete preferred
  server.
- Re-audited only `.codex`, `.agents`, and `.claude` skill roots. No eligible
  child-only skills remained. The approved sync restored a missing top-level
  Codex `doc` copy without touching `.system`, Blender, Superpowers, or any
  project-specific path.
- The required Blender refresh remains at commit
  `8f778d2405a214b508d4c7d80742be8e43acdd52`: 94 upstream skills plus one
  separately protected local entry.

## 2026-08-24 Catalog Refresh And Child Promotion

- Compared every recorded upstream source head with its exact mapped skill
  path. Refreshed material changes in `avoid-ai-writing`, the eight selected
  Matt Pocock workflows, and `x-twitter-scraper`; unrelated source head
  movement was recorded without rewriting unchanged mapped paths.
- Promoted five eligible personal-Codex child skills: `codex-app-threads`,
  `codex-computer-use`, `codex-in-app-browser`, `codex-router`, and
  `codex-router-media`. Their host marker files remain outside the parent;
  package and tree-digest provenance is recorded in the registry.
- Child reconciliation scanned only `.codex`, `.agents`, and `.claude` skill
  roots. It excluded Codex `.system`, the 94-skill Blender overlay plus the
  separately protected local entry, copied
  official Superpowers, and all project-specific `C:\Assumption University`
  paths. No additional eligible skills remained in `.agents` or `.claude`.
- The required Blender refresh completed at upstream commit
  `8f778d2405a214b508d4c7d80742be8e43acdd52` with 94 upstream skills plus one
  separately protected local entry and no promotion to the parent, shared, or
  Claude roots.

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
- Sync also prunes the exact retired catalog folders `frontend-skill` and
  `premium-frontend-ui` from the three approved roots after their content and
  provenance have been consolidated into `frontend-design`.

Host-provided or plugin-managed skills that are not part of this maintained
catalog should stay external unless you intentionally vendor them into this
repo.

## Upstream-Only Skill Sources

Normal child discovery is limited to the personal `.codex`, `.agents`, and
`.claude` skill roots. Project-local roots under paths such as
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
6. For source maintenance, run
   `scripts/update-codex-local-blender-skills.ps1` as well.
7. Then sync it to the downstream targets.

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
