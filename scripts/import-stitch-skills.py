#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


DATE = "2026-07-29"
MCP_VERIFIED_DATE = "2026-06-15"
SOURCE_REPO = "https://github.com/google-labs-code/stitch-skills"
SOURCE_COMMIT = "7b53207b94e62911777d53d4238b5f8c88c2b519"
COPY_DIRS = {"scripts", "resources", "references", "reference", "examples"}
COPY_FILES = {"package.json", "package-lock.json"}


SKILLS = [
    {
        "dest": "stitch-code-to-design",
        "source": "plugins/stitch-design/skills/code-to-design",
        "title": "Stitch Code To Design",
        "tags": ["stitch", "design", "frontend", "html", "migration"],
        "description": "Convert an existing frontend into Stitch-ready design assets by extracting static HTML, writing DESIGN.md, creating the design system, and uploading approved files.",
        "use": "Use when an existing web app, React view, or static page must be moved into Stitch.",
        "workflow": [
            "Resolve the target app root, route, and intended Stitch project. If the project ID is unknown, require a user-provided Stitch URL/project ID, the Stitch web UI, or a host-listed lookup tool.",
            "Run `stitch-extract-static-html` for the relevant route or UI state and keep the output under `.stitch/`.",
            "Run `stitch-extract-design-md` against the source tree and save `.stitch/DESIGN.md`.",
            "Run `stitch-manage-design-system` to create or update the Stitch design system, using `--generated-by 'stitch::code-to-design'` when the bundled upload helper is needed.",
            "Run `stitch-upload-to-stitch` for the static HTML only after the user approves the exact file, size, and destination; identify the producer with `--generated-by 'stitch::extract-static-html'`.",
            "Update `.stitch/metadata.json` with project, screen, and design-system identifiers.",
        ],
        "checks": [
            "`.stitch/DESIGN.md` exists and summarizes real source tokens.",
            "The static HTML opens locally enough to inspect core layout and images.",
            "Stitch design-system creation was MCP-verified or the fallback evidence is recorded.",
            "No API key, token, cookie, or credential-bearing config was copied into durable files.",
        ],
        "fallback": "Use local extraction, source-code design-system synthesis, and manual Stitch web UI upload when MCP upload tools are unavailable.",
        "related": ["stitch-extract-static-html", "stitch-extract-design-md", "stitch-manage-design-system", "stitch-upload-to-stitch"],
        "reason": "Orchestrates the end-to-end path from an existing frontend to a Stitch project while keeping each step separately verifiable.",
    },
    {
        "dest": "stitch-generate-design",
        "source": "plugins/stitch-design/skills/generate-design",
        "title": "Stitch Generate Design",
        "tags": ["stitch", "design", "prompting", "screens", "ui"],
        "description": "Prepare Stitch screen-generation, edit, image-to-design, and variant prompts with verified tool checks and design-system-aware wording.",
        "use": "Use when the user wants to generate, edit, or vary Stitch screens from text, screenshots, or mockups.",
        "workflow": [
            "Check the active host tool list. In this workspace, verified Stitch MCP tools cover project creation and design systems, not screen generation or editing.",
            "If screen generation/edit tools are present, use them and record the exact tool names.",
            "If those tools are absent, prepare the enhanced prompt for the Stitch web UI or another approved Stitch client.",
            "Before generation, run `stitch-enhance-prompt` and avoid duplicating project-level colors and fonts when a design system exists.",
            "Use `stitch-manage-design-system` first when the project needs a consistent design system.",
            "Save returned or exported HTML/screenshots under `.stitch/designs/` and update `.stitch/metadata.json`.",
        ],
        "checks": [
            "The final prompt is structured by purpose, platform, and page sections.",
            "Design-system tokens are project-level or explicit edit instructions, not repeated blindly.",
            "Final screen evidence is a real Stitch export, screenshot, browser capture, or clearly labeled pending web-UI action.",
            "Unavailable MCP tools are not claimed as executed.",
        ],
        "fallback": "Use the Stitch web UI with the enhanced prompt and save exported assets locally when the host lacks screen-generation MCP tools.",
        "related": ["stitch-enhance-prompt", "stitch-manage-design-system", "stitch-design-md", "stitch-loop"],
        "reason": "Keeps generation and editing prompt work separate from upload and code-conversion workflows while correcting unsupported MCP assumptions.",
    },
    {
        "dest": "stitch-manage-design-system",
        "source": "plugins/stitch-design/skills/manage-design-system",
        "title": "Stitch Manage Design System",
        "tags": ["stitch", "design-system", "mcp", "tokens", "ui"],
        "description": "Create, list, and apply Stitch design systems from DESIGN.md using the verified Stitch MCP design-system tools and safe upload fallbacks.",
        "use": "Use when `.stitch/DESIGN.md` should become a Stitch design system or an existing design system should be listed or applied.",
        "workflow": [
            "Create or identify the target project; use `create_project` only when a new project is appropriate.",
            "Inspect `.stitch/DESIGN.md` for project name, colors, type, shape, component, layout, and anti-pattern rules.",
            "For small DESIGN.md files, base64-encode UTF-8 content and call `upload_design_md` with the numeric project ID; for the bundled helper, pass `--generated-by` with the calling skill or agent name.",
            "Immediately call `create_design_system_from_design_md` with the returned screen instance `id` and `sourceScreen`.",
            "Use `list_design_systems` to confirm the design-system asset exists for the project.",
            "Use `apply_design_system` only with valid selected screen instance `id` and `sourceScreen` values.",
        ],
        "checks": [
            "`upload_design_md` and `create_design_system_from_design_md` were called in sequence, or fallback evidence is recorded.",
            "`list_design_systems` returns the expected design-system asset.",
            "`apply_design_system` calls pass only `id` and `sourceScreen` for selected screen instances.",
            "Local metadata records the project ID and design-system asset ID when available.",
        ],
        "fallback": "Use the Stitch web UI or bundled upload script for large files when direct MCP upload would exceed model output limits.",
        "related": ["stitch-design-md", "stitch-extract-design-md", "stitch-taste-design", "stitch-generate-design"],
        "reason": "Provides the verified MCP-backed core of the Stitch import and replaces unsupported upstream lookup calls with actual design-system tools.",
    },
    {
        "dest": "stitch-extract-design-md",
        "source": "plugins/stitch-design/skills/extract-design-md",
        "title": "Stitch Extract DESIGN.md From Source",
        "tags": ["stitch", "design-system", "frontend", "tokens", "audit"],
        "description": "Extract a Stitch-compatible DESIGN.md from frontend source code, stylesheets, Tailwind config, theme files, and component patterns.",
        "use": "Use when source code should reveal the visual system before a Stitch upload or generation workflow.",
        "workflow": [
            "Detect the framework and read the closest file under `references/`: React/Tailwind, Vue, Svelte, Angular, or plain CSS.",
            "Read theme config, global CSS, font imports, layout roots, representative components, and state styles.",
            "Extract actual colors, fonts, spacing, radii, shadows, variants, and responsive rules.",
            "Name tokens semantically and keep exact values next to descriptive labels.",
            "Write `.stitch/DESIGN.md` using atmosphere, palette, typography, components, layout, and generation notes.",
            "Hand off to `stitch-manage-design-system` when the user wants upload.",
        ],
        "checks": [
            "Every color and typography claim is traceable to source or marked as inference.",
            "Framework guidance was selected correctly.",
            "The DESIGN.md translates technical values into semantic design language.",
            "No fabricated brand claims, metrics, or unsupported implementation details were introduced.",
        ],
        "fallback": "No Stitch MCP is required; use local source reads, repo search, and framework references.",
        "related": ["stitch-design-md", "stitch-manage-design-system", "frontend-design"],
        "reason": "Keeps source-code design extraction distinct from rendered Stitch project analysis.",
    },
    {
        "dest": "stitch-extract-static-html",
        "source": "plugins/stitch-design/skills/extract-static-html",
        "title": "Stitch Extract Static HTML",
        "tags": ["stitch", "html", "frontend", "snapshot", "assets"],
        "description": "Capture a self-contained static HTML snapshot from a running app or mock component so it can be reviewed or uploaded to Stitch.",
        "use": "Use when a route or UI state must become standalone HTML for review or Stitch upload.",
        "workflow": [
            "Prefer `scripts/snapshot.ts` when the app can run locally without auth blockers.",
            "Use interactive browser capture only when clicks, form input, or navigation are needed first.",
            "Use static mock fallback only when the app cannot run and the user accepts a manually flattened state.",
            "Start or identify the dev server and record the URL before capture.",
            "Run `npx tsx scripts/snapshot.ts --url <url> --output .stitch/<page>.html` with matched viewport and wait flags.",
            "Open or parse the output to confirm CSS, images, and critical layout survived script removal.",
        ],
        "checks": [
            "The output HTML exists under `.stitch/`.",
            "Capture route, viewport, wait time, and special flags are recorded.",
            "Important images are inlined or intentionally left as stable external URLs.",
            "No authenticated personal content, cookies, tokens, or private user data were captured.",
        ],
        "fallback": "Use browser export or a manually flattened mock component when Puppeteer is unavailable, then document fidelity limits.",
        "related": ["stitch-code-to-design", "stitch-upload-to-stitch", "web-testing", "vite-development"],
        "reason": "Splits static capture from upload so local browser evidence is available before external Stitch side effects.",
    },
    {
        "dest": "stitch-upload-to-stitch",
        "source": "plugins/stitch-design/skills/upload-to-stitch",
        "title": "Stitch Upload To Stitch",
        "tags": ["stitch", "upload", "assets", "html", "mcp"],
        "description": "Upload approved local HTML, markdown, or image assets to a Stitch project using direct MCP for small DESIGN.md files or the bundled API script for larger files.",
        "use": "Use when approved local HTML, markdown, image, or mockup files must be uploaded to a Stitch project.",
        "workflow": [
            "List file path, size, MIME type, target project ID, and upload method before uploading.",
            "For small DESIGN.md content, prefer `upload_design_md` followed by `create_design_system_from_design_md` through `stitch-manage-design-system`.",
            "For HTML, markdown, or image uploads, use `scripts/upload_to_stitch.py` only with a user-approved API key source and set `--generated-by` to the calling skill or agent.",
            "Never print, commit, or store the Stitch API key.",
            "Use non-default `--api-url` only when a verified config or user instruction provides it.",
            "Save returned source screen and screen instance IDs in `.stitch/metadata.json`.",
        ],
        "checks": [
            "The file type is supported: `.html`, `.htm`, `.md`, `.png`, `.jpg`, `.jpeg`, or `.webp`.",
            "User approval covers the actual file and destination project.",
            "The response returned expected IDs, or the failure response is captured without leaking secrets.",
            "Local metadata was updated without credentials.",
        ],
        "fallback": "Use the Stitch web UI for manual upload when API credentials are unavailable or external upload risk needs review.",
        "related": ["stitch-code-to-design", "stitch-manage-design-system", "stitch-extract-static-html"],
        "reason": "Centralizes upload safety, credential handling, and token-limit workarounds.",
    },
    {
        "dest": "stitch-react-components",
        "source": "plugins/stitch-build/skills/react-components",
        "title": "Stitch React Components",
        "tags": ["stitch", "react", "typescript", "components", "frontend"],
        "description": "Convert Stitch HTML and screenshots into modular Vite/React/TypeScript components, or sync existing components to updated Stitch designs, with local architecture and validation checks.",
        "use": "Use when a Stitch screen or export should become modular React components or an existing React surface must be synchronized with newer Stitch evidence.",
        "workflow": [
            "Acquire source HTML and screenshots from `.stitch/designs/`, Stitch web exports, or current host-listed screen tools.",
            "Do not assume `get_screen` or `list_screens` exists in this workspace.",
            "Record available project and screen identifiers plus the sync timestamp in `.stitch/metadata.json` when that evidence exists.",
            "Extract current color, typography, spacing, and radius tokens from the exported HTML before editing components.",
            "Move static copy, image URLs, and lists into `src/data/mockData.ts`.",
            "Create small components with `Readonly` prop interfaces and isolate interactions in hooks.",
            "Map Stitch theme values into Tailwind/theme tokens, replace placeholder links with real application routes, and cover dark-mode states instead of scattering raw hex values.",
            "Run the bundled validator where dependencies are available, then run the app build or dev check.",
        ],
        "checks": [
            "Every component has typed props or an explicit reason it has no props.",
            "Static content is separated from component structure.",
            "Generated project code does not carry irrelevant upstream license headers.",
            "The rendered app was checked locally or the blocker is documented.",
        ],
        "fallback": "Use local Stitch exports and browser screenshots when MCP screen retrieval is unavailable.",
        "related": ["react-development", "frontend-design", "stitch-extract-static-html", "stitch-shadcn-ui"],
        "reason": "Narrows old Stitch-to-React guidance into a dedicated React implementation skill.",
    },
    {
        "dest": "stitch-react-vite-dashboard",
        "source": "plugins/stitch-build/skills/react-vite-dashboard",
        "title": "Stitch React Vite Dashboard",
        "tags": ["stitch", "react", "vite", "dashboard", "typescript"],
        "description": "Convert approved Stitch exports into accessible React and Vite dashboards with DESIGN.md tokens, TanStack Query data boundaries, responsive layouts, and optional read-only Web3 integrations.",
        "use": "Use when a Stitch design should become a data-dense React and Vite dashboard rather than a general component library.",
        "workflow": [
            "Acquire approved Stitch HTML and screenshots from local exports, the Stitch web UI, or current host-listed screen tools; do not assume screen retrieval tools exist.",
            "Read DESIGN.md and map real color, typography, spacing, radius, and focus tokens into CSS variables or the selected styling system.",
            "Scaffold or confirm React, Vite, TypeScript, React Router, and TanStack Query boundaries before generating dashboard components.",
            "Use semantic tables or TanStack Table for tabular data, native buttons and labels, visible focus states, and `aria-busy` for loading regions.",
            "Keep presentational components pure and place asynchronous access in typed query hooks.",
            "For optional Web3 reads, isolate providers, format token values safely, show network identity, and never embed private keys or private RPC credentials.",
            "Run the local build, type checks, responsive checks at narrow and desktop widths, and an accessibility review.",
        ],
        "checks": [
            "Dashboard tokens are traceable to DESIGN.md or explicitly labeled as fallbacks.",
            "Tables, forms, loading states, keyboard order, and focus behavior use accessible semantics.",
            "Data access is isolated from presentational components and does not leak secrets into Vite-exposed environment variables.",
            "The dashboard build and representative responsive states were checked locally or the blocker is documented.",
        ],
        "fallback": "Use approved local Stitch exports and standard React/Vite tooling when Stitch MCP screen retrieval is unavailable.",
        "related": ["stitch-react-components", "stitch-design-md", "react-development", "vite-development"],
        "reason": "Adds the upstream dashboard-specific workflow without merging data-dense, query-driven concerns into the general React component skill.",
    },
    {
        "dest": "stitch-react-native",
        "source": "plugins/stitch-build/skills/react-native",
        "title": "Stitch React Native",
        "tags": ["stitch", "react-native", "mobile", "components", "frontend"],
        "description": "Convert Stitch HTML designs into React Native screens, or sync existing native components to updated Stitch designs, using native primitives, StyleSheet rules, and mobile platform checks.",
        "use": "Use when Stitch web designs should become React Native screens or existing native components must be synchronized with newer Stitch evidence.",
        "workflow": [
            "Start from exported Stitch HTML and a screenshot, using host-listed screen tools only when present.",
            "Extract current theme values into `src/theme.ts` and record available project/screen identifiers plus the sync timestamp in `.stitch/metadata.json`.",
            "Map web elements to React Native primitives and wrap visible text in `Text`.",
            "Translate CSS into `StyleSheet.create()` with shared theme values rather than raw color literals.",
            "Replace hover, fixed positioning, browser-only CSS, and DOM events with native patterns.",
            "Use `react-native-safe-area-context`, accessibility labels and roles, useWindowDimensions, Platform.select, FlatList, and SectionList where appropriate.",
            "Validate syntax with the bundled validator when dependencies are installed.",
        ],
        "checks": [
            "No DOM tags or web event names remain.",
            "Text, images, lists, and press interactions use native primitives.",
            "iOS and Android shadow/safe-area differences are handled or scoped out.",
            "The result was checked with local React Native tooling or blocker evidence.",
        ],
        "fallback": "Use local HTML/screenshots and manual native mapping when Stitch MCP screen retrieval is unavailable.",
        "related": ["stitch-react-components", "frontend-design", "react-development"],
        "reason": "Keeps mobile conversion separate from web React conversion because platform constraints differ.",
    },
    {
        "dest": "stitch-remotion",
        "source": "plugins/stitch-build/skills/remotion",
        "title": "Stitch Remotion Walkthrough",
        "tags": ["stitch", "remotion", "video", "screens", "react"],
        "description": "Create Remotion walkthrough videos from Stitch screen exports with ordered assets, transitions, captions, and render checks.",
        "use": "Use when Stitch screens or a design flow should become a Remotion video walkthrough.",
        "workflow": [
            "Gather screenshots and optional HTML/text from `.stitch/designs/`, Stitch web exports, or current host-listed screen tools.",
            "Create deterministic `screens.json` with title, order, image path, dimensions, and narration notes.",
            "Use bundled templates as starting points, not final untailored output.",
            "Set composition dimensions from the actual screen set.",
            "Preview the Remotion composition before rendering.",
            "Render the final MP4 only after timing, crop, and text overlays are acceptable.",
        ],
        "checks": [
            "Every manifest entry points to an existing screenshot or approved placeholder.",
            "Preview was reviewed for crop, timing, text, and transitions.",
            "The final render command and output path are recorded.",
            "Unavailable Stitch or Remotion MCP tools are not claimed as used.",
        ],
        "fallback": "Use Remotion CLI and local exported screenshots when Stitch or Remotion MCP tools are unavailable.",
        "related": ["stitch-generate-design", "stitch-react-components", "frontend-design"],
        "reason": "Preserves the media-generation workflow as its own skill.",
    },
    {
        "dest": "stitch-shadcn-ui",
        "source": "plugins/stitch-build/skills/shadcn-ui",
        "title": "Stitch shadcn/ui Integration",
        "tags": ["stitch", "shadcn", "react", "components", "tailwind"],
        "description": "Integrate Stitch-derived UI direction into shadcn/ui React projects with registry-aware setup, ownership rules, theming, and validation.",
        "use": "Use when a Stitch design should be implemented with shadcn/ui components.",
        "workflow": [
            "Inspect for `components.json`, Tailwind config, path aliases, and existing `components/ui` patterns.",
            "Use `npx shadcn@latest init` or `npx shadcn@latest add <component>` unless a verified shadcn MCP tool exists.",
            "Map Stitch components to shadcn primitives such as Button, Card, Dialog, Sheet, Tabs, Table, Command, Form, and Select.",
            "Keep `components/ui` close to generated source; build project-specific wrappers elsewhere.",
            "Update CSS variables and Tailwind tokens to match DESIGN.md.",
            "Verify light/dark themes, keyboard behavior, ARIA attributes, and responsive layouts.",
        ],
        "checks": [
            "Installed components are present and imports resolve.",
            "The app builds or the dependency/tooling blocker is captured.",
            "Interactive components preserve focus, keyboard, and ARIA behavior.",
            "Design mapping is token-based rather than arbitrary classes.",
        ],
        "fallback": "Use the shadcn CLI and official registry docs when no shadcn MCP server is exposed.",
        "related": ["react-development", "frontend-design", "stitch-react-components"],
        "reason": "Keeps shadcn integration separate from general React conversion because it has its own CLI and ownership model.",
    },
    {
        "dest": "stitch-design-md",
        "source": "plugins/stitch-utilities/skills/design-md",
        "title": "Stitch DESIGN.md From Project",
        "tags": ["stitch", "design-system", "design-md", "tokens", "mcp"],
        "description": "Analyze existing Stitch project evidence and synthesize a semantic DESIGN.md for consistent future Stitch generation.",
        "use": "Use when existing Stitch screens, screenshots, HTML, or metadata should become a DESIGN.md source of truth.",
        "workflow": [
            "Gather screenshots, exported HTML, design-system metadata, user descriptions, or host-listed screen retrieval output.",
            "Do not assume this workspace exposes `list_projects`, `list_screens`, `get_screen`, or `get_project`.",
            "Extract atmosphere, palette, typography, shape, elevation, components, layout, responsive behavior, and interaction states.",
            "Translate CSS/Tailwind into descriptive names with exact values.",
            "Write `.stitch/DESIGN.md` with project title and reusable prompting language.",
            "Hand off to `stitch-manage-design-system` for upload.",
        ],
        "checks": [
            "The DESIGN.md is grounded in real exports or labeled user-provided descriptions.",
            "Major tokens include semantic role and exact value where available.",
            "The document avoids implementation-only jargon.",
            "The next action is clear: upload, web UI use, or local prompt use.",
        ],
        "fallback": "Use screenshots, exported HTML, and local notes when Stitch MCP screen retrieval is unavailable.",
        "related": ["stitch-extract-design-md", "stitch-manage-design-system", "stitch-taste-design"],
        "reason": "Keeps rendered/project-based DESIGN.md synthesis distinct from source-code extraction.",
    },
    {
        "dest": "stitch-enhance-prompt",
        "source": "plugins/stitch-utilities/skills/enhance-prompt",
        "title": "Stitch Enhance Prompt",
        "tags": ["stitch", "prompting", "ui", "design", "copy"],
        "description": "Transform rough UI requests into structured Stitch prompts with platform, layout, component, and design-system context.",
        "use": "Use when a rough Stitch prompt needs better structure or an edit prompt needs precision.",
        "workflow": [
            "Identify platform, page type, intent, sections, visual style, components, and constraints already present.",
            "Read `.stitch/DESIGN.md` when present and include only relevant rules.",
            "Replace vague terms with concrete UI patterns, component names, and layout structure.",
            "For generation prompts, describe layout, content, and behavior without duplicating project-level theme tokens.",
            "For edit prompts, name the exact screen region and focused change.",
            "Return the enhanced prompt plus assumptions that affect the design.",
        ],
        "checks": [
            "Output includes platform, purpose, page structure, and component terms.",
            "It preserves user intent instead of over-designing a different product.",
            "Design-system context is included only when useful.",
            "The prompt is ready for Stitch generation or web UI use.",
        ],
        "fallback": "No MCP is required; use local DESIGN.md files, prompt references, and user context.",
        "related": ["stitch-generate-design", "stitch-design-md", "stitch-taste-design", "avoid-ai-writing"],
        "reason": "Prompt enhancement is reusable across generation, editing, and loop workflows without depending on external tools.",
    },
    {
        "dest": "stitch-loop",
        "source": "plugins/stitch-utilities/skills/stitch-loop",
        "title": "Stitch Build Loop",
        "tags": ["stitch", "workflow", "websites", "iteration", "frontend"],
        "description": "Run an iterative Stitch website-building loop using `.stitch/next-prompt.md`, SITE.md, DESIGN.md, generated pages, and verification checkpoints.",
        "use": "Use when a multi-page site should be built iteratively with Stitch and baton files.",
        "workflow": [
            "Read `.stitch/next-prompt.md`, `.stitch/SITE.md`, and `.stitch/DESIGN.md` before generating or integrating pages.",
            "Use `stitch-generate-design` for screen prompts when tools or the Stitch web UI are available.",
            "When screen-generation MCP tools are absent, prepare the next prompt and record that the web UI/API step is required.",
            "Move generated or exported HTML into the site only after checking the sitemap.",
            "Run local browser verification when a page is integrated into a runnable site.",
            "Update SITE.md, metadata, and `next-prompt.md` before closing the loop.",
        ],
        "checks": [
            "Baton frontmatter has a page slug and concrete task body.",
            "SITE.md reflects sitemap, completed pages, and next backlog item.",
            "Generated or integrated pages were checked locally or unavailable generation is recorded.",
            "The loop leaves a next baton for the following session.",
        ],
        "fallback": "Use the Stitch web UI plus local site integration when MCP generation tools are unavailable.",
        "related": ["stitch-generate-design", "stitch-design-md", "stitch-extract-static-html", "web-testing"],
        "reason": "Keeps autonomous multi-page iteration separate from one-off screen generation and local code conversion.",
    },
    {
        "dest": "stitch-taste-design",
        "source": "plugins/stitch-utilities/skills/taste-design",
        "title": "Stitch Taste Design",
        "tags": ["stitch", "design-system", "taste", "ui", "prompting"],
        "description": "Create opinionated premium DESIGN.md guidance for Stitch, emphasizing calibrated typography, restrained color, layout discipline, motion, and anti-generic UI rules.",
        "use": "Use when a Stitch DESIGN.md needs a stronger design-quality point of view rather than token extraction.",
        "workflow": [
            "Clarify product type, audience, density, motion, brand constraints, and forbidden aesthetics.",
            "Define atmosphere, palette, typography, component behavior, layout, responsive rules, motion, and anti-patterns.",
            "Use exact values only when chosen or derived intentionally.",
            "Avoid invented metrics, fake dashboards, decorative cliches, and data claims the user did not provide.",
            "Write DESIGN.md language that Stitch can use directly.",
            "Optionally hand off to `stitch-manage-design-system` to upload after approval.",
        ],
        "checks": [
            "The direction matches product domain and audience.",
            "Color, type, layout, and motion rules are concrete enough for Stitch generation.",
            "The anti-pattern list is specific and enforceable.",
            "No fake data, unsupported claims, or inaccessible requirements were introduced.",
        ],
        "fallback": "No MCP is required for drafting; upload later through Stitch MCP or web UI.",
        "related": ["frontend-design", "stitch-design-md", "stitch-enhance-prompt"],
        "reason": "Preserves the opinionated design-quality role as distinct from extraction and prompt-polishing skills.",
    },
]


def render_frontmatter(skill: dict) -> str:
    tags = ", ".join(skill["tags"])
    return (
        "---\n"
        f"name: {skill['dest']}\n"
        'version: "2.0"\n'
        f"last_updated: {DATE}\n"
        f"tags: [{tags}]\n"
        f"description: \"{skill['description']}\"\n"
        "license: Apache-2.0\n"
        "---\n\n"
    )


def numbered(items: list[str]) -> str:
    return "\n".join(f"{i}. {item}" for i, item in enumerate(items, 1))


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def render_skill(skill: dict) -> str:
    related = "\n".join(
        f"- [{name}](../{name}/SKILL.md): Use when the task also needs this adjacent Stitch workflow."
        for name in skill["related"]
    )
    checks = "\n".join(
        f"{i}. Pass/fail: {item}" for i, item in enumerate(skill["checks"], 1)
    )
    return render_frontmatter(skill) + f"""# {skill["title"]}

This skill is a catalog-normalized import from `{SOURCE_REPO}` at commit `{SOURCE_COMMIT}`, source path `{skill["source"]}`. The upstream control file was corrected for this workspace: the verified Stitch MCP surface here is design-system oriented, so screen lookup, screen generation, and screen editing tools must be used only when the current host explicitly exposes them.

## When to Use This Skill

- {skill["use"]}
- The task involves Google Stitch project IDs, `.stitch/` artifacts, DESIGN.md files, Stitch exports, or Stitch-specific validation.
- The broader `stitch-design` router points here as the narrowest workflow.

## Workflow

{numbered(skill["workflow"])}

## Local Assets

- `examples/`, `resources/`, `references/`, or `reference/` are upstream support material when present. Treat `SKILL.md` as the source of truth if a support file mentions an unavailable MCP tool.
- `scripts/` are optional helpers. On Windows, prefer PowerShell or Node equivalents unless Git Bash or WSL is actually available.
- Keep generated `.stitch/` files out of commits unless the user explicitly wants them as durable examples.

## Corrected Stitch MCP Surface

Verified in this workspace on {MCP_VERIFIED_DATE}: `create_project`, `upload_design_md`, `create_design_system_from_design_md`, `list_design_systems`, and `apply_design_system`. This 2026-07-29 source refresh did not re-verify a broader live MCP surface. Do not claim `list_projects`, `list_screens`, `get_project`, `get_screen`, `generate_screen_from_text`, `edit_screens`, or `generate_variants` were used unless the current host exposes those exact tools in the active tool list.

## Anti-Patterns

- Claiming a Stitch screen-generation, screen-editing, or screen-retrieval MCP call succeeded when the active host does not expose that tool.
- Uploading files, screenshots, HTML, markdown, or design assets to Stitch without user-approved destination and artifact details.
- Reading, printing, storing, or committing Stitch API keys, MCP config secrets, cookies, or credential-bearing files.
- Treating generated design or code as final without local render, syntax, or artifact verification.
- Collapsing this workflow into a broader frontend/design skill when Stitch-specific files, project IDs, or design-system assets matter.

## Verification Protocol

Before claiming this skill was applied successfully:

{checks}
5. Pressure-test scenario: Repeat the workflow with Stitch MCP screen tools unavailable and confirm the fallback path remains honest and actionable.
6. Success metric: The user can identify the exact artifact, project/design-system target, and verification evidence without relying on unstated MCP behavior.

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: Stitch MCP

- Fallback prompt: "Use the {skill["title"]} skill without Stitch MCP. {skill["fallback"]} Show the exact files, commands, manual Stitch UI steps, and verification evidence used before concluding."
- Verified Stitch MCP tools in this workspace are design-system/project oriented; use broader screen tools only when the current host exposes them.
- Use local scripts, exported HTML/screenshots, the Stitch web UI, and project metadata files as the fallback evidence path.

<!-- MCP:END -->

## Related Skills

{related}
"""


def render_changelog_entry(skill: dict) -> str:
    return f"""## [{DATE}] - Upstream Refresh and MCP Correction

### Added

- Refreshed support material from `{SOURCE_REPO}` at `{skill["source"]}` and commit `{SOURCE_COMMIT}`.

### Changed

- Normalized the refreshed workflow into the local `version: "2.0"` schema with folder-safe naming.
- Preserved the verified design-system MCP boundary while incorporating compatible upstream workflow and helper-script improvements.

### Fixed

- Avoided importing upstream assumptions that unverified Stitch screen lookup, generation, or editing tools are always available.
"""


def render_router() -> str:
    rows = "\n".join(
        f"| `{skill['dest']}` | {skill['description']} |" for skill in SKILLS
    )
    related = "\n".join(
        f"- [{skill['dest']}](../{skill['dest']}/SKILL.md): Dedicated Stitch workflow."
        for skill in SKILLS[:10]
    )
    related += "\n- [frontend-design](../frontend-design/SKILL.md): Use when the task needs general UI composition beyond Stitch."
    return f"""---
name: stitch-design
version: "2.0"
last_updated: {DATE}
tags: [stitch, design, frontend, ui, mcp]
description: "Route Google Stitch tasks to the correct imported Stitch skill, with verified MCP tool boundaries, upload safety, and cross-client fallback guidance."
license: Apache-2.0
---

# Stitch Design

Use this as the entrypoint for Google Stitch work. The old local monolithic Stitch guidance has been consolidated into narrower skills imported from `{SOURCE_REPO}` at commit `{SOURCE_COMMIT}`. This file now routes tasks and carries shared safety rules; detailed workflows live in the dedicated `stitch-*` skills.

## When to Use This Skill

- The user asks for Stitch, Google Stitch, Stitch MCP, DESIGN.md, Stitch screen generation, Stitch upload, or Stitch-to-code work.
- The task is unclear and needs routing to the correct Stitch design, build, or utility workflow.
- A previous broad Stitch workflow would have mixed upload, prompt, design-system, code, and video steps in one place.

## Route Selection

| Skill | Use when |
|---|---|
{rows}

## Consolidation Decision

The previous `stitch-design` skill repeated design-md, React conversion, build-loop, prompt-enhancement, Remotion, and shadcn/ui guidance in one large file. Those important parts were not removed; they were moved into dedicated skills with clearer triggers, support assets, and verification protocols. This entrypoint stays small so agents choose the narrowest Stitch workflow first.

## Verified Stitch MCP Surface

Verified in this workspace on {MCP_VERIFIED_DATE}: `create_project`, `upload_design_md`, `create_design_system_from_design_md`, `list_design_systems`, and `apply_design_system`. This 2026-07-29 source refresh did not re-verify a broader live MCP surface. Treat screen lookup, screen generation, screen editing, and variant generation tools as optional host-specific capabilities. Use them only when they are present in the active tool list.

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

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: Stitch MCP

- Fallback prompt: "Use the Stitch Design router without Stitch MCP. Route to the correct local Stitch skill, use local artifacts or the Stitch web UI where needed, and show the exact evidence used before concluding."
- Use screenshots, exported HTML, DESIGN.md files, local scripts, and metadata files when Stitch MCP is not exposed by the host.
- Treat generated React, design assets, and uploaded screens as drafts until verified through local render, Stitch MCP, or the Stitch UI.

<!-- MCP:END -->

## Related Skills

{related}
"""


def copy_support(repo_root: Path, source_root: Path, skill: dict, license_text: str) -> None:
    src_dir = source_root / skill["source"]
    dest_dir = repo_root / skill["dest"]
    dest_dir.mkdir(exist_ok=True)
    for child in src_dir.iterdir():
        if child.name in {"SKILL.md", "README.md"}:
            continue
        dest = dest_dir / child.name
        if child.is_dir() and child.name in COPY_DIRS:
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(child, dest)
        elif child.is_file() and child.name in COPY_FILES:
            shutil.copy2(child, dest)
    for markdown_path in dest_dir.rglob("*.md"):
        text = markdown_path.read_text(encoding="utf-8")
        text = re.sub(
            r"so that the coding agent \([^)]*\) knows exactly",
            "so that the coding agent knows exactly",
            text,
        )
        markdown_path.write_text(text, encoding="utf-8")
    (dest_dir / "LICENSE.txt").write_text(license_text, encoding="utf-8")
    (dest_dir / "SKILL.md").write_text(render_skill(skill), encoding="utf-8")
    changelog_path = dest_dir / "CHANGELOG.md"
    changelog = (
        changelog_path.read_text(encoding="utf-8")
        if changelog_path.exists()
        else f"# Changelog\n\nAll notable changes to the `{skill['dest']}` skill will be documented in this file.\n"
    )
    title = f"## [{DATE}] - Upstream Refresh and MCP Correction"
    if title not in changelog:
        first = re.search(r"^## ", changelog, flags=re.MULTILINE)
        entry = render_changelog_entry(skill)
        if first:
            changelog = changelog[: first.start()].rstrip() + "\n\n" + entry + "\n" + changelog[first.start() :]
        else:
            changelog = changelog.rstrip() + "\n\n" + entry
    changelog_path.write_text(changelog.rstrip() + "\n", encoding="utf-8")


def update_router_changelog(repo_root: Path) -> None:
    path = repo_root / "stitch-design" / "CHANGELOG.md"
    text = path.read_text(encoding="utf-8") if path.exists() else "# Changelog\n"
    text = text.replace("### Tested", "### Changed")
    title = f"## [{DATE}] - Stitch Skill Router Refresh"
    entry = f"""{title}

### Added

- Refreshed route selection for the dedicated Stitch skills imported from `{SOURCE_REPO}` at `{SOURCE_COMMIT}`.

### Changed

- Kept the Stitch Design skill as a lightweight router so detailed workflow guidance remains in narrower `stitch-*` skills.
- Preserved the verified design-system MCP boundary while refreshing compatible upstream support material.

### Fixed

- Prevented upstream screen-tool assumptions from overriding the host-verified fallback guidance.

"""
    if title not in text:
        first = re.search(r"^## ", text, flags=re.MULTILINE)
        if first:
            text = text[: first.start()].rstrip() + "\n\n" + entry + text[first.start():]
        else:
            text = text.rstrip() + "\n\n" + entry
    path.write_text(text, encoding="utf-8")


def update_registry(repo_root: Path) -> None:
    path = repo_root / "scripts" / "skill-registry.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("source_commits", {})["stitch_skills"] = {
        "repo": SOURCE_REPO,
        "commit": SOURCE_COMMIT,
    }
    fallback = [
        "Use local `.stitch/` artifacts, exported HTML or screenshots, bundled scripts, and the Stitch web UI when the host does not expose the needed Stitch MCP operation.",
        "Do not claim screen lookup, generation, editing, or variant MCP calls unless those tools are present in the active host tool list.",
    ]
    for name in ["stitch-design", *[skill["dest"] for skill in SKILLS]]:
        data.setdefault("mcp_skills", {})[name] = {
            "mode": "Primary",
            "servers": ["Stitch MCP"],
            "fallback": fallback,
        }
    refs = data.setdefault("reference_installs", {})
    refs["stitch-design"] = {
        "source_repo": SOURCE_REPO,
        "source_commit": SOURCE_COMMIT,
        "source_path": "local router for plugins/stitch-design, plugins/stitch-build, and plugins/stitch-utilities",
        "reason": "Entry point for routing Google Stitch work to the dedicated imported Stitch skills while preserving verified MCP boundaries.",
    }
    for skill in SKILLS:
        refs[skill["dest"]] = {
            "source_repo": SOURCE_REPO,
            "source_commit": SOURCE_COMMIT,
            "source_path": skill["source"],
            "reason": skill["reason"],
        }
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Path to a clone of google-labs-code/stitch-skills")
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    source_root = Path(args.source).resolve()
    license_text = (source_root / "LICENSE").read_text(encoding="utf-8")

    for skill in SKILLS:
        copy_support(repo_root, source_root, skill, license_text)

    stitch_design = repo_root / "stitch-design"
    stitch_design.mkdir(exist_ok=True)
    (stitch_design / "SKILL.md").write_text(render_router(), encoding="utf-8")
    (stitch_design / "LICENSE.txt").write_text(license_text, encoding="utf-8")
    update_router_changelog(repo_root)
    update_registry(repo_root)

    print(
        json.dumps(
            {
                "router": "stitch-design",
                "imported": [skill["dest"] for skill in SKILLS],
                "source_commit": SOURCE_COMMIT,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
