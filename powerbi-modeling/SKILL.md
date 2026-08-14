---
name: powerbi-modeling
version: "2.0"
last_updated: 2026-08-14
tags: [powerbi, modeling, documents, automation, productivity]
description: "Power BI semantic models - DAX measures, star schemas, relationships, RLS, and performance tuning via MCP. Use when creating data models, writing DAX, or configuring table relationships in Power BI."
---
# Power BI Modeling

> Tech Stack Target / Version: Power BI Desktop current release, Tabular Editor, DAX Studio, and Fabric semantic-model workflows.

Use this skill when the work is inside a Power BI semantic model rather than a generic SQL schema or spreadsheet.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- Designing or cleaning up a star schema
- Creating or reviewing DAX measures
- Configuring relationships and cross-filter direction
- Implementing row-level security
- Auditing model health and performance

## Practical Workflow

1. Inspect the current model before changing anything.
2. Classify tables as dimension, fact, bridge, or helper tables.
3. Prefer explicit measures over implicit aggregation.
4. Keep relationships simple and single-direction unless the use case is proven.
5. Hide technical fields from report authors.

## MCP Reality

Power BI model tooling is host-specific. If your client exposes a Power BI modeling MCP server, inspect the available operations first and map them to the model areas you need: connections, tables, columns, measures, relationships, DAX queries, and security roles.

For Microsoft documentation, the Microsoft Learn MCP server is a good companion. Prefer:

- `microsoft_docs_search_by_product` with `power-bi`
- `microsoft_docs_fetch` for the final page

## Anti-Patterns

- Treating source content as already clean: Formatting automation will happily preserve broken or inconsistent input.
- Skipping an open-file verification pass: Documents and spreadsheets often fail in the destination app, not in the script output.
- Automating irreversible edits without checkpoints: A small mapping mistake can affect an entire workbook or document.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Powerbi Modeling implementation names the target runtime, framework version, and affected files.
2. Pass/fail: Build, lint, test, or equivalent local validation is run for the changed surface.
3. Pass/fail: Edge cases for errors, dependency drift, and environment differences are addressed or explicitly out of scope.
4. Pressure-test scenario: Apply the workflow to a change that passes happy-path tests but fails one boundary condition.
5. Success metric: Zero untested success claims; every implementation claim maps to a command or artifact.

## References & Resources

### Documentation
- [STAR-SCHEMA](./references/STAR-SCHEMA.md) - Dimension and fact modeling guidance
- [RELATIONSHIPS](./references/RELATIONSHIPS.md) - Relationship patterns and cross-filter tradeoffs
- [MEASURES-DAX](./references/MEASURES-DAX.md) - DAX naming and measure design
- [PERFORMANCE](./references/PERFORMANCE.md) - High-impact optimization ideas
- [RLS](./references/RLS.md) - Row-level security patterns

### Scripts
- [Power BI Model Audit](./scripts/powerbi-model-audit.py) - Local audit helper for naming, documentation, and modeling smells

### Examples
- [Model Examples](./examples/model-examples.md) - Example modeling patterns and DAX structure

<!-- MCP:START -->

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/powerbi-modeling` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: Power BI MCP

- Fallback prompt: "Use the Power BI Modeling skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- Use Power BI Desktop, Tabular Editor, DAX Studio, and exported model metadata when the MCP surface is unavailable.
- Validate measures, relationships, and performance with local model tools before completion.

<!-- MCP:END -->

## Related Skills

- [documentation-authoring](../documentation-authoring/SKILL.md): Use it when the workflow also needs drafting structured technical or product documents.
- [notion-docs](../notion-docs/SKILL.md): Use it when the workflow also needs Notion page and database publishing workflows.
- [pdf](../pdf/SKILL.md): Use it when the workflow also needs PDF extraction, generation, and layout-aware review.
- [word-document](../word-document/SKILL.md): Use it when the workflow also needs Word document authoring and formatting workflows.
