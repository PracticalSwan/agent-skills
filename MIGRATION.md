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

Legacy external mirror directories are no longer managed by this repository.
They are not deleted automatically because they may contain user-managed
material.

## Rollback

To restore the prior support model, revert the version 2.0 catalog commit,
restore the former exporter and five-root sync policy from Git history, run
the restored validation/export workflow, and resync the restored destinations.
Do not mix a version 1.3 sync script with version 2.0 skill metadata.
