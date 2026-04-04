---
name: spreadsheet-formula-helper
description: Write and debug spreadsheet formulas (Excel/Google Sheets), pivot tables, and array formulas; translate between dialects; use when users need working formulas with examples and edge-case checks.
metadata:
  short-description: Build/debug Excel or Sheets formulas
---
# Spreadsheet Formula Helper

Produce reliable spreadsheet formulas with explanations.

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

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:spreadsheet-formula-helper` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py spreadsheet-formula-helper` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

No dedicated MCP server is required for the normal workflow in this skill.

- If the current host lacks an equivalent tool surface, use the bundled scripts, standard shell or editor tooling, and the manual workflow already described in this skill.
- Treat local verification as the fallback evidence path before closing the task.

<!-- MCP:END -->
