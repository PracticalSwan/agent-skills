# Changelog

## [2026-04-24] - Skill Refresh

### Changed
- Standardized the SKILL frontmatter with version metadata, last-updated date, tags, and a concise catalog description.
- Reformatted the portability and MCP guidance with a preferred server line, a copy-paste fallback prompt, and consistent bullet lists.
- Added a catalog-standard Anti-Patterns section and refreshed the Related Skills links at the end of the skill.
## [2026-04-04] - Initial Import and Catalog Upgrade

### Added

- Imported `context-map` from the `awesome-copilot` reference catalog into the canonical maintained workspace
- Added a stronger scoping workflow, risk heuristics, and a reusable Markdown output format
- Added `references/context-map-template.md` and `scripts/build-context-map.py` to make the skill actionable across clients

### Tested

- Ran `python context-map/scripts/build-context-map.py --root . --query sync-skills --query codex --limit 5`
- Planned validation through `python scripts/validate-skills.py`
