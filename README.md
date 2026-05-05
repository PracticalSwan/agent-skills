# Agent Skills

Shared skill catalog for GitHub Copilot, Claude Code, Codex, and Gemini CLI.

This workspace is the main branch for maintained skills, cross-client portability guidance, Gemini command generation, and MCP fallback rules.
Install or import new maintained skills here first, then sync them outward to the downstream targets.

## Current Inventory

Snapshot date: `2026-05-05`. Local overlay totals can differ by machine.

- Git-tracked catalog in this repository:
  - `71` tracked skill folders
  - `57` tracked maintained skills
  - `14` tracked copied official Claude/Codex-style superpowers
- Live local workspace snapshot (includes local-only overlays such as `gws-*` and `recipe-*` when present):
  - `129` local skill folders detected
  - `115` local maintained skills detected
  - `14` local copied official superpowers detected
- Copied official superpowers are identified by the explicit list in `scripts/skill-registry.json`, not by whether a skill folder has a `CHANGELOG.md`
- The normalized catalog baseline includes:
  - catalog frontmatter with `name`, `version`, `last_updated`, `tags`, and `description`
  - a per-skill `CHANGELOG.md`
  - a cross-client portability section
  - an MCP section that names the preferred server and a no-MCP fallback path
  - an `Anti-Patterns` section
  - a `Verification Protocol` section
  - a final `Related Skills` section
- Most tracked maintained skills are currently aligned on `version: "1.2"` with `last_updated: 2026-04-25`
- The tracked imports `docx`, `jupyter-notebook`, `pptx`, and `xlsx` are present in git but still need catalog normalization before they match the full maintained-skill baseline

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
- a final `## Related Skills`
- `CHANGELOG.md` in every skill folder
- new changelog entries with `Added`, `Changed`, and `Fixed` sections only; do not add a `### Tested` section

Catalog policy also expects each `SKILL.md` to include `## Verification Protocol` immediately after `## Anti-Patterns`.

The tracked raw imports `docx`, `jupyter-notebook`, `pptx`, and `xlsx` are the current known exceptions to that full schema baseline until they are modernized in this repo.

For a catalog-wide skill refresh, update the root docs in the same pass, then rerun validation, Gemini export, and downstream sync even if the folder counts did not change.

Regenerate Gemini CLI commands:

```powershell
python scripts/export-gemini-skill.py --all
```

Refresh portability and MCP sections across all skills:

```powershell
python scripts/modernize-skills.py
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

### Architecture and Platform

- `cloud-design-patterns`
- `mcp-builder`

### Frontend, Design, and Testing

- `canvas-design`
- `excalidraw-diagram-generator`
- `frontend-design`
- `legacy-circuit-mockups`
- `nextjs-development`
- `premium-frontend-ui`
- `react-development`
- `stitch-design`
- `vite-development`
- `web-design-reviewer`
- `web-testing`

### Languages, Backend, and Data

- `csharp-xunit`
- `dotnet-best-practices`
- `java-docs`
- `java-junit`
- `javascript-development`
- `jupyter-notebook`
- `mongodb-mongoose`
- `php-development`
- `powerbi-modeling`
- `sql-development`

### Microsoft, Documents, and Office

- `azure-integrations`
- `docx`
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
- `custom-agent-usage`
- `notebooklm-management`
- `notion-docs`
- `serena-usage`
- `subagent-delegation`

### Security and Specialized

- `infostealer-malware-detector`
- `secret-scanning`
- `security-review`

## MCP-Aware Skills

These maintained skills are MCP-backed or MCP-aware in this repo:

- `azure-integrations`
- `codexer`
- `devops-tooling`
- `excel-sheet`
- `microsoft-development`
- `mongodb-mongoose`
- `nextjs-development`
- `notebooklm-management`
- `notion-docs`
- `powerbi-modeling`
- `powerpoint-ppt`
- `secret-scanning`
- `serena-usage`
- `stitch-design`
- `web-design-reviewer`
- `web-testing`
- `word-document`

The registry for MCP mappings and no-MCP fallback guidance is stored in [scripts/skill-registry.json](c:\Users\LOQ\.copilot\skills\scripts\skill-registry.json).

## Reference Skill Imports

The following externally sourced skills are currently tracked and maintained in this repo.

Imported after auditing the wider `C:\Assumption University` workspace and matching them to real project needs:

- `agentic-eval`
- `avoid-ai-writing`
- `cloud-design-patterns`
- `codebase-to-course`
- `context-map`
- `csharp-xunit`
- `dotnet-best-practices`
- `java-docs`
- `java-junit`
- `mcp-builder`
- `pdf`
- `premium-frontend-ui`
- `secret-scanning`
- `security-review`
- `spreadsheet-formula-helper`

Tracked imports currently in git but still pending schema normalization and finalized provenance:

- `docx`
- `jupyter-notebook`
- `pptx`
- `xlsx`

Additional local-only sourced overlays (currently `58`, primarily `gws-*` and `recipe-*`) are mapped in `scripts/skill-registry.json` and summarized in [REFERENCE_SOURCES.md](c:\Users\LOQ\.copilot\skills\REFERENCE_SOURCES.md).

## Repository Docs

- [CHANGELOG.md](c:\Users\LOQ\.copilot\skills\CHANGELOG.md): repo-wide history
- [CLAUDE.md](c:\Users\LOQ\.copilot\skills\CLAUDE.md): maintenance guidance for Claude-style workflows
- [GEMINI.md](c:\Users\LOQ\.copilot\skills\GEMINI.md): Gemini CLI command guidance
- [LESSON.md](c:\Users\LOQ\.copilot\skills\LESSON.md): maintenance lessons and gotchas
