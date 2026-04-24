# Changelog

## [2026-04-25] - Version 1.2 Verification Protocol Refresh

### Added
- Added a `Verification Protocol` section with skill-specific pass/fail checks, one pressure-test scenario, and a measurable success metric.
- Added guidance to leverage native parallel subagent dispatch and 200k+ context windows where available.

### Changed
- Updated `SKILL.md` frontmatter to `version: "1.2"` and `last_updated: 2026-04-25`.
- Reframed activation guidance toward symptom -> action triggers and standardized two-stage review wording where applicable.

## [2026-04-24] - Version 1.1 Refresh

### Changed
- Updated the SKILL frontmatter version to `1.1` for the 2026-04-24 catalog refresh.
- Added an "Optimized for ..." note at the top so the guidance is anchored to current platform versions.

All notable changes to the `dotnet-best-practices` skill will be documented in this file.

## [2026-04-24] - Skill Refresh

### Changed
- Standardized the SKILL frontmatter with version metadata, last-updated date, tags, and a concise catalog description.
- Reformatted the portability and MCP guidance with a preferred server line, a copy-paste fallback prompt, and consistent bullet lists.
- Added a catalog-standard Anti-Patterns section and refreshed the Related Skills links at the end of the skill.
- Added an explicit before-and-after example and a Common Pitfalls section for modern .NET implementation guidance.
## [2026-04-04] - Initial Import and Portability Upgrade

### Added
- Imported this skill from `https://github.com/github/awesome-copilot` at `skills/dotnet-best-practices`.
- Added cross-client portability guidance for GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- Added the repo-standard MCP or no-MCP fallback guidance for this skill.

### Changed
- Rewrote the description and scope wording so the guidance applies cleanly across clients and no longer depends on a host-specific `${selection}` placeholder.

### Tested
- Validated `SKILL.md` frontmatter and Gemini command export readiness with `python scripts/validate-skills.py`.
