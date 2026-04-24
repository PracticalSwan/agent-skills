---
name: pdf
version: "1.2"
last_updated: 2026-04-25
tags: [pdf, docs, writing, quality, templates]
description: "Use when tasks involve reading, creating, or reviewing PDF files where rendering and layout matter; prefer visual checks by rendering pages (Poppler) and use Python tools such as `reportlab`, `pdfplumber`, and `pypdf` for generation and extraction."
---

# PDF Skill

> Tech Stack Target / Version: PDF extraction, OCR-capable tooling, conversion scripts, and Acrobat-compatible review workflows.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## When to use
Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- Read or review PDF content where layout and visuals matter.
- Create PDFs programmatically with reliable formatting.
- Validate final rendering before delivery.

## Workflow
1. Prefer visual review: render PDF pages to PNGs and inspect them.
   - Use `pdftoppm` if available.
   - If unavailable, install Poppler or ask the user to review the output locally.
2. Use `reportlab` to generate PDFs when creating new documents.
3. Use `pdfplumber` (or `pypdf`) for text extraction and quick checks; do not rely on it for layout fidelity.
4. After each meaningful update, re-render pages and verify alignment, spacing, and legibility.

## Temp and output conventions
- Use `tmp/pdfs/` for intermediate files; delete when done.
- Write final artifacts under `output/pdf/` when working in this repo.
- Keep filenames stable and descriptive.

## Dependencies (install if missing)
Prefer `uv` for dependency management.

Python packages:
```
uv pip install reportlab pdfplumber pypdf
```
If `uv` is unavailable:
```
python3 -m pip install reportlab pdfplumber pypdf
```
System tools (for rendering):
```
# macOS (Homebrew)
brew install poppler

# Ubuntu/Debian
sudo apt-get install -y poppler-utils
```

If installation isn't possible in this environment, tell the user which dependency is missing and how to install it locally.

## Environment
No required environment variables.

## Rendering command
```
pdftoppm -png $INPUT_PDF $OUTPUT_PREFIX
```

## Quality expectations
- Maintain polished visual design: consistent typography, spacing, margins, and section hierarchy.
- Avoid rendering issues: clipped text, overlapping elements, broken tables, black squares, or unreadable glyphs.
- Charts, tables, and images must be sharp, aligned, and clearly labeled.
- Use ASCII hyphens only. Avoid U+2011 (non-breaking hyphen) and other Unicode dashes.
- Citations and references must be human-readable; never leave tool tokens or placeholder strings.

## Final checks
- Do not deliver until the latest PNG inspection shows zero visual or formatting defects.
- Confirm headers/footers, page numbering, and section transitions look polished.
- Keep intermediate files organized or remove them after final approval.

## Anti-Patterns

- Writing for the author instead of the reader: It bakes in unstated context and leaves the actual audience unsure what to do next.
- Skipping concrete examples or commands: Abstract guidance is easy to approve and hard to apply correctly.
- Letting links, screenshots, or versions drift: Polished formatting does not help if the instructions are no longer true.

<!-- PORTABILITY:START -->

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The PDF artifact type, target format, and required output fidelity are stated before editing.
2. Pass/fail: MCP availability is checked and the native automation fallback path is named when MCP is absent.
3. Pass/fail: The produced file or formula is opened, parsed, rendered, or otherwise validated locally.
4. Pressure-test scenario: Apply the workflow to a file with formatting, metadata, or conversion edge cases and verify nothing important is lost.
5. Success metric: Zero unverified document claims; the artifact itself is the evidence.


## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:pdf` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py pdf` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the PDF Skill skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [documentation-authoring](../documentation-authoring/SKILL.md): Use it when the workflow also needs drafting structured technical or product documents.
- [documentation-patterns](../documentation-patterns/SKILL.md): Use it when the workflow also needs reusable documentation structures and templates.
- [documentation-quality](../documentation-quality/SKILL.md): Use it when the workflow also needs documentation review standards and quality gates.
- [documentation-verification](../documentation-verification/SKILL.md): Use it when the workflow also needs final documentation validation before publishing.
