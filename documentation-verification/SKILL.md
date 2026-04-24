---
name: documentation-verification
version: "1.1"
last_updated: 2026-04-24
tags: [documentation, verification, docs, writing, quality]
description: "Validate documentation before merging - check completeness, broken links, code example accuracy, and factual correctness. Use when reviewing docs for quality gates or running pre-merge doc validation."
---

# Documentation Verification

Use this skill when a docs change needs evidence, not just a writing pass.

## Activation Conditions

- Reviewing docs before merge or release
- Checking README, setup, or config accuracy
- Verifying local links, commands, and code samples
- Confirming docs changed alongside user-facing behavior

## Verification Workflow

1. Confirm the docs cover the changed behavior.
2. Check relative links and referenced files.
3. Validate commands and snippets where feasible.
4. Report missing coverage and stale claims explicitly.

## Anti-Patterns

- Writing for the author instead of the reader: It bakes in unstated context and leaves the actual audience unsure what to do next.
- Skipping concrete examples or commands: Abstract guidance is easy to approve and hard to apply correctly.
- Letting links, screenshots, or versions drift: Polished formatting does not help if the instructions are no longer true.

## Review Checklist

- [ ] Public behavior changes are documented
- [ ] Local links resolve
- [ ] Examples and commands still make sense
- [ ] Setup steps reflect current tool versions
- [ ] README and CHANGELOG were updated when required

## References & Resources

### Documentation
- [Validation Procedures](./references/validation.md) - Practical checks for links, examples, config, and coverage

### Scripts
- [Doc Link Check](./scripts/doc-link-check.py) - Validate relative Markdown links across one file or an entire docs tree

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:documentation-verification` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py documentation-verification` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the Documentation Verification skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [documentation-authoring](../documentation-authoring/SKILL.md): Use it when the workflow also needs drafting structured technical or product documents.
- [documentation-patterns](../documentation-patterns/SKILL.md): Use it when the workflow also needs reusable documentation structures and templates.
- [documentation-quality](../documentation-quality/SKILL.md): Use it when the workflow also needs documentation review standards and quality gates.
- [notion-docs](../notion-docs/SKILL.md): Use it when the workflow also needs Notion page and database publishing workflows.
