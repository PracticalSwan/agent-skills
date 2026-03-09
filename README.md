# Agent Skills

Maintained skill catalog for GitHub Copilot, Codex, and Claude-style agents.
Each maintained skill combines a focused workflow, current references,
and runnable helpers.

## Scope

- `53` total skill directories in this workspace
- `39` maintained skill folders in this repo
- `14` copied Claude Code official superpowers kept for local discovery
  and intentionally left unchanged

## Maintained Skill Structure

```text
skill-name/
|- SKILL.md
|- CHANGELOG.md
|- references/
|  `- notes.md
|- scripts/
|  `- helper.py
`- examples/
   `- example.md
```

Required:
- `SKILL.md`
- `CHANGELOG.md`
- `references/`
- `scripts/`

Optional:
- `examples/`
- `LICENSE.txt`

## Loading Order

1. Workspace skills from `.github/skills/`
2. Global fallback skills from `C:/Users/LOQ/.agents/skills/`

Workspace skills win on name collisions.

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
- `react-development`
- `stitch-design`
- `vite-development`
- `web-design-reviewer`
- `web-testing`

### Backend and Data

- `javascript-development`
- `mongodb-mongoose`
- `nestjs`
- `php-development`
- `powerbi-modeling`
- `sql-development`

### Microsoft and Office

- `azure-integrations`
- `excel-sheet`
- `microsoft-development`
- `powerpoint-ppt`
- `word-document`

### Agent and Research

- `agent-task-mapping`
- `codexer`
- `custom-agent-usage`
- `notebooklm-management`
- `notion-docs`
- `serena-usage`
- `subagent-delegation`

### Specialized

- `infostealer-malware-detector`

## MCP Coverage

This repo currently has `16` maintained skills that are MCP-backed or
MCP-aware. The remaining maintained skills are local guidance, CLI workflows,
or script-first utilities.

Status legend:
- `Primary`: the skill is designed around that MCP server
- `Optional`: the MCP server enhances the skill but is not required
- `None`: no MCP server is required for normal use

## Verified MCP Servers

Validated on `2026-03-10` using available tool surfaces and official
documentation where public sources exist.

| Server | What it covers | Sources |
|--------|----------------|---------|
| Serena MCP | Activation, memories, symbol search, refactors | [1] |
| Context7 MCP | Resolve library IDs and query package docs | [2] |
| Notion MCP | Search, read, update pages and databases | [3], [4] |
| Microsoft Learn Docs MCP | Search Microsoft and Azure documentation | [5] |
| Playwright MCP | Browser navigation, snapshots, actions, screenshots | [6] |
| Power BI MCP | Manage model tables, measures, DAX, and relationships | [7] |
| Word Document MCP | Word document read, edit, format, and export | [8] |
| Excel MCP | Workbook, worksheet, and chart manipulation | [9] |
| PowerPoint MCP | Presentation creation, editing, and template management | [10] |
| NotebookLM MCP | Notebook research and session management | [11] |
| Stitch MCP | Screen generation, project management, variant creation | [12] |
| MongoDB MCP | Database queries, schema inspection, and aggregation | [13] |
| Azure MCP | Azure resource management, deployment, and queries | [14] |
| GitHub MCP | Repository, issues, PRs, commits, and branch management | [15] |
| Next.js MCP (next-devtools-mcp) | Live dev server errors, logs, routes, Server Actions, project metadata | [16] |

Notes:
- NotebookLM MCP is community-provided via jgravelle/NotebookLM-MCP-Server.
  Validate that the server is installed before use.
- Stitch MCP is environment-provided by Google. No separate installation is
  needed when the MCP surface is already active in your client.
- Office MCP servers (Word, Excel, PowerPoint) are installed as separate PyPI
  packages via `uvx` and expose independent tool namespaces per application.

## Per-Skill MCP Map

### Workflow and Delivery

| Skill | MCP | Notes |
|-------|-----|-------|
| `breaking-changes-management` | `None` | Local semver, deprecation, and migration guidance |
| `code-examples-sync` | `None` | Local doc and snippet sync checks |
| `code-quality` | `None` | Local review and refactor guidance; use `serena-usage` if available |
| `development-workflow` | `None` | Specs, plans, and contribution workflows are local |
| `devops-tooling` | `Optional: GitHub MCP` | Core workflow is local; GitHub MCP available for repository and PR operations |
| `documentation-authoring` | `None` | Source documentation creation does not require MCP |
| `documentation-automation` | `None` | Linters and doc pipelines are local toolchain work |
| `documentation-patterns` | `None` | Templates and structure patterns are local |
| `documentation-quality` | `None` | Style and readability checks are local |
| `documentation-verification` | `None` | Local completeness, links, and example validation |

### Frontend, Design, and Testing

| Skill | MCP | Notes |
|-------|-----|-------|
| `canvas-design` | `None` | Design philosophy and canvas docs are local |
| `excalidraw-diagram-generator` | `None` | Uses local diagram helpers, not MCP |
| `frontend-design` | `None` | Layout, accessibility, and CSS guidance is local |
| `legacy-circuit-mockups` | `None` | HTML5 Canvas and local assets only |
| `nextjs-development` | `Optional: Next.js MCP` | Core patterns are local; `next-devtools-mcp` adds live error, log, and runtime queries |
| `react-development` | `None` | React guidance does not require MCP |
| `stitch-design` | `Primary: Stitch MCP` | Available when Stitch MCP is configured in the client |
| `vite-development` | `None` | Vite configuration and build work is local |
| `web-design-reviewer` | `Primary: Playwright MCP, optional Chrome MCP` | Best when browser snapshot and screenshot tools are available |
| `web-testing` | `Primary: Playwright MCP, optional Chrome MCP` | Playwright CLI remains a valid fallback |

### Backend and Data

| Skill | MCP | Notes |
|-------|-----|-------|
| `javascript-development` | `None` | JS and TS implementation guidance is local |
| `mongodb-mongoose` | `Primary: MongoDB MCP` | Use for queries, schema inspection, stats, and aggregation |
| `nestjs` | `None` | Framework guidance is local |
| `php-development` | `None` | PHP and PDO guidance is local |
| `powerbi-modeling` | `Primary: Power BI MCP` | Full model surface confirmed; use local audit script as fallback |
| `sql-development` | `None` | Pair with `microsoft-development` for Microsoft docs lookup |

### Microsoft and Office

| Skill | MCP | Notes |
|-------|-----|-------|
| `azure-integrations` | `Primary: Azure MCP` | Use for deploying, managing, and querying Azure resources |
| `excel-sheet` | `Primary: Excel MCP` | Confirmed via mcp_excel_* tool surface |
| `microsoft-development` | `Primary: Microsoft Learn Docs MCP` | Official Microsoft docs and code sample retrieval |
| `powerpoint-ppt` | `Primary: PowerPoint MCP` | Confirmed via mcp_ppt_* tool surface |
| `word-document` | `Primary: Word Document MCP` | Confirmed via mcp_word-document_* tool surface |

### Agent and Research

| Skill | MCP | Notes |
|-------|-----|-------|
| `agent-task-mapping` | `None` | Maps work to local custom agents rather than MCP servers |
| `codexer` | `Primary: Context7 MCP` | Resolve library IDs and query current package docs |
| `custom-agent-usage` | `None` | Discovers local `.agent.md` files, not MCP servers |
| `notebooklm-management` | `Primary: NotebookLM MCP` | Community or environment-provided; validate locally |
| `notion-docs` | `Primary: Notion MCP` | Supports remote endpoint or local stdio package |
| `serena-usage` | `Primary: Serena MCP` | Project memories, symbol navigation, and refactoring |
| `subagent-delegation` | `None` | Delegation workflow only |

### Specialized

| Skill | MCP | Notes |
|-------|-----|-------|
| `infostealer-malware-detector` | `None` | Detection guidance and local scripts only |

## Non-MCP Notes

- `custom-agent-usage` is not MCP-based. It discovers local custom agents from:
  - `C:\Users\LOQ\.claude\agents`
  - `C:\Users\LOQ\AppData\Roaming\Code - Insiders\User\prompts`
- In the VS Code Insiders prompts directory, only `*.agent.md` files count as
  subagent definitions.

## MCP Sources

1. [Serena MCP](https://github.com/oraios/serena)
2. [Context7](https://context7.com/)
3. [Notion MCP Quickstart](https://developers.notion.com/docs/get-started-with-mcp)
4. [makenotion/notion-mcp-server](https://github.com/makenotion/notion-mcp-server)
5. [Microsoft Learn Docs MCP](https://github.com/MicrosoftDocs/mcp)
6. [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)
7. [Power BI MCP (Docker Desktop)](https://docs.docker.com/ai/mcp-catalog-and-toolkit/)
8. [office-word-mcp-server](https://pypi.org/project/office-word-mcp-server/)
9. [excel-mcp-server](https://pypi.org/project/excel-mcp-server/)
10. [office-powerpoint-mcp-server](https://pypi.org/project/office-powerpoint-mcp-server/)
11. [NotebookLM MCP Server](https://github.com/jgravelle/NotebookLM-MCP-Server)
12. [Stitch by Google](https://stitch.withgoogle.com/)
13. [MongoDB MCP](https://www.mongodb.com/products/tools/mcp)
14. [Azure MCP Server](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/)
15. [GitHub MCP Server](https://github.com/github/github-mcp-server)
16. [next-devtools-mcp](https://github.com/vercel/next-devtools-mcp)

## Copied Official Superpowers

These `14` directories are copied for local discovery and are intentionally not
maintained here:

- `brainstorming`
- `dispatching-parallel-agents`
- `executing-plans`
- `finishing-a-development-branch`
- `receiving-code-review`
- `requesting-code-review`
- `subagent-driven-development`
- `systematic-debugging`
- `test-driven-development`
- `using-git-worktrees`
- `using-superpowers`
- `verification-before-completion`
- `writing-plans`
- `writing-skills`

They are excluded from the per-skill MCP map above because this repo does not
maintain their server requirements.

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for repository history.
