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

## [2026-04-24] - Skill Refresh

### Changed
- Standardized the SKILL frontmatter with version metadata, last-updated date, tags, and a concise catalog description.
- Reformatted the portability and MCP guidance with a preferred server line, a copy-paste fallback prompt, and consistent bullet lists.
- Added a catalog-standard Anti-Patterns section and refreshed the Related Skills links at the end of the skill.
## [2026-04-24] - Catalog Audit Cleanup

### Fixed
- Repaired imported mojibake or replacement-character separators so command tables and prose render cleanly.

All notable changes to the `avoid-ai-writing` skill will be documented in this file.

## [2026-04-24] - Initial Import and Portability Upgrade

### Added
- Imported the skill from `https://github.com/conorbronsdon/avoid-ai-writing` at `cbf885e087e8ec1168bc58dc603606a6e4bfacbd`.
- Added the upstream MIT license as `LICENSE.txt`.
- Added cross-client portability guidance for GitHub Copilot, Claude Code, Codex, and Gemini CLI.
- Added the repo-standard no-MCP fallback guidance for this skill.

### Changed
- Kept the upstream `SKILL.md` guidance intact while appending catalog-required generated sections.

### Tested
- Validated `SKILL.md` frontmatter and Gemini command export readiness with `python scripts/validate-skills.py`.
