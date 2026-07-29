---
name: stitch-design
version: "2.0"
last_updated: 2026-07-29
tags: [stitch, design, frontend, ui, mcp]
description: "Route Google Stitch tasks to the correct imported Stitch skill, with verified MCP tool boundaries, upload safety, and cross-client fallback guidance."
license: "Apache-2.0"
---
# Stitch Design

Use this as the entrypoint for Google Stitch work. The old local monolithic Stitch guidance has been consolidated into narrower skills imported from `https://github.com/google-labs-code/stitch-skills` at commit `7b53207b94e62911777d53d4238b5f8c88c2b519`. This file now routes tasks and carries shared safety rules; detailed workflows live in the dedicated `stitch-*` skills.

## When to Use This Skill

- The user asks for Stitch, Google Stitch, Stitch MCP, DESIGN.md, Stitch screen generation, Stitch upload, or Stitch-to-code work.
- The task is unclear and needs routing to the correct Stitch design, build, or utility workflow.
- A previous broad Stitch workflow would have mixed upload, prompt, design-system, code, and video steps in one place.

## Route Selection

| Skill | Use when |
|---|---|
| `stitch-code-to-design` | Convert an existing frontend into Stitch-ready design assets by extracting static HTML, writing DESIGN.md, creating the design system, and uploading approved files. |
| `stitch-generate-design` | Prepare Stitch screen-generation, edit, image-to-design, and variant prompts with verified tool checks and design-system-aware wording. |
| `stitch-manage-design-system` | Create, list, and apply Stitch design systems from DESIGN.md using the verified Stitch MCP design-system tools and safe upload fallbacks. |
| `stitch-extract-design-md` | Extract a Stitch-compatible DESIGN.md from frontend source code, stylesheets, Tailwind config, theme files, and component patterns. |
| `stitch-extract-static-html` | Capture a self-contained static HTML snapshot from a running app or mock component so it can be reviewed or uploaded to Stitch. |
| `stitch-upload-to-stitch` | Upload approved local HTML, markdown, or image assets to a Stitch project using direct MCP for small DESIGN.md files or the bundled API script for larger files. |
| `stitch-react-components` | Convert Stitch HTML and screenshots into modular Vite/React/TypeScript components, or sync existing components to updated Stitch designs, with local architecture and validation checks. |
| `stitch-react-vite-dashboard` | Convert approved Stitch exports into accessible React and Vite dashboards with DESIGN.md tokens, TanStack Query data boundaries, responsive layouts, and optional read-only Web3 integrations. |
| `stitch-react-native` | Convert Stitch HTML designs into React Native screens, or sync existing native components to updated Stitch designs, using native primitives, StyleSheet rules, and mobile platform checks. |
| `stitch-remotion` | Create Remotion walkthrough videos from Stitch screen exports with ordered assets, transitions, captions, and render checks. |
| `stitch-shadcn-ui` | Integrate Stitch-derived UI direction into shadcn/ui React projects with registry-aware setup, ownership rules, theming, and validation. |
| `stitch-design-md` | Analyze existing Stitch project evidence and synthesize a semantic DESIGN.md for consistent future Stitch generation. |
| `stitch-enhance-prompt` | Transform rough UI requests into structured Stitch prompts with platform, layout, component, and design-system context. |
| `stitch-loop` | Run an iterative Stitch website-building loop using `.stitch/next-prompt.md`, SITE.md, DESIGN.md, generated pages, and verification checkpoints. |
| `stitch-taste-design` | Create opinionated premium DESIGN.md guidance for Stitch, emphasizing calibrated typography, restrained color, layout discipline, motion, and anti-generic UI rules. |

## Consolidation Decision

The previous `stitch-design` skill repeated design-md, React conversion, build-loop, prompt-enhancement, Remotion, and shadcn/ui guidance in one large file. Those important parts were not removed; they were moved into dedicated skills with clearer triggers, support assets, and verification protocols. This entrypoint stays small so agents choose the narrowest Stitch workflow first.

## Verified Stitch MCP Surface

Verified in this workspace on 2026-06-15: `create_project`, `upload_design_md`, `create_design_system_from_design_md`, `list_design_systems`, and `apply_design_system`. This 2026-07-29 source refresh did not re-verify a broader live MCP surface. Treat screen lookup, screen generation, screen editing, and variant generation tools as optional host-specific capabilities. Use them only when they are present in the active tool list.

## Common Workflow

1. Classify the task as prompt work, design-system work, static extraction, upload, screen generation, code generation, video generation, or iterative site building.
2. Open and follow the narrowest related Stitch skill.
3. Check the available Stitch MCP tools before naming or calling a tool.
4. Keep `.stitch/DESIGN.md`, `.stitch/metadata.json`, screenshots, and static HTML as the local evidence trail when the workflow creates them.
5. Ask before external uploads unless the current user request already approves that exact upload target and artifact.
6. Verify with Stitch MCP when the requested operation matches the available tool surface; otherwise document the web UI/API/local fallback used.

## Anti-Patterns

- Using this entrypoint as a replacement for reading the dedicated skill that matches the task.
- Claiming unavailable Stitch MCP screen tools exist because an upstream skill mentioned them.
- Uploading assets or creating external Stitch state without a clear project target and approval.
- Combining Stitch-specific skills into generic frontend skills when Stitch project IDs, DESIGN.md, or MCP evidence matter.

## Verification Protocol

Before claiming Stitch work is complete:

1. Pass/fail: The correct dedicated Stitch skill was selected and followed.
2. Pass/fail: The active Stitch MCP tool surface was checked and any unavailable tools were handled honestly.
3. Pass/fail: Local artifacts or external Stitch IDs were recorded with enough detail to reproduce the result.
4. Pass/fail: Uploads and external state changes had user-approved artifact and destination details.
5. Pressure-test scenario: Re-run the route selection with only the verified design-system MCP tools available and confirm the fallback path still works.
6. Success metric: The final response names the selected Stitch skill, evidence used, and whether verification was local, MCP-backed, or manual.

<!-- MCP:START -->

<!-- PORTABILITY:START -->

## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/stitch-design` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: Stitch MCP

- Fallback prompt: "Use the Stitch Design router without Stitch MCP. Route to the correct local Stitch skill, use local artifacts or the Stitch web UI where needed, and show the exact evidence used before concluding."
- Use screenshots, exported HTML, DESIGN.md files, local scripts, and metadata files when Stitch MCP is not exposed by the host.
- Treat generated React, design assets, and uploaded screens as drafts until verified through local render, Stitch MCP, or the Stitch UI.

<!-- MCP:END -->

## Related Skills

- [stitch-code-to-design](../stitch-code-to-design/SKILL.md): Dedicated Stitch workflow.
- [stitch-generate-design](../stitch-generate-design/SKILL.md): Dedicated Stitch workflow.
- [stitch-manage-design-system](../stitch-manage-design-system/SKILL.md): Dedicated Stitch workflow.
- [stitch-extract-design-md](../stitch-extract-design-md/SKILL.md): Dedicated Stitch workflow.
- [stitch-extract-static-html](../stitch-extract-static-html/SKILL.md): Dedicated Stitch workflow.
- [stitch-upload-to-stitch](../stitch-upload-to-stitch/SKILL.md): Dedicated Stitch workflow.
- [stitch-react-components](../stitch-react-components/SKILL.md): Dedicated Stitch workflow.
- [stitch-react-vite-dashboard](../stitch-react-vite-dashboard/SKILL.md): Dedicated Stitch workflow.
- [stitch-react-native](../stitch-react-native/SKILL.md): Dedicated Stitch workflow.
- [stitch-remotion](../stitch-remotion/SKILL.md): Dedicated Stitch workflow.
- [frontend-design](../frontend-design/SKILL.md): Use when the task needs general UI composition beyond Stitch.
