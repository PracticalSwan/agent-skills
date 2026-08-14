---
name: stitch-react-vite-dashboard
version: "2.0"
last_updated: 2026-08-14
tags: [stitch, react, vite, dashboard, typescript]
description: "Convert approved Stitch exports into accessible React and Vite dashboards with DESIGN.md tokens, TanStack Query data boundaries, responsive layouts, and optional read-only Web3 integrations."
license: "Apache-2.0"
---
# Stitch React Vite Dashboard

This skill is a catalog-normalized import from `https://github.com/google-labs-code/stitch-skills` at commit `7b53207b94e62911777d53d4238b5f8c88c2b519`, source path `plugins/stitch-build/skills/react-vite-dashboard`. The upstream control file was corrected for this workspace: the verified Stitch MCP surface here is design-system oriented, so screen lookup, screen generation, and screen editing tools must be used only when the current host explicitly exposes them.

## When to Use This Skill

- Use when a Stitch design should become a data-dense React and Vite dashboard rather than a general component library.
- The task involves Google Stitch project IDs, `.stitch/` artifacts, DESIGN.md files, Stitch exports, or Stitch-specific validation.
- The broader `stitch-design` router points here as the narrowest workflow.

## Workflow

1. Acquire approved Stitch HTML and screenshots from local exports, the Stitch web UI, or current host-listed screen tools; do not assume screen retrieval tools exist.
2. Read DESIGN.md and map real color, typography, spacing, radius, and focus tokens into CSS variables or the selected styling system.
3. Scaffold or confirm React, Vite, TypeScript, React Router, and TanStack Query boundaries before generating dashboard components.
4. Use semantic tables or TanStack Table for tabular data, native buttons and labels, visible focus states, and `aria-busy` for loading regions.
5. Keep presentational components pure and place asynchronous access in typed query hooks.
6. For optional Web3 reads, isolate providers, format token values safely, show network identity, and never embed private keys or private RPC credentials.
7. Run the local build, type checks, responsive checks at narrow and desktop widths, and an accessibility review.

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

1. Pass/fail: Dashboard tokens are traceable to DESIGN.md or explicitly labeled as fallbacks.
2. Pass/fail: Tables, forms, loading states, keyboard order, and focus behavior use accessible semantics.
3. Pass/fail: Data access is isolated from presentational components and does not leak secrets into Vite-exposed environment variables.
4. Pass/fail: The dashboard build and representative responsive states were checked locally or the blocker is documented.
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
  `$CODEX_HOME/skills/stitch-react-vite-dashboard` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: Stitch MCP

- Fallback prompt: "Use the Stitch React Vite Dashboard skill without Stitch MCP. Use approved local Stitch exports and standard React/Vite tooling when Stitch MCP screen retrieval is unavailable. Show the exact files, commands, manual Stitch UI steps, and verification evidence used before concluding."
- Verified Stitch MCP tools in this workspace are design-system/project oriented; use broader screen tools only when the current host exposes them.
- Use local scripts, exported HTML/screenshots, the Stitch web UI, and project metadata files as the fallback evidence path.

<!-- MCP:END -->

## Related Skills

- [stitch-react-components](../stitch-react-components/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
- [stitch-design-md](../stitch-design-md/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
- [react-development](../react-development/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
- [vite-development](../vite-development/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
