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

All notable changes to the `codebase-to-course` skill will be documented in this file.

## [2026-04-24] - Skill Refresh

### Changed
- Standardized the SKILL frontmatter with version metadata, last-updated date, tags, and a concise catalog description.
- Reformatted the portability and MCP guidance with a preferred server line, a copy-paste fallback prompt, and consistent bullet lists.
- Added a catalog-standard Anti-Patterns section and refreshed the Related Skills links at the end of the skill.
## [2026-04-24] - Initial Import and Portability Upgrade

### Added
- Imported the skill from `https://github.com/zarazhangrui/codebase-to-course` at `ff8837ecf8e9f6ce9874ffa42e42633394a52a00`.
- Imported the upstream `references/` course template assets used by the skill.
- Added cross-client portability guidance for GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- Added the repo-standard no-MCP fallback guidance for this skill.

### Changed
- Clarified that parallel delegated-agent module writing depends on host support and user approval.

### Tested
- Validated `SKILL.md` frontmatter and Gemini command export readiness with `python scripts/validate-skills.py`.
