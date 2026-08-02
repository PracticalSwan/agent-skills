# Version 2.0 Client-Support Migration

Catalog version 2.0 is a breaking client-support reset dated `2026-07-29`.

## Old behavior

- The catalog advertised four clients and generated an additional command
  surface.
- The sync script wrote to five personal-global roots.
- Browser-oriented skills could imply that a Chrome integration was portable
  across model providers.

## New behavior

- Supported clients are GitHub Copilot, Claude Code, and Codex.
- Validation operates directly on `SKILL.md`; no generated command export is
  part of maintenance.
- Sync is restricted to:
  - `C:\Users\LOQ\.agents\skills`
  - `C:\Users\LOQ\.codex\skills`
  - `C:\Users\LOQ\.claude\skills`
- Codex-owned `.system` skills remain authoritative and are excluded from
  same-named top-level Codex mirror writes.
- Claude Code sessions using the GLM Coding Plan must use an explicitly
  configured external browser MCP for authenticated browser automation.

## Migration steps

1. Remove any automation that calls the retired command exporter.
2. Run `python scripts/validate-skills.py`.
3. Run
   `powershell -ExecutionPolicy Bypass -File .\scripts\sync-skills.ps1`.
   The sync removes known stale top-level system shadows and copied
   Superpowers that conflict with the new routing, while preserving unknown
   personal skills and Codex `.system`.
4. Restart or reopen Codex and Claude Code when their skill discovery cache
   requires it.
5. For Claude browser workflows, inspect `claude mcp list` and the active tool
   list. Use a healthy external Chrome DevTools, Puppeteer, or Playwright MCP,
   or keep the workflow at a manual handoff.

## 2026-08-02 Frontend Skill Consolidation

The general frontend creation surface now has one canonical skill:
`frontend-design`.

- Removed `frontend-skill`: use `frontend-design`.
- Removed `premium-frontend-ui`: use `frontend-design` and select immersive or
  experimental mode only when the context justifies it.
- Retained `web-design-reviewer` as the separate post-implementation visual QA
  workflow.
- Retained React, Next.js, Vite, JavaScript, web testing, Figma, and Stitch
  skills as specialized workflows.

The existing `#component-review-rubric` anchor remains valid for React,
Next.js, and Vite references. The sync script removes only the two exact
retired catalog folders from the Codex, shared, and Claude roots while
preserving unknown personal skills and Codex `.system` folders.

The consolidated folder preserves the original MIT license, the Apache-2.0
license and modification notice for adapted historical OpenAI material, and
the reviewed Awesome Copilot MIT attribution.

The two verified legacy skill-only mirror trees were removed during the
user-requested cleanup after confirming they were byte-identical, stale,
unreferenced, and unused by running processes. Their surrounding application
state was preserved. Do not delete neighboring client data when cleaning up
retired mirror leaves.

## Rollback

To restore the prior support model, revert the version 2.0 catalog commit,
restore the former exporter and five-root sync policy from Git history, run
the restored validation/export workflow, and resync the restored destinations.
Do not mix a version 1.3 sync script with version 2.0 skill metadata.

To roll back only the frontend consolidation, restore both retired folders and
their registry and active-reference entries from the pre-consolidation commit,
remove them from the exact retired-name cleanup list, validate the whole
catalog, and resync all three approved roots. Do not restore only the links;
that would leave broken activation and licensing state.
