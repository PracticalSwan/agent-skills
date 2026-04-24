# Changelog

## [2026-04-24] - Version 1.1 Refresh

### Changed
- Updated the SKILL frontmatter version to `1.1` for the 2026-04-24 catalog refresh.
- Added an "Optimized for ..." note at the top so the guidance is anchored to current platform versions.

All notable changes to the `csharp-xunit` skill will be documented in this file.

## [2026-04-24] - Skill Refresh

### Changed
- Standardized the SKILL frontmatter with version metadata, last-updated date, tags, and a concise catalog description.
- Reformatted the portability and MCP guidance with a preferred server line, a copy-paste fallback prompt, and consistent bullet lists.
- Added a catalog-standard Anti-Patterns section and refreshed the Related Skills links at the end of the skill.
- Added an explicit before-and-after example, current-version targeting note, and a Common Pitfalls section for modern xUnit usage.
## [2026-04-04] - Initial Import and Portability Upgrade

### Added
- Imported this skill from `https://github.com/github/awesome-copilot` at `skills/csharp-xunit`.
- Added cross-client portability guidance for GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- Added the repo-standard MCP or no-MCP fallback guidance for this skill.

### Changed
- Rewrote the frontmatter description to match the activation-focused style used by the maintained catalog.

### Tested
- Validated `SKILL.md` frontmatter and Gemini command export readiness with `python scripts/validate-skills.py`.
