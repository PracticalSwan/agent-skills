---
name: documentation-patterns
version: "2.0"
last_updated: 2026-08-24
tags: [documentation, patterns, docs, writing, quality]
description: "Templates and structural patterns for API docs, feature docs, config guides, and REST endpoint documentation. Use when structuring docs, applying Markdown templates, or standardizing doc formats."
---
# Documentation Patterns

Use this skill when the main problem is document shape and consistency rather than writing quality alone.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- Creating a new API, feature, or config guide
- Standardizing Markdown sections across repositories
- Writing migration or runbook documents
- Picking the right template for a doc request

## Pattern Selection

- API docs: endpoints, auth, request and response schema, errors
- Feature docs: purpose, UX, dependencies, rollout, support
- Config docs: env vars, defaults, examples, failure modes
- Migration docs: changed behavior, upgrade path, verification

## Cross-Skill Workflow

- Use [documentation-authoring](../documentation-authoring/SKILL.md) to gather context and draft the content before template selection becomes the bottleneck.
- Use this skill when structure, section order, or template choice is the main problem.
- Finish with [documentation-quality](../documentation-quality/SKILL.md) to review the final document against quality expectations.

## Agent Prompt Template

```text
Use the documentation-patterns skill to choose and apply the best structure for a [document type].
Context: [feature, system, migration, or runbook].
Bias toward: [API docs, feature docs, config guide, migration guide, etc.].
Return the recommended section outline with short notes on why each section exists.
```

## Shared Documentation Stack

Use this as the inherited baseline for documentation-authoring, documentation-quality, documentation-automation, and documentation-verification.

1. Source of truth: identify owner, audience, canonical files, and freshness requirements before drafting.
2. Structure: choose the smallest reusable pattern that fits the reader task.
3. Verification: check links, commands, examples, screenshots, and version-sensitive claims before publishing.
4. Handoff: state unresolved gaps, owners, and next review trigger instead of implying false completeness.

## Anti-Patterns

- Writing for the author instead of the reader: It bakes in unstated context and leaves the actual audience unsure what to do next.
- Skipping concrete examples or commands: Abstract guidance is easy to approve and hard to apply correctly.
- Letting links, screenshots, or versions drift: Polished formatting does not help if the instructions are no longer true.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Documentation Patterns output identifies audience, purpose, source of truth, and freshness requirements.
2. Pass/fail: Shared documentation-stack guidance is referenced instead of duplicating another documentation skill.
3. Pass/fail: Claims, links, commands, examples, and screenshots are verified or explicitly marked unverified.
4. Pressure-test scenario: Apply the skill to a doc request with a stale command, missing owner, and conflicting audience.
5. Success metric: Zero undocumented assumptions; every reader-facing claim is sourced or scoped.

## References & Resources

### Documentation
- [API Documentation Templates](./references/api-templates.md) - Endpoint, SDK, and function documentation patterns
- [Feature Documentation Templates](./references/feature-templates.md) - Feature overview, rollout, and troubleshooting patterns
- [Configuration Documentation Templates](./references/config-templates.md) - Config and environment variable templates

### Scripts
- [Doc Template Picker](./scripts/doc-template-picker.py) - Print a starter Markdown template for `api`, `feature`, `config`, or `migration`

<!-- MCP:START -->

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/documentation-patterns` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the Documentation Patterns skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [documentation-authoring](../documentation-authoring/SKILL.md): Use it when the workflow also needs drafting structured technical or product documents.
- [documentation-quality](../documentation-quality/SKILL.md): Use it when the workflow also needs documentation review standards and quality gates.
- [documentation-verification](../documentation-verification/SKILL.md): Use it when the workflow also needs final documentation validation before publishing.
- [notion-docs](../notion-docs/SKILL.md): Use it when the workflow also needs Notion page and database publishing workflows.
