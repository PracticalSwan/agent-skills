---
name: word-document
version: "1.2"
last_updated: 2026-04-25
tags: [docs, document, writing, quality, templates]
description: "Word (.docx) manipulation via MCP server. Use for reading, creating, editing, formatting Word documents including tables, footnotes, comments, images, headers, styles, and PDF conversion."
---

# Word Document Workflows

> Tech Stack Target / Version: Word desktop or `python-docx` automation with current OOXML-compatible workflows.

Use this skill when `.docx` layout and document structure matter, not just the raw text.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Current MCP Reality

Microsoft publicly documents a Word MCP server in the Microsoft 365 Agents Toolkit preview, but tool availability still depends on the host. In GitHub Copilot you may see Word-specific tools; in other clients they may be missing. If direct Word MCP access is unavailable, use the included local script workflow.

## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- Creating or editing `.docx` reports, memos, or structured deliverables
- Applying headings, tables, images, or styles
- Reviewing or extracting document structure
- Preparing Word output before a later PDF conversion

## Practical Workflow

1. Confirm whether the client exposes Word MCP capabilities.
2. Start with structure: title, headings, sections, tables.
3. Apply styling consistently only after the structure is right.
4. Validate comments, footnotes, and references before export.
5. Use the local generator script when MCP access is unavailable.

## MCP Fallback – Native Automation

When MCP is unavailable, use native automation: `python-docx` for `.docx`, direct OOXML inspection for unsupported structures, and PDF export checks when layout matters. Preserve styles, tables, headers, footers, comments, tracked-change expectations, and metadata, then reopen or parse the document before claiming success.

## Anti-Patterns

- Writing for the author instead of the reader: It bakes in unstated context and leaves the actual audience unsure what to do next.
- Skipping concrete examples or commands: Abstract guidance is easy to approve and hard to apply correctly.
- Letting links, screenshots, or versions drift: Polished formatting does not help if the instructions are no longer true.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Word Document artifact type, target format, and required output fidelity are stated before editing.
2. Pass/fail: MCP availability is checked and the native automation fallback path is named when MCP is absent.
3. Pass/fail: The produced file or formula is opened, parsed, rendered, or otherwise validated locally.
4. Pressure-test scenario: Apply the workflow to a file with formatting, metadata, or conversion edge cases and verify nothing important is lost.
5. Success metric: Zero unverified document claims; the artifact itself is the evidence.


## Document Checklist

- [ ] Heading hierarchy is clear
- [ ] Tables are readable and consistently styled
- [ ] Comments or review notes are intentional
- [ ] Placeholder text is removed
- [ ] The final document was re-opened or otherwise verified after generation

## References & Resources

### Documentation
- [DOCX Formatting Reference](./references/docx-formatting-reference.md) - Practical formatting notes and document structure guidance

### Scripts
- [DOC Template Generator](./scripts/doc-template-generator.py) - Local fallback for generating Word-ready document structures

### Examples
- [Report Generation Example](./examples/report-generation-example.md) - Example report workflow for `.docx` output

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:word-document` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py word-document` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: Word Document MCP

- Fallback prompt: "Use the Word Document Workflows skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- Use `python-docx`, Word desktop, or document export scripts when the MCP surface is unavailable.
- Re-open or render the document locally so formatting, comments, and pagination are verified before delivery.

<!-- MCP:END -->

## Related Skills

- [documentation-authoring](../documentation-authoring/SKILL.md): Use it when the workflow also needs drafting structured technical or product documents.
- [documentation-patterns](../documentation-patterns/SKILL.md): Use it when the workflow also needs reusable documentation structures and templates.
- [documentation-quality](../documentation-quality/SKILL.md): Use it when the workflow also needs documentation review standards and quality gates.
- [documentation-verification](../documentation-verification/SKILL.md): Use it when the workflow also needs final documentation validation before publishing.
