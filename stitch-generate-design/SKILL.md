---
name: stitch-generate-design
version: "1.2"
last_updated: 2026-06-15
tags: [stitch, design, prompting, screens, ui]
description: "Prepare Stitch screen-generation, edit, image-to-design, and variant prompts with verified tool checks and design-system-aware wording."
license: Apache-2.0
---

# Stitch Generate Design

This skill is a catalog-normalized import from `https://github.com/google-labs-code/stitch-skills` at commit `1544aa4a3be93e7515b0c27d32722f7ca5a2f691`, source path `plugins/stitch-design/skills/generate-design`. The upstream control file was corrected for this workspace: the verified Stitch MCP surface here is design-system oriented, so screen lookup, screen generation, and screen editing tools must be used only when the current host explicitly exposes them.

## When to Use This Skill

- Use when the user wants to generate, edit, or vary Stitch screens from text, screenshots, or mockups.
- The task involves Google Stitch project IDs, `.stitch/` artifacts, DESIGN.md files, Stitch exports, or Stitch-specific validation.
- The broader `stitch-design` router points here as the narrowest workflow.

## Workflow

1. Check the active host tool list. In this workspace, verified Stitch MCP tools cover project creation and design systems, not screen generation or editing.
2. If screen generation/edit tools are present, use them and record the exact tool names.
3. If those tools are absent, prepare the enhanced prompt for the Stitch web UI or another approved Stitch client.
4. Before generation, run `stitch-enhance-prompt` and avoid duplicating project-level colors and fonts when a design system exists.
5. Use `stitch-manage-design-system` first when the project needs a consistent design system.
6. Save returned or exported HTML/screenshots under `.stitch/designs/` and update `.stitch/metadata.json`.

## Local Assets

- `examples/`, `resources/`, `references/`, or `reference/` are upstream support material when present. Treat `SKILL.md` as the source of truth if a support file mentions an unavailable MCP tool.
- `scripts/` are optional helpers. On Windows, prefer PowerShell or Node equivalents unless Git Bash or WSL is actually available.
- Keep generated `.stitch/` files out of commits unless the user explicitly wants them as durable examples.

## Corrected Stitch MCP Surface

Verified in this workspace on 2026-06-15: `create_project`, `upload_design_md`, `create_design_system_from_design_md`, `list_design_systems`, and `apply_design_system`. Do not claim `list_projects`, `list_screens`, `get_project`, `get_screen`, `generate_screen_from_text`, `edit_screens`, or `generate_variants` were used unless the current host exposes those exact tools in the active tool list.

## Anti-Patterns

- Claiming a Stitch screen-generation, screen-editing, or screen-retrieval MCP call succeeded when the active host does not expose that tool.
- Uploading files, screenshots, HTML, markdown, or design assets to Stitch without user-approved destination and artifact details.
- Reading, printing, storing, or committing Stitch API keys, MCP config secrets, cookies, or credential-bearing files.
- Treating generated design or code as final without local render, syntax, or artifact verification.
- Collapsing this workflow into a broader frontend/design skill when Stitch-specific files, project IDs, or design-system assets matter.

## Verification Protocol

Before claiming this skill was applied successfully:

1. Pass/fail: The final prompt is structured by purpose, platform, and page sections.
2. Pass/fail: Design-system tokens are project-level or explicit edit instructions, not repeated blindly.
3. Pass/fail: Final screen evidence is a real Stitch export, screenshot, browser capture, or clearly labeled pending web-UI action.
4. Pass/fail: Unavailable MCP tools are not claimed as executed.
5. Pressure-test scenario: Repeat the workflow with Stitch MCP screen tools unavailable and confirm the fallback path remains honest and actionable.
6. Success metric: The user can identify the exact artifact, project/design-system target, and verification evidence without relying on unstated MCP behavior.

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:stitch-generate-design` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py stitch-generate-design` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: Stitch MCP

- Fallback prompt: "Use the Stitch Generate Design skill without Stitch MCP. Use the Stitch web UI with the enhanced prompt and save exported assets locally when the host lacks screen-generation MCP tools. Show the exact files, commands, manual Stitch UI steps, and verification evidence used before concluding."
- Verified Stitch MCP tools in this workspace are design-system/project oriented; use broader screen tools only when the current host exposes them.
- Use local scripts, exported HTML/screenshots, the Stitch web UI, and project metadata files as the fallback evidence path.

<!-- MCP:END -->

## Related Skills

- [stitch-enhance-prompt](../stitch-enhance-prompt/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
- [stitch-manage-design-system](../stitch-manage-design-system/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
- [stitch-design-md](../stitch-design-md/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
- [stitch-loop](../stitch-loop/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
