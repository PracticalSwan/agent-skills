---
name: documentation-automation
description: Automate doc generation with JSDoc/TSDoc, linters, and pre-commit hooks. Use when setting up markdownlint, configuring doc linting pipelines, integrating JSDoc/TSDoc, or building automated documentation workflows.
license: Complete terms in LICENSE.txt
---

# Documentation Automation

## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

## Activation Conditions

Use this skill when:
- Setting up automated documentation generation
- Configuring JSDoc/TSDoc for JS/TS projects
- Implementing documentation linting
- Adding pre-commit doc validation
- Integrating documentation generators

## Documentation Generation Tools

See [Automated Tools](./references/tools.md) for:
- JSDoc/TSDoc for JavaScript/TypeScript
- Sphinx/pdoc for Python
- Javadoc for Java
- xmldoc for C#
- godoc for Go
- rustdoc for Rust

## Documentation Linting

**Validate documentation with:**
- Markdown linters: `markdownlint`, `remark-lint`
- Link checkers: `markdown-link-check`, `lychee`
- Spell checkers: `cspell`, `aspell`
- Code example validators

## Pre-Commit Hooks

**Add pre-commit checks for:**
- Documentation build succeeds
- No broken links
- Code examples are valid
- Changelog entry exists for changes
- Markdown formatting is clean

## Example Configuration

```json
{
  "scripts": {
    "docs:build": "Build documentation",
    "docs:test": "Test code examples in docs",
    "docs:lint": "Lint documentation files",
    "docs:links": "Check for broken links",
    "docs:spell": "Spell check documentation",
    "docs:validate": "Run all documentation checks"
  }
}

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [documentation-authoring](../documentation-authoring/SKILL.md) | Generate docs that automation tools process |
| [devops-tooling](../devops-tooling/SKILL.md) | Pre-commit hooks and CI pipeline integration |
| [documentation-verification](../documentation-verification/SKILL.md) | Automated validation in doc pipelines |

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [documentation-authoring](../documentation-authoring/SKILL.md) | Generate docs that automation tools process |
| [devops-tooling](../devops-tooling/SKILL.md) | Pre-commit hooks and CI pipeline integration |
| [documentation-verification](../documentation-verification/SKILL.md) | Automated validation in doc pipelines |
