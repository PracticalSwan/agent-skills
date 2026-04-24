---
name: documentation-quality
version: "1.1"
last_updated: 2026-04-24
tags: [documentation, quality, docs, writing, templates]
description: "Documentation quality standards and writing principles. Use when establishing formatting rules, reviewing doc quality metrics, creating writing guidelines, or enforcing consistent documentation style across a project."
---

# Documentation Quality Standards

Use this skill when documentation should be judged against explicit standards instead of subjective preference.

## Activation Conditions

- Reviewing docs before merge
- Creating or updating a style guide
- Defining expectations for examples, structure, and terminology
- Auditing a docs set for consistency and readability

## Core Standards

- Clear audience and scope
- Stable heading hierarchy
- Runnable or honest examples
- Consistent terminology
- Explicit edge cases, constraints, and failure modes

## Anti-Patterns

- Writing for the author instead of the reader: It bakes in unstated context and leaves the actual audience unsure what to do next.
- Skipping concrete examples or commands: Abstract guidance is easy to approve and hard to apply correctly.
- Letting links, screenshots, or versions drift: Polished formatting does not help if the instructions are no longer true.

## Quality Checklist

- [ ] Title and purpose are clear
- [ ] Heading levels do not jump unexpectedly
- [ ] Code examples have language tags and realistic inputs
- [ ] Commands match current tooling
- [ ] Links and file paths are accurate

## Cross-Skill Workflow

- Use [documentation-authoring](../documentation-authoring/SKILL.md) when the content itself still needs to be drafted or clarified.
- Use [documentation-patterns](../documentation-patterns/SKILL.md) when the review shows that the problem is document shape rather than wording.
- Use this skill as the final standards check before publish or merge.

## Agent Prompt Template

```text
Use the documentation-quality skill to review this document against explicit standards.
Artifact: [file or pasted draft].
Audience: [who will read it].
Check for clarity, completeness, accurate examples, terminology consistency, and stale references.
Report concrete findings first, then suggest the smallest high-value fixes.
```

## References & Resources

### Documentation
- [Writing Standards](./references/writing-standards.md) - Clarity, example quality, terminology, and formatting guidance

### Scripts
- [Doc Style Audit](./scripts/doc-style-audit.py) - Check Markdown files for heading jumps, long lines, tabs, and trailing whitespace

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:documentation-quality` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py documentation-quality` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the Documentation Quality Standards skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [documentation-authoring](../documentation-authoring/SKILL.md): Use it when the workflow also needs drafting structured technical or product documents.
- [documentation-patterns](../documentation-patterns/SKILL.md): Use it when the workflow also needs reusable documentation structures and templates.
- [documentation-verification](../documentation-verification/SKILL.md): Use it when the workflow also needs final documentation validation before publishing.
- [notion-docs](../notion-docs/SKILL.md): Use it when the workflow also needs Notion page and database publishing workflows.
