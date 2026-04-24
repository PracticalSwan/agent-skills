---
name: powerpoint-ppt
version: "1.0"
last_updated: 2026-04-24
tags: [slides, ppt, docs, writing, quality]
description: "PowerPoint (.pptx) manipulation via MCP server. Use for creating slides, formatting presentations, managing placeholders, adding images, applying templates, or extracting text from .pptx files."
---

# PowerPoint Presentation Workflows

> Tech Stack Target / Version: PowerPoint current desktop or web releases and `python-pptx` automation.

Use this skill when a `.pptx` deck is the output and slide composition matters.

## Current MCP Reality

Presentation MCP tooling is host-dependent. Some clients expose Office presentation tools directly, while others do not. Do not assume stable public tool names. If the current client lacks those tools, use the included local automation script or generate the content structure first and import it into PowerPoint.

## Activation Conditions

- Creating a deck from structured content
- Applying templates, branding, and slide layouts
- Updating text, images, or charts inside an existing presentation
- Extracting slide text for review or translation

## Practical Workflow

1. Confirm whether the client exposes presentation tools.
2. Prefer template-driven decks over manual one-off slide formatting.
3. Keep one idea per slide and treat text density as a defect.
4. Validate the final deck visually before calling it done.

## Anti-Patterns

- Writing for the author instead of the reader: It bakes in unstated context and leaves the actual audience unsure what to do next.
- Skipping concrete examples or commands: Abstract guidance is easy to approve and hard to apply correctly.
- Letting links, screenshots, or versions drift: Polished formatting does not help if the instructions are no longer true.

## Deck Checklist

- [ ] Title slide is present
- [ ] Slide layouts are consistent
- [ ] Fonts and colors match the template
- [ ] Images are high-resolution and not stretched
- [ ] Final slides were reviewed in slideshow size, not just as raw XML or text

## References & Resources

### Documentation
- [PowerPoint References](./references/) - Supporting notes for formatting, structure, and automation expectations

### Scripts
- [PPT Automation Script](./scripts/ppt-automation.py) - Local fallback for building or updating presentation content

### Examples
- [Presentation Examples](./examples/presentation-examples.md) - Example deck structures and content patterns

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:powerpoint-ppt` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py powerpoint-ppt` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: PowerPoint MCP

- Fallback prompt: "Use the PowerPoint Presentation Workflows skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- Use `python-pptx`, PowerPoint desktop, or a scriptable slide generator when the MCP surface is unavailable.
- Render the final deck and manually verify layout, overflow, and speaker-facing notes before delivery.

<!-- MCP:END -->

## Related Skills

- [documentation-authoring](../documentation-authoring/SKILL.md): Use it when the workflow also needs drafting structured technical or product documents.
- [documentation-patterns](../documentation-patterns/SKILL.md): Use it when the workflow also needs reusable documentation structures and templates.
- [documentation-quality](../documentation-quality/SKILL.md): Use it when the workflow also needs documentation review standards and quality gates.
- [documentation-verification](../documentation-verification/SKILL.md): Use it when the workflow also needs final documentation validation before publishing.
