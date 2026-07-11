---
name: stitch-code-to-design
version: "1.3"
last_updated: 2026-07-11
tags: [stitch, design, frontend, html, migration]
description: "Convert an existing frontend into Stitch-ready design assets by extracting static HTML, writing DESIGN.md, creating the design system, and uploading approved files."
license: "Apache-2.0"
---
# Stitch Code To Design

This skill is a catalog-normalized import from `https://github.com/google-labs-code/stitch-skills` at commit `3f64079d75d025bc5890c73669f27c26a2d80b31`, source path `plugins/stitch-design/skills/code-to-design`. The upstream control file was corrected for this workspace: the verified Stitch MCP surface here is design-system oriented, so screen lookup, screen generation, and screen editing tools must be used only when the current host explicitly exposes them.

## When to Use This Skill

- Use when an existing web app, React view, or static page must be moved into Stitch.
- The task involves Google Stitch project IDs, `.stitch/` artifacts, DESIGN.md files, Stitch exports, or Stitch-specific validation.
- The broader `stitch-design` router points here as the narrowest workflow.

## Workflow

1. Resolve the target app root, route, and intended Stitch project. If the project ID is unknown, require a user-provided Stitch URL/project ID, the Stitch web UI, or a host-listed lookup tool.
2. Run `stitch-extract-static-html` for the relevant route or UI state and keep the output under `.stitch/`.
3. Run `stitch-extract-design-md` against the source tree and save `.stitch/DESIGN.md`.
4. Run `stitch-manage-design-system` to create or update the Stitch design system, using `--generated-by 'stitch::code-to-design'` when the bundled upload helper is needed.
5. Run `stitch-upload-to-stitch` for the static HTML only after the user approves the exact file, size, and destination; identify the producer with `--generated-by 'stitch::extract-static-html'`.
6. Update `.stitch/metadata.json` with project, screen, and design-system identifiers.

## Local Assets

- `examples/`, `resources/`, `references/`, or `reference/` are upstream support material when present. Treat `SKILL.md` as the source of truth if a support file mentions an unavailable MCP tool.
- `scripts/` are optional helpers. On Windows, prefer PowerShell or Node equivalents unless Git Bash or WSL is actually available.
- Keep generated `.stitch/` files out of commits unless the user explicitly wants them as durable examples.

## Corrected Stitch MCP Surface

Verified in this workspace on 2026-06-15: `create_project`, `upload_design_md`, `create_design_system_from_design_md`, `list_design_systems`, and `apply_design_system`. This 2026-07-11 source refresh did not re-verify a broader live MCP surface. Do not claim `list_projects`, `list_screens`, `get_project`, `get_screen`, `generate_screen_from_text`, `edit_screens`, or `generate_variants` were used unless the current host exposes those exact tools in the active tool list.

## Anti-Patterns

- Claiming a Stitch screen-generation, screen-editing, or screen-retrieval MCP call succeeded when the active host does not expose that tool.
- Uploading files, screenshots, HTML, markdown, or design assets to Stitch without user-approved destination and artifact details.
- Reading, printing, storing, or committing Stitch API keys, MCP config secrets, cookies, or credential-bearing files.
- Treating generated design or code as final without local render, syntax, or artifact verification.
- Collapsing this workflow into a broader frontend/design skill when Stitch-specific files, project IDs, or design-system assets matter.

## Verification Protocol

Before claiming this skill was applied successfully:

1. Pass/fail: `.stitch/DESIGN.md` exists and summarizes real source tokens.
2. Pass/fail: The static HTML opens locally enough to inspect core layout and images.
3. Pass/fail: Stitch design-system creation was MCP-verified or the fallback evidence is recorded.
4. Pass/fail: No API key, token, cookie, or credential-bearing config was copied into durable files.
5. Pressure-test scenario: Repeat the workflow with Stitch MCP screen tools unavailable and confirm the fallback path remains honest and actionable.
6. Success metric: The user can identify the exact artifact, project/design-system target, and verification evidence without relying on unstated MCP behavior.

<!-- PORTABILITY:START -->

## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:stitch-code-to-design` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py stitch-code-to-design` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: Stitch MCP

- Fallback prompt: "Use the Stitch Code To Design skill without Stitch MCP. Use local extraction, source-code design-system synthesis, and manual Stitch web UI upload when MCP upload tools are unavailable. Show the exact files, commands, manual Stitch UI steps, and verification evidence used before concluding."
- Verified Stitch MCP tools in this workspace are design-system/project oriented; use broader screen tools only when the current host exposes them.
- Use local scripts, exported HTML/screenshots, the Stitch web UI, and project metadata files as the fallback evidence path.

<!-- MCP:END -->

## Related Skills

- [stitch-extract-static-html](../stitch-extract-static-html/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
- [stitch-extract-design-md](../stitch-extract-design-md/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
- [stitch-manage-design-system](../stitch-manage-design-system/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
- [stitch-upload-to-stitch](../stitch-upload-to-stitch/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
