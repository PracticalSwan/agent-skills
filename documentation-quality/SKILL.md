---
name: documentation-quality
description: Documentation quality standards and writing principles. Use when establishing formatting rules, reviewing doc quality metrics, creating writing guidelines, or enforcing consistent documentation style across a project.
license: Complete terms in LICENSE.txt
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

## Quality Checklist

- [ ] Title and purpose are clear
- [ ] Heading levels do not jump unexpectedly
- [ ] Code examples have language tags and realistic inputs
- [ ] Commands match current tooling
- [ ] Links and file paths are accurate

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

No dedicated MCP server is required for the normal workflow in this skill.

- If the current host lacks an equivalent tool surface, use the bundled scripts, standard shell or editor tooling, and the manual workflow already described in this skill.
- Treat local verification as the fallback evidence path before closing the task.

<!-- MCP:END -->

## Related Skills
| Skill | Relationship |
|-------|-------------|
| [documentation-authoring](../documentation-authoring/SKILL.md) | Apply quality standards during doc creation |
| [documentation-verification](../documentation-verification/SKILL.md) | Verify quality metrics before merging docs |
| [documentation-patterns](../documentation-patterns/SKILL.md) | Patterns that enforce quality consistency |
