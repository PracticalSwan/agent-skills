# Changelog

All notable changes to the Copilot Skills repository will be documented in this
file.

## [2026-04-24] - Validation Scope Fix, Provenance Alignment, and Full Sync

### Changed

- Updated `scripts/validate-skills.py` to ignore local environment folders (`.venv`, `venv`, `env`) and cache folders when scanning for stray `*.pyc` files, preventing false positives from local toolchains.
- Updated `README.md` and `CLAUDE.md` to show both git-tracked catalog counts and live local workspace counts, removing inventory ambiguity.
- Updated `GEMINI.md` to clarify that Gemini export and validation include all local `SKILL.md` folders, including local-only overlays.
- Reworked `REFERENCE_SOURCES.md` to align with `scripts/skill-registry.json`, including the `googleworkspace_cli` source commit and tracked-versus-local provenance coverage.
- Added new maintenance guidance in `LESSON.md` for dual inventory reporting and validator exclusion scope.

### Tested

- Ran `C:/Users/LOQ/AppData/Local/Python/pythoncore-3.14-64/python.exe scripts/export-gemini-skill.py --all`.
- Ran `C:/Users/LOQ/AppData/Local/Python/pythoncore-3.14-64/python.exe scripts/validate-skills.py` and confirmed `status: ok` with `125` skills and `125` Gemini commands.
- Ran `powershell -ExecutionPolicy Bypass -File .\scripts\sync-skills.ps1 -WorkspaceSearchRoot "C:\Assumption University"`.
- Verified downstream target inventories after sync:
  - `C:\Users\LOQ\.agents\skills`: `111` skills with `SKILL.md`
  - `C:\Users\LOQ\.claude\skills`: `111` skills with `SKILL.md`
  - `C:\Users\LOQ\.gemini\antigravity\global_skills`: `125` skills with `SKILL.md`
  - `C:\Users\LOQ\.agents\skills\superpowers`: `14` skills with `SKILL.md`

## [2026-04-24] - Skill Imports and Source Refresh

### Added

- Imported `avoid-ai-writing` from `https://github.com/conorbronsdon/avoid-ai-writing`.
- Imported `codebase-to-course` from `https://github.com/zarazhangrui/codebase-to-course` with its course-generation reference assets.
- Added provenance records and per-skill changelogs for both new maintained skills.

### Changed

- Updated public inventory counts to `67` tracked skill folders and `53` maintained skills.
- Refreshed upstream provenance for audited source repos in `scripts/skill-registry.json` and `REFERENCE_SOURCES.md`.
- Applied the current upstream `premium-frontend-ui` author metadata and Anthropic `mcp-builder` license notice.

### Tested

- Rechecked registered upstream source paths against current GitHub heads before applying updates.
- Planned Gemini export, structural validation, downstream sync, and scoped secret review for this catalog refresh.

## [2026-04-04] - Public Docs Cleanup for Ignored Local-Only Skills

### Changed

- Removed ignored local-only skill families from the public inventory, provenance notes, and lessons.
- Restored the tracked documentation counts to `65` total skill folders and `51` maintained skills.

### Tested

- Recomputed the tracked catalog counts by excluding ignored local-only skill folders from the public inventory.

## [2026-04-04] - Curated Skill Imports, AGENTS Upgrade, and Full Sync Refresh

### Added

- Imported and maintained these new skills after researching the reference catalogs in parallel:
  - `agentic-eval`
  - `cloud-design-patterns`
  - `context-map`
  - `mcp-builder`
  - `secret-scanning`
- Added local helper scripts so the imported skills are useful even without host-specific MCP or plugin support:
  - `agentic-eval/scripts/rubric-scorecard.py`
  - `cloud-design-patterns/scripts/pattern-shortlist.py`
  - `context-map/scripts/build-context-map.py`
  - `secret-scanning/scripts/precommit-secret-audit.py`
- Added per-skill changelogs for all newly maintained imports

### Changed

- Updated root documentation for the new `65` total skill / `51` maintained skill inventory
- Extended provenance tracking to record canonical upstream sources separately from discovery catalogs when the discovery repo was not the best maintained origin
- Rewrote the top-level imported skill instructions into the repo house style while preserving upstream references and helper assets where they added value
- Strengthened the global Codex `AGENTS.md` guidance to require safer skill import screening, canonical-source preference, import smoke tests, and repo-wide sync discipline

### Tested

- Smoke-tested the new helper scripts:
  - `python context-map/scripts/build-context-map.py --root . --query sync-skills --query codex --limit 5`
  - `python agentic-eval/scripts/rubric-scorecard.py --rubric agentic-eval/references/rubric-template.json --scores agentic-eval/references/example-scores.json --threshold 0.8`
  - `python secret-scanning/scripts/precommit-secret-audit.py --path secret-scanning/scripts`
  - `python cloud-design-patterns/scripts/pattern-shortlist.py --concern reliability --concern migration --concern security`
  - `python -m py_compile mcp-builder/scripts/connections.py mcp-builder/scripts/evaluation.py`
- Planned repo-wide validation, Gemini export, downstream sync, and sensitive-data review after the documentation and AGENTS updates

## [2026-04-04] - Main Workspace Policy Clarification

### Changed

- Clarified in root documentation that `C:\Users\LOQ\.copilot\skills` is the canonical main workspace for maintained skills and that new maintained skills must be added here first
- Documented downstream skill roots as synced branch mirrors rather than authoring locations
- Updated maintenance guidance so external skill imports are recorded and reviewed in this repo before outward sync

## [2026-04-04] - Codex Path Alignment and Sync Refresh

### Changed

- Realigned `scripts/sync-skills.ps1` so maintained skills now target `C:\Users\LOQ\.codex\skills` for Codex while keeping `C:\Users\LOQ\.agents\skills` as a shared mirror
- Updated root documentation to distinguish the primary Codex install root from the shared mirror path instead of treating them as the same destination
- Refreshed installed Codex skills from the current workspace catalog before the full sync pass

### Fixed

- Removed the stale assumption that `C:\Users\LOQ\.agents\skills` was the only Codex sync target

## [2026-04-04] - Gemini Antigravity Sync and Cleanup

### Changed

- Added `C:\Users\LOQ\.gemini\antigravity\global_skills` as a first-class sync target in `scripts/sync-skills.ps1`
- Updated root documentation to describe Gemini Antigravity global-skill syncing alongside generated Gemini CLI commands
- Refined high-impact meta-skill wording in `using-superpowers`, `writing-skills`, and `nextjs-development` so they read more cleanly across clients instead of assuming only Claude or Codex paths

### Fixed

- Removed the accidental `GEMINI.md` ignore rule from `.gitignore` so the Gemini-specific documentation can be tracked with the repo

### Tested

- Ran `powershell -ExecutionPolicy Bypass -File .\scripts\sync-skills.ps1 -WorkspaceSearchRoot "C:\Assumption University"` after adding the Gemini target
- Verified the Gemini Antigravity root now mirrors the current full skill catalog in `C:\Users\LOQ\.gemini\antigravity\global_skills`

## [2026-04-04] - Four-Client Portability and Workspace Skill Expansion

### Added

- Added `scripts/skill-registry.json` to track MCP-backed skills, no-MCP fallback guidance, reference sources, and imported-skill provenance
- Added `scripts/export-gemini-skill.py` to generate Gemini CLI `/skills:<skill-name>` commands from repo `SKILL.md` files
- Added `scripts/modernize-skills.py` to inject the standard cross-client portability section and MCP fallback section across skills
- Added `scripts/validate-skills.py` to verify skill frontmatter, required sections, and generated Gemini command validity
- Added [GEMINI.md](c:\Users\LOQ\.copilot\skills\GEMINI.md) for Gemini CLI usage guidance
- Added [REFERENCE_SOURCES.md](c:\Users\LOQ\.copilot\skills\REFERENCE_SOURCES.md) documenting imported skill sources, commits, and selection rationale
- Imported and maintained these new skills after auditing `C:\Assumption University`:
  - `csharp-xunit`
  - `dotnet-best-practices`
  - `java-docs`
  - `java-junit`
  - `pdf`
  - `premium-frontend-ui`
  - `security-review`
  - `spreadsheet-formula-helper`

### Changed

- Updated every skill folder so the current catalog works across GitHub Copilot, Claude Code, Codex, and Gemini CLI instead of assuming a single host
- Added explicit no-MCP fallback guidance to MCP-aware skills so the workflows stay usable even when a client lacks the preferred MCP server
- Rewrote root docs for the new `60` total skill / `46` maintained skill inventory and the four-client support model
- Extended `scripts/sync-skills.ps1` to discover workspace-local skill roots under `.agent\skills`, `.agents\skills`, and `.claude\skills`
- Fixed `scripts/sync-skills.ps1` summary handling so source inventory and discovered workspace targets are tracked separately
- Reworked Gemini command export to use TOML-safe escaped strings instead of fragile raw multiline embedding
- Normalized imported skill descriptions and wording where they still assumed Copilot-only or host-specific placeholders

### Tested

- Ran `python scripts/export-gemini-skill.py --all`
- Ran `python scripts/validate-skills.py` and confirmed `60` skills plus `60` Gemini commands
- Syntax-checked repo Python helpers with `py_compile`
- Syntax-checked repo JavaScript helpers with `node --check`
- Syntax-checked repo PowerShell helpers with PowerShell's parser API
- Ran `powershell -ExecutionPolicy Bypass -File .\scripts\sync-skills.ps1 -WorkspaceSearchRoot "C:\Assumption University"`
- Verified synced copies in:
  - `C:\Users\LOQ\.agents\skills`
  - `C:\Users\LOQ\.claude\skills`
  - `C:\Assumption University\Finished\CSX4107\Assignments\.agent\skills`
  - `C:\Assumption University\Finished\ITX2007\Assignments\.agent\skills`
  - `C:\Assumption University\Workshops\ThreeJS\.agents\skills`
  - `C:\Assumption University\Workshops\ThreeJS\Mini_Hands_On_Cube\.agents\skills`

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
