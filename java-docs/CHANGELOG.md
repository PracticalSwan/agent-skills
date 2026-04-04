# Changelog

All notable changes to the `java-docs` skill will be documented in this file.

## [2026-04-04] - Initial Import and Portability Upgrade

### Added
- Imported this skill from `https://github.com/github/awesome-copilot` at `skills/java-docs`.
- Added cross-client portability guidance for GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- Added the repo-standard MCP or no-MCP fallback guidance for this skill.

### Changed
- Rewrote the frontmatter description to match the activation-focused style used by the maintained catalog.

### Tested
- Validated `SKILL.md` frontmatter and Gemini command export readiness with `python scripts/validate-skills.py`.
