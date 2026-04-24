# Changelog

## [2026-04-24] - Version 1.1 Refresh

### Changed
- Updated the SKILL frontmatter version to `1.1` for the 2026-04-24 catalog refresh.

## [2026-04-24] - Skill Refresh

### Changed
- Standardized the SKILL frontmatter with version metadata, last-updated date, tags, and a concise catalog description.
- Reformatted the portability and MCP guidance with a preferred server line, a copy-paste fallback prompt, and consistent bullet lists.
- Added a catalog-standard Anti-Patterns section and refreshed the Related Skills links at the end of the skill.
## [2026-04-04] - Initial Import and Catalog Upgrade

### Added

- Imported `cloud-design-patterns` from the `awesome-copilot` reference catalog into the canonical maintained workspace
- Rewrote the skill into the repo house style with a clearer concern-to-pattern mapping and selection workflow
- Added `scripts/pattern-shortlist.py` to quickly turn workload concerns into reference-backed pattern shortlists

### Tested

- Ran `python cloud-design-patterns/scripts/pattern-shortlist.py --concern reliability --concern migration --concern security`
- Planned validation through `python scripts/validate-skills.py`
