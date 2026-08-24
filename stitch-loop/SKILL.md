---
name: stitch-loop
version: "2.0"
last_updated: 2026-08-24
tags: [stitch, workflow, websites, iteration, frontend]
description: "Run an iterative Stitch website-building loop using `.stitch/next-prompt.md`, SITE.md, DESIGN.md, generated pages, and verification checkpoints."
license: "Apache-2.0"
---
# Stitch Build Loop

This skill is a catalog-normalized import from `https://github.com/google-labs-code/stitch-skills` at commit `7b53207b94e62911777d53d4238b5f8c88c2b519`, source path `plugins/stitch-utilities/skills/stitch-loop`. The upstream control file was corrected for this workspace: the verified Stitch MCP surface here is design-system oriented, so screen lookup, screen generation, and screen editing tools must be used only when the current host explicitly exposes them.

## When to Use This Skill

- Use when a multi-page site should be built iteratively with Stitch and baton files.
- The task involves Google Stitch project IDs, `.stitch/` artifacts, DESIGN.md files, Stitch exports, or Stitch-specific validation.
- The broader `stitch-design` router points here as the narrowest workflow.

## Workflow

1. Read `.stitch/next-prompt.md`, `.stitch/SITE.md`, and `.stitch/DESIGN.md` before generating or integrating pages.
2. Use `stitch-generate-design` for screen prompts when tools or the Stitch web UI are available.
3. When screen-generation MCP tools are absent, prepare the next prompt and record that the web UI/API step is required.
4. Move generated or exported HTML into the site only after checking the sitemap.
5. Run local browser verification when a page is integrated into a runnable site.
6. Update SITE.md, metadata, and `next-prompt.md` before closing the loop.

## Local Assets

- `examples/`, `resources/`, `references/`, or `reference/` are upstream support material when present. Treat `SKILL.md` as the source of truth if a support file mentions an unavailable MCP tool.
- `scripts/` are optional helpers. On Windows, prefer PowerShell or Node equivalents unless Git Bash or WSL is actually available.
- Keep generated `.stitch/` files out of commits unless the user explicitly wants them as durable examples.

## Corrected Stitch MCP Surface

Verified in this workspace on 2026-06-15: `create_project`, `upload_design_md`, `create_design_system_from_design_md`, `list_design_systems`, and `apply_design_system`. This 2026-07-29 source refresh did not re-verify a broader live MCP surface. Do not claim `list_projects`, `list_screens`, `get_project`, `get_screen`, `generate_screen_from_text`, `edit_screens`, or `generate_variants` were used unless the current host exposes those exact tools in the active tool list.

## Anti-Patterns

- Claiming a Stitch screen-generation, screen-editing, or screen-retrieval MCP call succeeded when the active host does not expose that tool.
- Uploading files, screenshots, HTML, markdown, or design assets to Stitch without user-approved destination and artifact details.
- Reading, printing, storing, or committing Stitch API keys, MCP config secrets, cookies, or credential-bearing files.
- Treating generated design or code as final without local render, syntax, or artifact verification.
- Collapsing this workflow into a broader frontend/design skill when Stitch-specific files, project IDs, or design-system assets matter.

## Verification Protocol

Before claiming this skill was applied successfully:

1. Pass/fail: Baton frontmatter has a page slug and concrete task body.
2. Pass/fail: SITE.md reflects sitemap, completed pages, and next backlog item.
3. Pass/fail: Generated or integrated pages were checked locally or unavailable generation is recorded.
4. Pass/fail: The loop leaves a next baton for the following session.
5. Pressure-test scenario: Repeat the workflow with Stitch MCP screen tools unavailable and confirm the fallback path remains honest and actionable.
6. Success metric: The user can identify the exact artifact, project/design-system target, and verification evidence without relying on unstated MCP behavior.

<!-- MCP:START -->

<!-- PORTABILITY:START -->

## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/stitch-loop` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: Stitch MCP

- Fallback prompt: "Use the Stitch Build Loop skill without Stitch MCP. Use the Stitch web UI plus local site integration when MCP generation tools are unavailable. Show the exact files, commands, manual Stitch UI steps, and verification evidence used before concluding."
- Verified Stitch MCP tools in this workspace are design-system/project oriented; use broader screen tools only when the current host exposes them.
- Use local scripts, exported HTML/screenshots, the Stitch web UI, and project metadata files as the fallback evidence path.

<!-- MCP:END -->

## Related Skills

- [stitch-generate-design](../stitch-generate-design/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
- [stitch-design-md](../stitch-design-md/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
- [stitch-extract-static-html](../stitch-extract-static-html/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
- [web-testing](../web-testing/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
