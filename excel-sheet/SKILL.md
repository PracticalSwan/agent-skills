---
name: excel-sheet
version: "1.3"
last_updated: 2026-07-11
tags: [spreadsheet, sheet, documents, automation, productivity]
description: "Excel (.xlsx) manipulation via MCP server. Use for creating workbooks, formatting cells, writing formulas, building charts, pivot tables, data analysis, or any task involving Excel spreadsheets."
---
# Excel Spreadsheet Workflows

> Tech Stack Target / Version: Excel desktop or `openpyxl`-based spreadsheet automation with current OOXML-compatible workflows.

Use this skill when the deliverable is an `.xlsx` workbook or when spreadsheet structure matters.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Current MCP Reality

Excel MCP tooling is host-dependent. In GitHub Copilot, Excel actions may appear as grouped Office tools. In Codex or Claude, those tools may be absent entirely. Treat the included Python script as the reliable fallback.

## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- Creating or updating workbooks
- Converting CSV data into structured Excel output
- Applying formulas, formatting, charts, or pivots
- Producing spreadsheet deliverables when layout matters

## Practical Workflow

1. Confirm whether the client exposes spreadsheet MCP tools.
2. If yes, inspect the actual tool names before assuming a wrapper exists.
3. If no, use the local converter or author the workbook with `openpyxl`.
4. Validate formulas and chart ranges before claiming the workbook is ready.

## MCP Fallback – Native Automation

When MCP is unavailable, use native automation: `openpyxl` for `.xlsx`, CSV export for flat data, and manual formula inspection for high-risk calculations. Preserve formulas, number formats, sheet names, hidden sheets, and workbook metadata, then reopen or parse the workbook before claiming success.

## Anti-Patterns

- Treating source content as already clean: Formatting automation will happily preserve broken or inconsistent input.
- Skipping an open-file verification pass: Documents and spreadsheets often fail in the destination app, not in the script output.
- Automating irreversible edits without checkpoints: A small mapping mistake can affect an entire workbook or document.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Excel Sheet artifact type, target format, and required output fidelity are stated before editing.
2. Pass/fail: MCP availability is checked and the native automation fallback path is named when MCP is absent.
3. Pass/fail: The produced file or formula is opened, parsed, rendered, or otherwise validated locally.
4. Pressure-test scenario: Apply the workflow to a file with formatting, metadata, or conversion edge cases and verify nothing important is lost.
5. Success metric: Zero unverified document claims; the artifact itself is the evidence.

## Workbook Checklist

- [ ] Sheets are named clearly
- [ ] Headers are formatted consistently
- [ ] Formulas are used instead of hardcoded derived values
- [ ] Charts reference the correct ranges
- [ ] Frozen panes or filters are applied where useful

## References & Resources

### Documentation
- [Excel Formulas Reference](./references/excel-formulas-reference.md) - Formula patterns, lookup guidance, and Power Query notes

### Scripts
- [CSV to XLSX Converter](./scripts/csv-to-xlsx.py) - Local fallback for generating formatted Excel workbooks from CSV input

### Examples
- [Excel Workbook Examples](./examples/excel-workbook-examples.md) - Example workbook structures and automation patterns

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:excel-sheet` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py excel-sheet` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: Excel MCP

- Fallback prompt: "Use the Excel Spreadsheet Workflows skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- Use `scripts/csv-to-xlsx.py`, `openpyxl`, or desktop Excel when the spreadsheet MCP surface is missing.
- Re-open the generated workbook locally to verify formulas, ranges, and frozen panes.

<!-- MCP:END -->

## Related Skills

- [documentation-authoring](../documentation-authoring/SKILL.md): Use it when the workflow also needs drafting structured technical or product documents.
- [notion-docs](../notion-docs/SKILL.md): Use it when the workflow also needs Notion page and database publishing workflows.
- [pdf](../pdf/SKILL.md): Use it when the workflow also needs PDF extraction, generation, and layout-aware review.
- [word-document](../word-document/SKILL.md): Use it when the workflow also needs Word document authoring and formatting workflows.
