<div align="center">

# Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills Count](https://img.shields.io/badge/Skills-52-blue.svg)](README.md)

A maintained skill catalog for GitHub Copilot, Codex, and Claude-style agents. Each skill combines a focused workflow, current references, and runnable helpers.

</div>

## Overview

This workspace currently contains:

- `52` total skills
- `38` editable domain skills maintained here
- `14` copied Claude Code official superpowers kept for local discovery and intentionally left unchanged

The current maintenance standard is pragmatic:

- concise `SKILL.md` files
- separate `references/` for larger notes
- separate `scripts/` for runnable helpers
- real MCP guidance where public or verifiable
- explicit fallback paths when a host-specific MCP surface is unavailable

## Skill Structure

Every maintained skill should follow this shape:

```text
skill-name/
├── SKILL.md
├── scripts/
│   └── useful-helper.py
└── references/
    └── reference-notes.md
```

Optional additions:

- `examples/` for realistic walkthroughs
- `LICENSE.txt`
- `CHANGELOG.md`

## Loading Order

Skills are resolved in this order:

1. Workspace skills from `.github/skills/`
2. Global fallback skills from `C:/Users/LOQ/.agents/skills/`

Workspace skills take precedence when names collide.

## MCP Guidance

The repo now distinguishes between:

### Publicly documented or directly verifiable MCP servers

- Notion MCP
- Microsoft Learn Docs MCP
- NotebookLM MCP
- Serena MCP
- Playwright MCP
- Context7 MCP

### Host-specific MCP surfaces

Some Office and Power BI workflows depend on tools exposed by a particular host such as GitHub Copilot or Microsoft 365 tooling. Those skills document that reality directly and include local fallback scripts instead of assuming the same tool names exist everywhere.

## Skill Categories

### Frontend and UX

- `frontend-design`
- `react-development`
- `vite-development`
- `web-design-reviewer`
- `web-testing`
- `stitch-design`

### Backend and Data

- `nestjs`
- `php-development`
- `mongodb-mongoose`
- `sql-development`
- `powerbi-modeling`

### Microsoft and Azure

- `microsoft-development`
- `azure-integrations`
- `excel-sheet`
- `word-document`
- `powerpoint-ppt`

### Documentation and Delivery

- `documentation-authoring`
- `documentation-automation`
- `documentation-patterns`
- `documentation-quality`
- `documentation-verification`
- `code-examples-sync`
- `breaking-changes-management`

### Agent and Research Workflows

- `serena-usage`
- `notion-docs`
- `notebooklm-management`
- `codexer`
- `agent-task-mapping`
- `custom-agent-usage`
- `subagent-delegation`

### Specialized

- `canvas-design`
- `legacy-circuit-mockups`
- `infostealer-malware-detector`
- `excalidraw-diagram-generator`

## Working With the Repo

### Editing Skills

When updating a skill:

1. Keep `SKILL.md` focused on activation conditions, workflow, and local links.
2. Move large or slow-changing material into `references/`.
3. Keep helper automation in `scripts/`.
4. Update repo docs if visible behavior or repo structure changes.

### Validation Expectations

Use the checks that match the files you touched:

- Python scripts: `python -m py_compile`
- JavaScript files: `node --check`
- PowerShell files: parse validation
- Markdown files: local link checks and spot review

Generated test artifacts such as `__pycache__` should not remain in the workspace.

## Notable Recent Improvements

The latest modernization pass focused on:

- deduplicating repeated `## Related Skills` sections
- adding missing `scripts/` directories and working helpers
- rewriting stale MCP-heavy skills around current 2026 behavior
- replacing broken PowerShell scripts with valid ASCII versions
- updating the repo structure and usage docs to match the actual workspace

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for the detailed history.
