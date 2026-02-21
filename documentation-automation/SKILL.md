---
name: documentation-automation
description: Documentation automation tools, JSDoc/TSDoc integration, linters, and pre-commit hooks. Use when automating doc generation, setting up doc linting, configuring pre-commit checks, integrating JSDoc or TSDoc, or ensuring doc builds succeed. Triggered by keywords like documentation automation, JSDoc, TSDoc, doc linters, markdownlint, pre-commit hooks, automated documentation.
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