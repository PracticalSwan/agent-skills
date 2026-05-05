# Reference Sources

This document summarizes external source provenance for skills in this workspace.
The canonical per-skill mapping is `scripts/skill-registry.json` under `reference_installs`.

## Snapshot (2026-05-05)

- `73` skills have external source mappings.
- `15` source-mapped skills are git-tracked in this repository.
- `58` source-mapped skills are local-only overlays (`gws-*` and `recipe-*` families).
- `4` tracked imports are currently present without finalized source mappings (`docx`, `jupyter-notebook`, `pptx`, `xlsx`).
- `0` source mappings point to missing local skill folders.
- `0` source mappings are missing required fields (`source_repo`, `source_commit`, `source_path`).

## Source Catalogs

- `https://github.com/github/awesome-copilot`
- `https://awesome-copilot.github.com/skills`
- `https://github.com/travisvn/awesome-claude-skills`
- `https://github.com/ComposioHQ/awesome-codex-skills`
- `https://github.com/anthropics/skills`
- `https://github.com/googleworkspace/cli`
- `https://github.com/conorbronsdon/avoid-ai-writing`
- `https://github.com/zarazhangrui/codebase-to-course`

## Source Commits

| Source | Commit |
|--------|--------|
| `awesome_copilot` | `63d08d51f792d53feec8c1c06897cee870e83c18` |
| `awesome_claude_skills` | `b05169af5448a3d8961aa0ed12c2934f94bfe52e` |
| `anthropic_skills` | `5128e1865d670f5d6c9cef000e6dfc4e951fb5b9` |
| `awesome_codex_skills` | `711ee69d724457093d52f685d729917f5389c686` |
| `googleworkspace_cli` | `a3768d0e82ad83cca2da97724e46bea4ff0e6dbd` |
| `avoid_ai_writing` | `cbf885e087e8ec1168bc58dc603606a6e4bfacbd` |
| `codebase_to_course` | `ff8837ecf8e9f6ce9874ffa42e42633394a52a00` |

## Tracked Reference Installs

These source-mapped skills are currently tracked in git in this repository.

| Skill | Source Repo | Source Commit | Source Path |
|-------|-------------|---------------|-------------|
| `agentic-eval` | `https://github.com/github/awesome-copilot` | `63d08d51f792d53feec8c1c06897cee870e83c18` | `skills/agentic-eval` |
| `avoid-ai-writing` | `https://github.com/conorbronsdon/avoid-ai-writing` | `cbf885e087e8ec1168bc58dc603606a6e4bfacbd` | `.` |
| `cloud-design-patterns` | `https://github.com/github/awesome-copilot` | `63d08d51f792d53feec8c1c06897cee870e83c18` | `skills/cloud-design-patterns` |
| `codebase-to-course` | `https://github.com/zarazhangrui/codebase-to-course` | `ff8837ecf8e9f6ce9874ffa42e42633394a52a00` | `.` |
| `context-map` | `https://github.com/github/awesome-copilot` | `63d08d51f792d53feec8c1c06897cee870e83c18` | `skills/context-map` |
| `csharp-xunit` | `https://github.com/github/awesome-copilot` | `63d08d51f792d53feec8c1c06897cee870e83c18` | `skills/csharp-xunit` |
| `dotnet-best-practices` | `https://github.com/github/awesome-copilot` | `63d08d51f792d53feec8c1c06897cee870e83c18` | `skills/dotnet-best-practices` |
| `java-docs` | `https://github.com/github/awesome-copilot` | `63d08d51f792d53feec8c1c06897cee870e83c18` | `skills/java-docs` |
| `java-junit` | `https://github.com/github/awesome-copilot` | `63d08d51f792d53feec8c1c06897cee870e83c18` | `skills/java-junit` |
| `mcp-builder` | `https://github.com/anthropics/skills` | `5128e1865d670f5d6c9cef000e6dfc4e951fb5b9` | `skills/mcp-builder` |
| `pdf` | `https://github.com/travisvn/awesome-claude-skills` | `b05169af5448a3d8961aa0ed12c2934f94bfe52e` | `Official skill reference -> anthropics/skills/pdf` |
| `premium-frontend-ui` | `https://github.com/github/awesome-copilot` | `63d08d51f792d53feec8c1c06897cee870e83c18` | `skills/premium-frontend-ui` |
| `secret-scanning` | `https://github.com/github/awesome-copilot` | `63d08d51f792d53feec8c1c06897cee870e83c18` | `skills/secret-scanning` |
| `security-review` | `https://github.com/github/awesome-copilot` | `63d08d51f792d53feec8c1c06897cee870e83c18` | `skills/security-review` |
| `spreadsheet-formula-helper` | `https://github.com/ComposioHQ/awesome-codex-skills` | `711ee69d724457093d52f685d729917f5389c686` | `spreadsheet-formula-helper` |

## Local-Only Overlay Reference Installs

These source-mapped overlays are intentionally local-only in this workspace and not tracked in git:

- `gws-*`: `26` skills sourced from `https://github.com/googleworkspace/cli`.
- `recipe-*`: `32` skills sourced from `https://github.com/googleworkspace/cli`.

Use `scripts/skill-registry.json` for the exact per-skill `source_path`, `source_commit`, and rationale entries.

## Tracked Imports Pending Provenance

These tracked skill folders are present in this repository but do not yet have finalized provenance records in `scripts/skill-registry.json`:

- `docx`
- `jupyter-notebook`
- `pptx`
- `xlsx`

They were synced in from the local Codex install root and still need canonical upstream matching before they should be treated as fully source-mapped maintained imports.

## Selection Notes

- The wider `C:\Assumption University` workspace was inventoried before adding tracked and local-only sourced skills.
- Imported skills are installed into `C:\Users\LOQ\.copilot\skills` first because this repo is the canonical maintained source.
- Discovery lists are useful for finding candidates, but canonical upstream sources win when a discovery repo points to a stronger maintained original.
- Downstream skill folders such as `C:\Users\LOQ\.codex\skills`, `C:\Users\LOQ\.agents\skills`, `C:\Users\LOQ\.claude\skills`, and workspace-local skill roots are synced from this repo after import and review.
- Imported skills are modernized in this repo so they work as shared skills across GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- MCP-aware skills are required to include a no-MCP fallback path before being treated as valid maintained skills.
- New helper scripts are smoke-tested locally before the repo-wide validation and sync pass.
- Unsafe, offensive, credential-heavy, or low-signal skills discovered during research are intentionally excluded from the tracked catalog.
