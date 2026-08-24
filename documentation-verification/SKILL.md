---
name: documentation-verification
version: "2.0"
last_updated: 2026-08-24
tags: [documentation, verification, docs, writing, quality]
description: "Validate documentation before merging - check completeness, broken links, code example accuracy, and factual correctness. Use when reviewing docs for quality gates or running pre-merge doc validation."
---
# Documentation Verification

Use this skill when a docs change needs evidence, not just a writing pass.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- Reviewing docs before merge or release
- Checking README, setup, or config accuracy
- Verifying local links, commands, and code samples
- Confirming docs changed alongside user-facing behavior

## Verification Workflow

1. Confirm the docs cover the changed behavior.
2. Check relative links and referenced files.
3. Validate commands and snippets where feasible.
4. Report missing coverage and stale claims explicitly.

## Documentation Stack Reference

Inherit the shared stack from [documentation-patterns](../documentation-patterns/SKILL.md#shared-documentation-stack): source-of-truth discovery, audience framing, structure selection, verification, and freshness checks. Keep this skill focused on final evidence checks instead of restating the full stack.

## Anti-Patterns

- Writing for the author instead of the reader: It bakes in unstated context and leaves the actual audience unsure what to do next.
- Skipping concrete examples or commands: Abstract guidance is easy to approve and hard to apply correctly.
- Letting links, screenshots, or versions drift: Polished formatting does not help if the instructions are no longer true.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Documentation Verification output identifies audience, purpose, source of truth, and freshness requirements.
2. Pass/fail: Shared documentation-stack guidance is referenced instead of duplicating another documentation skill.
3. Pass/fail: Claims, links, commands, examples, and screenshots are verified or explicitly marked unverified.
4. Pressure-test scenario: Apply the skill to a doc request with a stale command, missing owner, and conflicting audience.
5. Success metric: Zero undocumented assumptions; every reader-facing claim is sourced or scoped.

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

<!-- MCP:START -->

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/documentation-verification` and restart Codex after major changes.

<!-- PORTABILITY:END -->

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
