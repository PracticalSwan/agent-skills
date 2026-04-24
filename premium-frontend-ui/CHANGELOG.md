# Changelog

## [2026-04-25] - Version 1.2 Verification Protocol Refresh

### Added
- Added a `Verification Protocol` section with skill-specific pass/fail checks, one pressure-test scenario, and a measurable success metric.
- Added guidance to leverage native parallel subagent dispatch and 200k+ context windows where available.
- Added or referenced the shared Component Review Rubric for frontend component review.

### Changed
- Updated `SKILL.md` frontmatter to `version: "1.2"` and `last_updated: 2026-04-25`.
- Reframed activation guidance toward symptom -> action triggers and standardized two-stage review wording where applicable.

## [2026-04-24] - Version 1.1 Refresh

### Changed
- Updated the SKILL frontmatter version to `1.1` for the 2026-04-24 catalog refresh.

All notable changes to the `premium-frontend-ui` skill will be documented in this file.

## [2026-04-24] - Skill Refresh

### Changed
- Standardized the SKILL frontmatter with version metadata, last-updated date, tags, and a concise catalog description.
- Reformatted the portability and MCP guidance with a preferred server line, a copy-paste fallback prompt, and consistent bullet lists.
- Added a catalog-standard Anti-Patterns section and refreshed the Related Skills links at the end of the skill.
## [2026-04-24] - Upstream Metadata Refresh

### Changed
- Added upstream author metadata from `https://github.com/github/awesome-copilot` commit `63d08d51f792d53feec8c1c06897cee870e83c18`.

### Tested
- Confirmed the current upstream change for this skill is limited to `SKILL.md` frontmatter metadata.

## [2026-04-04] - Initial Import and Portability Upgrade

### Added
- Imported this skill from `https://github.com/github/awesome-copilot` at `skills/premium-frontend-ui`.
- Added cross-client portability guidance for GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- Added the repo-standard MCP or no-MCP fallback guidance for this skill.

### Changed
- Rewrote the activation description and opening guidance to be host-neutral instead of Copilot-specific.

### Tested
- Validated `SKILL.md` frontmatter and Gemini command export readiness with `python scripts/validate-skills.py`.
