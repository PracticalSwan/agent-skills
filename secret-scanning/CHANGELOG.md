# Changelog

## [2026-04-24] - Version 1.1 Refresh

### Changed
- Updated the SKILL frontmatter version to `1.1` for the 2026-04-24 catalog refresh.

## [2026-04-24] - Skill Refresh

### Changed
- Standardized the SKILL frontmatter with version metadata, last-updated date, tags, and a concise catalog description.
- Reformatted the portability and MCP guidance with a preferred server line, a copy-paste fallback prompt, and consistent bullet lists.
- Added a catalog-standard Anti-Patterns section and refreshed the Related Skills links at the end of the skill.
- Added a Tech Stack Target / Version note so the workflow clearly targets the current GitHub Advanced Security and local audit tooling.
## [2026-04-04] - Initial Import and Catalog Upgrade

### Added

- Imported `secret-scanning` from the `awesome-copilot` reference catalog into the canonical maintained workspace
- Rewrote the top-level skill into the repo house style while preserving the detailed upstream reference notes
- Added `scripts/precommit-secret-audit.py` as a client-neutral local fallback for pre-commit secret checks

### Tested

- Ran `python secret-scanning/scripts/precommit-secret-audit.py --path secret-scanning/scripts`
- Planned validation through `python scripts/validate-skills.py`
