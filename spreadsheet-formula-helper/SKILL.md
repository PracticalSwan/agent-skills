---
name: spreadsheet-formula-helper
version: "1.3"
last_updated: 2026-07-11
tags: [spreadsheet, formula, helper, documents, automation]
description: "Write and debug spreadsheet formulas (Excel/Google Sheets), pivot tables, and array formulas; translate between dialects; use when users need working formulas with examples and edge-case checks."
---
# Spreadsheet Formula Helper

Produce reliable spreadsheet formulas with explanations.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Inputs to gather
- Platform (Excel/Sheets), locale (comma vs. semicolon separators), sample data layout (headers, ranges), expected outputs, and constraints (volatile functions allowed?).
- Provide small example rows and the desired result for them.

## Workflow
1) Restate the problem with explicit ranges and sheet names; propose a minimal sample to verify.
2) Draft formula(s); when dynamic arrays are available, prefer them over copy-down formulas.
3) Explain how it works and where to place it; include named ranges if helpful.
4) Edge cases: blank rows, mixed types, timezone/date quirks, duplicates; offer guardrails (e.g., `IFERROR`, `LET`, `LAMBDA`).
5) Variants: if porting between Excel and Sheets, provide both versions.

## Output
- Primary formula, short explanation, and a 2-3 row worked example showing inputs to outputs.
- Optional: quick troubleshooting checklist for common errors.

## MCP Fallback – Native Automation

When MCP is unavailable, use native automation: local spreadsheet formulas, `openpyxl` for workbook inspection, CSV fixtures for examples, and manual recalculation notes for functions the local engine cannot evaluate. Preserve locale separators, absolute references, dynamic arrays, and Excel-vs-Sheets differences before claiming success.

## Anti-Patterns

- Treating source content as already clean: Formatting automation will happily preserve broken or inconsistent input.
- Skipping an open-file verification pass: Documents and spreadsheets often fail in the destination app, not in the script output.
- Automating irreversible edits without checkpoints: A small mapping mistake can affect an entire workbook or document.

<!-- PORTABILITY:START -->

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Spreadsheet Formula Helper artifact type, target format, and required output fidelity are stated before editing.
2. Pass/fail: MCP availability is checked and the native automation fallback path is named when MCP is absent.
3. Pass/fail: The produced file or formula is opened, parsed, rendered, or otherwise validated locally.
4. Pressure-test scenario: Apply the workflow to a file with formatting, metadata, or conversion edge cases and verify nothing important is lost.
5. Success metric: Zero unverified document claims; the artifact itself is the evidence.

## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:spreadsheet-formula-helper` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py spreadsheet-formula-helper` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the Spreadsheet Formula Helper skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [documentation-authoring](../documentation-authoring/SKILL.md): Use it when the workflow also needs drafting structured technical or product documents.
- [notion-docs](../notion-docs/SKILL.md): Use it when the workflow also needs Notion page and database publishing workflows.
- [pdf](../pdf/SKILL.md): Use it when the workflow also needs PDF extraction, generation, and layout-aware review.
- [word-document](../word-document/SKILL.md): Use it when the workflow also needs Word document authoring and formatting workflows.
