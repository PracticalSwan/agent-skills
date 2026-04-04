# Changelog

All notable changes to the `spreadsheet-formula-helper` skill will be documented in this file.

## [2026-04-04] - Initial Import and Portability Upgrade

### Added
- Imported this skill from `https://github.com/ComposioHQ/awesome-codex-skills` at `spreadsheet-formula-helper`.
- Added cross-client portability guidance for GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- Added the repo-standard MCP or no-MCP fallback guidance for this skill.

### Changed
- Normalized the output wording so the main example line stays ASCII-friendly across hosts.

### Tested
- Validated `SKILL.md` frontmatter and Gemini command export readiness with `python scripts/validate-skills.py`.
