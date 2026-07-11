# Agent Skills

Shared skill catalog for GitHub Copilot, Claude Code, Codex, and Gemini CLI.

This workspace is the main branch for maintained skills, cross-client portability guidance, Gemini command generation, and MCP fallback rules.
Install or import new maintained skills here first, then sync them outward to the downstream targets.

## Session Start Rule

Every AI agent working in this workspace, including Codex, Claude Code,
Antigravity or Gemini CLI, and GitHub Copilot, must read
[`LESSON.md`](c:\Users\LOQ\.copilot\skills\LESSON.md) at the start of each new
session before analysis, planning, edits, validation, reviews, or advisory
work.

## Completion, Sync, and Publish Rule

For every user-requested mutation task in this workspace, finish the requested
work in `C:\Users\LOQ\.copilot\skills` first, then validate, export Gemini
commands, sync outward to the skill folders, and commit and push to GitHub when
the result is satisfactory.

Treat the work as satisfactory only when validation/export pass, sync completes,
no requested step was skipped, no required command was rejected, no unresolved
secret/security/privacy issue remains, and the final diff matches the user's
request. Escalate to the user instead of committing or pushing when those
conditions are not met. For read-only or advisory tasks with no file changes,
do not create empty sync, commit, or push churn.

## Current Inventory

Snapshot date: `2026-07-11`. Local overlay totals can differ by machine.

- Git-tracked catalog in this repository:
  - `134` tracked skill folders
  - `102` tracked maintained skills
  - `32` tracked copied official Superpowers
- Live local workspace snapshot (includes local-only overlays such as `gws-*` and `recipe-*` when present):
  - `192` local skill folders detected
  - `160` local maintained skills detected
  - `32` local copied official Superpowers detected
- Copied official superpowers are identified by the explicit list in `scripts/skill-registry.json`, not by whether a skill folder has a `CHANGELOG.md`
- The normalized catalog baseline includes:
  - catalog frontmatter with `name`, `version`, `last_updated`, `tags`, and `description`
  - a per-skill `CHANGELOG.md`
  - a cross-client portability section
  - an MCP section that names the preferred server and a no-MCP fallback path
  - an `Anti-Patterns` section
  - a `Verification Protocol` section
  - a final `Related Skills` section
- All `134` tracked skills are aligned on catalog `version: "1.3"` with `last_updated: 2026-07-11`.
- The `58` local-only Google Workspace overlays retain their upstream `version: "0.22.5"` while sharing the 2026-07-11 catalog sections and validation baseline.
- Provenance is complete for `docx`, `jupyter-notebook`, `pptx`, and `xlsx`; the registry now maps them to the current Anthropic or OpenAI canonical sources.
- The 2026-07-11 child-path reconciliation promoted `11` Codex-only skills, `12` workspace-local skills, and `18` newly discovered nested official Superpowers into the parent catalog.

## Main Workspace

- Author, import, and maintain new skills in `C:\Users\LOQ\.copilot\skills`
- Treat the following paths as downstream sync targets or branch mirrors, not authoring roots:
  - `C:\Users\LOQ\.codex\skills`
  - `C:\Users\LOQ\.agents\skills`
  - `C:\Users\LOQ\.claude\skills`
- Sync the full current skill catalog to:
  - `C:\Users\LOQ\.gemini\antigravity\global_skills`
- Sync copied official superpowers only to:
  - `C:\Users\LOQ\.agents\skills\superpowers`
- Leave host-provided or plugin-managed skills outside this repo unless you intentionally choose to vendor and maintain them here
- Generated Gemini CLI commands live under:
  - [`.gemini/commands/skills`](c:\Users\LOQ\.copilot\skills\.gemini\commands\skills)

## Client Support

### GitHub Copilot

- Keep skills in a Copilot-visible skill path or load them through project instructions where folder-based skills are not supported directly.

### Claude Code

- Sync maintained skills to `C:\Users\LOQ\.claude\skills`
- Keep copied official superpowers out of that folder unless you intentionally want local overrides

### Codex

- Sync maintained skills to `C:\Users\LOQ\.codex\skills`
- Keep `C:\Users\LOQ\.agents\skills` as a shared mirror for cross-client reuse and fallback lookups
- Sync copied official superpowers to `C:\Users\LOQ\.agents\skills\superpowers`
- Do not install new maintained skills directly into those target roots; install them in this repo first
- The Codex root can contain extra local skills beyond this catalog, so verify sync by checking that the expected maintained set is present instead of relying only on raw folder totals

### Gemini CLI

- Sync the full current skill catalog to `C:\Users\LOQ\.gemini\antigravity\global_skills`
- Use the generated `/skills:<skill-name>` commands from [`.gemini/commands/skills`](c:\Users\LOQ\.copilot\skills\.gemini\commands\skills)
- Rebuild them with `python scripts/export-gemini-skill.py --all`
- Reload them in Gemini CLI with `/commands reload`
- See [GEMINI.md](c:\Users\LOQ\.copilot\skills\GEMINI.md) for usage notes

## Maintained Skill Structure

```text
skill-name/
|- SKILL.md
|- CHANGELOG.md
|- references/
|  `- supporting-notes.md
|- scripts/
|  `- helper.py
`- examples/
   `- optional-example.md
```

Expected:

- `SKILL.md`
- `CHANGELOG.md`

Recommended:

- `references/`
- `scripts/`

Optional:

- `examples/`
- `LICENSE.txt`

## Validation and Maintenance Commands

When adding a new maintained skill:

1. Add or import it into `C:\Users\LOQ\.copilot\skills`
2. Prefer the canonical upstream source when a discovery catalog points to a stronger maintained original
3. Update `REFERENCE_SOURCES.md` and `scripts/skill-registry.json` if the skill came from an external source
4. Smoke-test any bundled helper scripts or local fallback workflow
5. Update the touched changelogs and root docs
6. Validate and export
7. Sync outward from this repo

Validate all skills and generated Gemini commands:

```powershell
python scripts/validate-skills.py
```

The validator expects:

- catalog frontmatter with `name`, `version`, `last_updated`, `tags`, and `description`
- the portability and MCP sections
- `Preferred MCP Server:` and `Fallback prompt:` inside the MCP section
- `## Anti-Patterns`
- `## Verification Protocol` immediately after `## Anti-Patterns`
- a final `## Related Skills`
- `CHANGELOG.md` in every skill folder
- changelog entries with `Added`, `Changed`, and `Fixed` sections only; `### Tested` and `### Verified` are rejected

Catalog policy also expects each `SKILL.md` to include `## Verification Protocol` immediately after `## Anti-Patterns`.

The tracked imports `docx`, `jupyter-notebook`, `pptx`, and `xlsx` now validate against the shared schema baseline and have finalized canonical provenance metadata.

For a catalog-wide skill refresh, update the root docs in the same pass, then rerun validation, Gemini export, and downstream sync even if the folder counts did not change.

Regenerate Gemini CLI commands:

```powershell
python scripts/export-gemini-skill.py --all
```

Refresh portability and MCP sections across all skills:

```powershell
python scripts/modernize-skills.py
```

Promote explicit child skills or flatten a nested skill catalog into this parent before normalization:

```powershell
python scripts/promote-child-skills.py --map "C:\path\to\child-skill" child-skill
python scripts/promote-child-skills.py --discover "C:\path\to\nested-skill-root"
python scripts/promote-child-skills.py --normalize-flattened skill-one skill-two
```

Refresh source commits, provenance mappings, copied-official classification, and the generated reference-source report:

```powershell
python scripts/update-skill-registry.py
```

Sync maintained skills to Codex, the shared mirror, and Claude, sync the full catalog to Gemini Antigravity, and sync maintained skills to discovered workspace-local roots:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\sync-skills.ps1 -WorkspaceSearchRoot "C:\Assumption University"
```

Sync only the personal global targets and skip workspace-local roots:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\sync-skills.ps1 -SkipWorkspaceRoots
```

## Workspace-Aware Sync

The sync script can now discover and update local project skill folders under a workspace root when they live under:

- `.agent\skills`
- `.agents\skills`
- `.claude\skills`

That allows one pass from this repo into your Codex root, shared mirror root, and project-local skill roots inside `C:\Assumption University`.

## Maintained Skill Catalog

### Workflow and Delivery

- `agentic-eval`
- `breaking-changes-management`
- `code-examples-sync`
- `code-quality`
- `context-map`
- `development-workflow`
- `devops-tooling`
- `documentation-authoring`
- `documentation-automation`
- `documentation-patterns`
- `documentation-quality`
- `documentation-verification`
- `step-by-step-web-project-builder`
- `web-dev-explainer`

### Architecture and Platform

- `cloud-design-patterns`
- `mcp-builder`
- `vercel-deploy`

### Frontend, Design, and Testing

- `canvas-design`
- `excalidraw-diagram-generator`
- `figma`
- `figma-implement-design`
- `frontend-design`
- `frontend-skill`
- `imagegen`
- `legacy-circuit-mockups`
- `nextjs-development`
- `premium-frontend-ui`
- `playwright`
- `react-development`
- `stitch-design`
- `stitch-code-to-design`
- `stitch-design-md`
- `stitch-enhance-prompt`
- `stitch-extract-design-md`
- `stitch-extract-static-html`
- `stitch-generate-design`
- `stitch-loop`
- `stitch-manage-design-system`
- `stitch-react-components`
- `stitch-react-native`
- `stitch-remotion`
- `stitch-shadcn-ui`
- `stitch-taste-design`
- `stitch-upload-to-stitch`
- `screenshot`
- `vite-development`
- `web-design-reviewer`
- `web-testing`

### Languages, Backend, and Data

- `accelerated-computing-cudf`
- `csharp-xunit`
- `dotnet-best-practices`
- `java-docs`
- `java-junit`
- `javascript-development`
- `jupyter-notebook`
- `ds-notebook-strict-code`
- `ds-teaching-assistant`
- `mongodb-mongoose`
- `php-development`
- `powerbi-modeling`
- `sql-development`
- `tabular-eda-review`

### AI, Retrieval, and Accelerated Computing

- `deepstream-dev`
- `deepstream-import-vision-model`
- `nemo-retriever`
- `rag-blueprint`
- `rag-eval`
- `rag-perf`
- `recommender-evaluation`

### Microsoft, Documents, and Office

- `azure-integrations`
- `doc`
- `docx`
- `document-metadata-review`
- `excel-sheet`
- `microsoft-development`
- `pdf`
- `powerpoint-ppt`
- `pptx`
- `spreadsheet-formula-helper`
- `word-document`
- `xlsx`

### Agent and Research

- `agent-task-mapping`
- `avoid-ai-writing`
- `codexer`
- `codebase-to-course`
- `course-content-map`
- `custom-agent-usage`
- `homework-notebook-review`
- `notebook-execution-safety`
- `notebooklm-management`
- `notion-docs`
- `serena-usage`
- `subagent-delegation`

### Security and Specialized

- `infostealer-malware-detector`
- `competition-submission-checker`
- `final-assignment-citation-review`
- `secret-scanning`
- `security-best-practices`
- `security-ownership-map`
- `security-review`
- `security-threat-model`
- `x-twitter-scraper`

## MCP-Aware Skills

These maintained skills are MCP-backed or MCP-aware in this repo:

- `azure-integrations`
- `codexer`
- `devops-tooling`
- `excel-sheet`
- `figma`
- `figma-implement-design`
- `microsoft-development`
- `mongodb-mongoose`
- `nextjs-development`
- `notebooklm-management`
- `notion-docs`
- `powerbi-modeling`
- `powerpoint-ppt`
- `secret-scanning`
- `serena-usage`
- `stitch-code-to-design`
- `stitch-design`
- `stitch-design-md`
- `stitch-enhance-prompt`
- `stitch-extract-design-md`
- `stitch-extract-static-html`
- `stitch-generate-design`
- `stitch-loop`
- `stitch-manage-design-system`
- `stitch-react-components`
- `stitch-react-native`
- `stitch-remotion`
- `stitch-shadcn-ui`
- `stitch-taste-design`
- `stitch-upload-to-stitch`
- `x-twitter-scraper`
- `web-design-reviewer`
- `web-testing`
- `word-document`

The registry for MCP mappings and no-MCP fallback guidance is stored in [scripts/skill-registry.json](c:\Users\LOQ\.copilot\skills\scripts\skill-registry.json).

## Reference Skill Imports

The following externally sourced skills are currently tracked and maintained in this repo.

Imported after auditing the wider `C:\Assumption University` workspace and matching them to real project needs:

- `accelerated-computing-cudf`
- `agentic-eval`
- `avoid-ai-writing`
- `cloud-design-patterns`
- `codebase-to-course`
- `context-map`
- `csharp-xunit`
- `deepstream-dev`
- `deepstream-import-vision-model`
- `dotnet-best-practices`
- `java-docs`
- `java-junit`
- `mcp-builder`
- `nemo-retriever`
- `pdf`
- `premium-frontend-ui`
- `rag-blueprint`
- `rag-eval`
- `rag-perf`
- `secret-scanning`
- `security-review`
- `x-twitter-scraper`
- `doc`
- `docx`
- `figma`
- `figma-implement-design`
- `frontend-skill`
- `imagegen`
- `jupyter-notebook`
- `playwright`
- `pptx`
- `screenshot`
- `security-best-practices`
- `security-ownership-map`
- `security-threat-model`
- `vercel-deploy`
- `xlsx`
- `competition-submission-checker`
- `course-content-map`
- `document-metadata-review`
- `ds-notebook-strict-code`
- `ds-teaching-assistant`
- `final-assignment-citation-review`
- `homework-notebook-review`
- `notebook-execution-safety`
- `recommender-evaluation`
- `step-by-step-web-project-builder`
- `tabular-eda-review`
- `web-dev-explainer`
- `stitch-code-to-design`
- `stitch-design`
- `stitch-design-md`
- `stitch-enhance-prompt`
- `stitch-extract-design-md`
- `stitch-extract-static-html`
- `stitch-generate-design`
- `stitch-loop`
- `stitch-manage-design-system`
- `stitch-react-components`
- `stitch-react-native`
- `stitch-remotion`
- `stitch-shadcn-ui`
- `stitch-taste-design`
- `stitch-upload-to-stitch`
- `spreadsheet-formula-helper`

The Stitch import keeps `stitch-design` as a router for discoverability and
keeps `stitch-code-to-design` as an end-to-end orchestrator over narrower
extraction, design-system, and upload skills. Do not merge or delete the
following overlapping Stitch workflows without explicit user approval, because
each pair has different inputs, outputs, validation paths, or activation
boundaries: `stitch-design-md` and `stitch-extract-design-md`,
`stitch-generate-design` and `stitch-loop`, `stitch-react-components` and
`stitch-react-native`, `stitch-shadcn-ui` and general React/frontend skills,
and `stitch-taste-design` and general premium UI guidance.

No tracked imports are currently pending provenance. The canonical source, commit or tree digest, source path, and rationale for every source-mapped skill are recorded in `scripts/skill-registry.json` and summarized in [REFERENCE_SOURCES.md](c:\Users\LOQ\.copilot\skills\REFERENCE_SOURCES.md).

The copied official Superpowers are classified separately from maintained imports. The 2026-07-11 refresh flattened the categorized `obra/superpowers-skills` child paths into top-level catalog folders and retained `using-superpowers` as a compatibility entry alongside the current `using-skills` entrypoint.

Additional local-only sourced overlays (currently `58`, primarily `gws-*` and `recipe-*`) are mapped in `scripts/skill-registry.json` and summarized in [REFERENCE_SOURCES.md](c:\Users\LOQ\.copilot\skills\REFERENCE_SOURCES.md).

## Repository Docs

- [CHANGELOG.md](c:\Users\LOQ\.copilot\skills\CHANGELOG.md): repo-wide history
- [CLAUDE.md](c:\Users\LOQ\.copilot\skills\CLAUDE.md): maintenance guidance for Claude-style workflows
- [CONTRIBUTING.md](c:\Users\LOQ\.copilot\skills\CONTRIBUTING.md): contribution workflow, validation, and sync expectations
- [GEMINI.md](c:\Users\LOQ\.copilot\skills\GEMINI.md): Gemini CLI command guidance
- [LESSON.md](c:\Users\LOQ\.copilot\skills\LESSON.md): maintenance lessons and gotchas
- [SECURITY.md](c:\Users\LOQ\.copilot\skills\SECURITY.md): vulnerability reporting and sensitive-disclosure guidance
