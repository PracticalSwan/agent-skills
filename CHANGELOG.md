# Changelog

All notable changes to the Copilot Skills repository will be documented in this
file.

## [2026-03-28] - Cross-Client Sync and Lessons

### Added

- Added `LESSON.md` to capture maintenance lessons and recurring mistakes for
  the shared skill catalog
- Added `scripts/sync-skills.ps1` to sync maintained skills from the workspace
  to Codex and Claude target folders while keeping Codex superpowers in their
  nested `superpowers/` location

### Changed

- Updated `README.md` with the correct `38` maintained-skill count, current
  sync workflow, and the explicit source-of-truth policy for this workspace
- Updated `CLAUDE.md` to document Codex versus Claude sync targets, repo-wide
  lesson tracking, and the maintained skill structure in clean ASCII

### Fixed

- Removed the stale `nestjs` entry from the maintained skill catalog
- Removed mojibake from the root documentation set by normalizing headings and
  structure examples to ASCII

## [2026-03-10] - nextjs-development Skill Added

### Added

- New `nextjs-development` maintained skill folder covering Next.js 15/16
  (v16.1.6)
- `SKILL.md` with 12 parts: App Router routing, Server/Client Components,
  `use cache` directive, `cacheTag()` and `cacheLife()`, Server Actions,
  `<Form>` component, `after()`, `connection()`, Turbopack, metadata API,
  auth interrupts (`forbidden()` and `unauthorized()`), and upgrade codemods
- Async Request APIs section covering the v15 breaking change for `params`,
  `searchParams`, `cookies()`, and `headers()`
- Next.js MCP dev tools coverage (`next-devtools-mcp`) with `.mcp.json` setup,
  all 5 runtime tool descriptions, and example agent prompts
- `references/app-router-reference.md`: complete file conventions table,
  dynamic routes, route groups, parallel routes, intercepting routes, and OG
  image generation
- `references/nextjs-mcp-server.md`: full `next-devtools-mcp` setup guide and
  troubleshooting
- `examples/data-fetching-patterns.md`: 8 patterns from `use cache` to SWR
  with TypeScript
- `examples/server-client-components.md`: RSC/RCC decision guide and 9
  composition patterns
- `scripts/page-generator.ps1`: scaffold `page.tsx`, `loading.tsx`,
  `error.tsx` for any route, with automatic handling of dynamic segment params
- `CHANGELOG.md` and `LICENSE.txt` (MIT) for the skill folder

## [2026-03-10] - README MCP Inventory Refresh

### Changed

- Rewrote `README.md` in clean ASCII to remove the visible encoding corruption
  in the structure examples and formatting blocks
- Added a complete maintained-skill catalog so the README now covers all
  editable skills instead of a partial subset
- Added a verified MCP server inventory with current sources for Serena,
  Context7, Notion, Microsoft Learn Docs, Playwright, Power BI, Microsoft
  Agent 365 Office preview, and NotebookLM
- Added a per-skill MCP map to show which maintained skills are MCP-backed,
  host-specific, client-specific, or fully local

### Tested

- Verified the new README content after the rewrite and reviewed the diff for
  formatting regressions

## [2026-03-09] - Custom Agent Discovery Alignment

### Changed

- Updated the `custom-agent-usage` skill, examples, and helper script to use
  the real custom-agent discovery directories on this machine:
  `C:\Users\LOQ\.claude\agents` and
  `C:\Users\LOQ\AppData\Roaming\Code - Insiders\User\prompts`
- Added repo-level guidance that the VS Code Insiders prompts folder contains
  mixed prompt file types and must be filtered to `*.agent.md` for subagent
  discovery

### Fixed

- Removed stale custom-agent discovery references to legacy
  `.copilot/agents` and `.github/copilot/agents` locations
- Removed the external `glob` dependency from
  `custom-agent-usage/scripts/agent-finder.js` so the helper runs in the
  current local Node environment

## [2026-03-09] - Workspace Skill Modernization

### Changed

- Modernized editable skill folders to align with the maintained structure of
  `SKILL.md`, `scripts/`, and `references/`
- Removed duplicated `## Related Skills` sections across the editable skill
  set
- Rewrote outdated MCP-heavy skills to reflect current 2026 behavior,
  especially for Notion, Microsoft Learn, NotebookLM, Power BI, and
  Office-document workflows
- Updated `README.md` to reflect the real workspace layout, current counts,
  loading order, and MCP guidance

### Added

- New runnable helper scripts for skills that previously had references only:
  - `breaking-changes-management/scripts/migration-guide-scaffold.py`
  - `code-examples-sync/scripts/example-sync-check.py`
  - `documentation-automation/scripts/docs-pipeline-scaffold.py`
  - `documentation-patterns/scripts/doc-template-picker.py`
  - `documentation-quality/scripts/doc-style-audit.py`
  - `documentation-verification/scripts/doc-link-check.py`
  - `web-design-reviewer/scripts/css-risk-audit.py`
- New current-reference notes:
  - `microsoft-development/references/microsoft-learn-mcp.md`
  - `notion-docs/references/notion-mcp-quickstart.md`
  - `notebooklm-management/scripts/README.md`
- Backfilled `CHANGELOG.md` into every editable skill folder and added a dated
  `2026-03-09` entry for each skill
- Normalized per-skill changelog headings so only `Added`, `Changed`, `Fixed`,
  and `Tested` are used

### Fixed

- Replaced broken PowerShell automation in:
  - `azure-integrations/scripts/deploy-appservice.ps1`
  - `microsoft-development/scripts/azure-health-check.ps1`
- Removed stale references to old global skill paths and legacy repo
  structure assumptions

## [2026-03-01] - Activation Testing and Fixes

### Fixed

- `javascript-development`: Added `TypeScript` to the description so
  TypeScript prompts without React context activate the right skill
- `frontend-design`: Added generic `CSS`, `wireframes`, and `writing CSS`
  keywords
- `web-testing`: Added `unit tests` to the description
- `web-design-reviewer`: Added clearer disambiguation against automated E2E
  testing

### Tested

- Ran 90+ activation test scenarios across 12 groups covering all 37
  non-superpower skills at the time
- Tested keyword matching against diverse prompt patterns
- Confirmed a small set of acceptable context-dependent overlaps

## [2026-02-28] - Description Rewrite and Cross-References

### Changed

- Rewrote all 37 non-superpower skill descriptions to concise
  activation-focused language
- Reduced overlap between related skills, especially JS vs React, DevOps vs
  Workflow, and the documentation skill cluster

### Added

- Added `## Related Skills` cross-reference tables across the editable skill
  set
