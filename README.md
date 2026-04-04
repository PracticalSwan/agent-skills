# Agent Skills

Shared skill catalog for GitHub Copilot, Claude Code, Codex, and Gemini CLI.

This workspace is the main branch for maintained skills, cross-client portability guidance, Gemini command generation, and MCP fallback rules.
Install or import new maintained skills here first, then sync them outward to the downstream targets.

## Current Inventory

- `60` total skill folders in this workspace
- `46` maintained skills in this repo
- `14` copied official Claude/Codex-style superpowers tracked locally for discovery and sync
- Every skill now includes:
  - a cross-client portability section
  - an MCP section that names the preferred server and a no-MCP fallback path

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
2. Update `REFERENCE_SOURCES.md` if the skill came from an external source
3. Update the touched changelogs and root docs
4. Validate and export
5. Sync outward from this repo

Validate all skills and generated Gemini commands:

```powershell
python scripts/validate-skills.py
```

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

## Workspace-Aware Sync

The sync script can now discover and update local project skill folders under a workspace root when they live under:

- `.agent\skills`
- `.agents\skills`
- `.claude\skills`

That allows one pass from this repo into your Codex root, shared mirror root, and project-local skill roots inside `C:\Assumption University`.

## Maintained Skill Catalog

### Workflow and Delivery

- `breaking-changes-management`
- `code-examples-sync`
- `code-quality`
- `development-workflow`
- `devops-tooling`
- `documentation-authoring`
- `documentation-automation`
- `documentation-patterns`
- `documentation-quality`
- `documentation-verification`

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
- `mongodb-mongoose`
- `php-development`
- `powerbi-modeling`
- `sql-development`

### Microsoft, Documents, and Office

- `azure-integrations`
- `excel-sheet`
- `microsoft-development`
- `pdf`
- `powerpoint-ppt`
- `spreadsheet-formula-helper`
- `word-document`

### Agent and Research

- `agent-task-mapping`
- `codexer`
- `custom-agent-usage`
- `notebooklm-management`
- `notion-docs`
- `serena-usage`
- `subagent-delegation`

### Security and Specialized

- `infostealer-malware-detector`
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
- `serena-usage`
- `stitch-design`
- `web-design-reviewer`
- `web-testing`
- `word-document`

The registry for MCP mappings and no-MCP fallback guidance is stored in [scripts/skill-registry.json](c:\Users\LOQ\.copilot\skills\scripts\skill-registry.json).

## Reference Skill Installs

The following high-quality skills were added after auditing the wider `C:\Assumption University` workspace and matching them to real project needs:

- `csharp-xunit`
- `dotnet-best-practices`
- `java-docs`
- `java-junit`
- `pdf`
- `premium-frontend-ui`
- `security-review`
- `spreadsheet-formula-helper`

Reference provenance, source commits, and selection reasons are documented in [REFERENCE_SOURCES.md](c:\Users\LOQ\.copilot\skills\REFERENCE_SOURCES.md).

## Repository Docs

- [CHANGELOG.md](c:\Users\LOQ\.copilot\skills\CHANGELOG.md): repo-wide history
- [CLAUDE.md](c:\Users\LOQ\.copilot\skills\CLAUDE.md): maintenance guidance for Claude-style workflows
- [GEMINI.md](c:\Users\LOQ\.copilot\skills\GEMINI.md): Gemini CLI command guidance
- [LESSON.md](c:\Users\LOQ\.copilot\skills\LESSON.md): maintenance lessons and gotchas
