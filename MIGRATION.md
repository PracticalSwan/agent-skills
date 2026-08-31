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

## 2026-08-17 Codex-Only Blender Overlay

The `arjun988/blender-skills` pack is intentionally outside the shared catalog even though the parent maintenance agent owns its update workflow.

- Install and update it only in `C:\Users\LOQ\.codex\skills`.
- Keep its checkout under `C:\Users\LOQ\.codex\vendor\blender-skills`.
- Never promote its protected skill names into the parent catalog or synchronize them to the shared or Claude roots.
- Use `scripts/update-codex-local-blender-skills.ps1` for upstream refreshes; it owns only the recorded Blender skill names and shared reference folder.
- The generic promotion and sync tooling rejects parent leakage for these names.

## 2026-08-29 Catalog Source Refresh

The catalog was rechecked against all recorded upstream heads and refreshed only
the installed paths that changed. `avoid-ai-writing` is now at detector 3.28.0;
the Gemini workflows include current transcription, Omni video, and embedding
guidance; `react-view-transitions` includes troubleshooting guidance; and the
web-quality workflows include current field-data and agentic-browsing checks.

The current Xquik source removed its MCP setup documents and metadata. The
normalized catalog therefore removes the stale preferred Xquik MCP mapping and
uses the documented REST/SDK fallback. Do not rely on the retired
`mcp-setup.md` or `mcp-tools.md` files in that skill.

## 2026-08-31 Catalog Corpus Refresh

The current `avoid-ai-writing` corpus includes small `docs` and
`conversational` pre-LLM seeds. They improve extraction-path coverage but do
not establish a register-level rate; keep the manifest's under-sampling limits
visible and do not treat the seeds as a publishable benchmark.

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
