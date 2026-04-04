# Changelog

## [2026-04-04] - Initial Import and Catalog Upgrade

### Added

- Imported `context-map` from the `awesome-copilot` reference catalog into the canonical maintained workspace
- Added a stronger scoping workflow, risk heuristics, and a reusable Markdown output format
- Added `references/context-map-template.md` and `scripts/build-context-map.py` to make the skill actionable across clients

### Tested

- Ran `python context-map/scripts/build-context-map.py --root . --query sync-skills --query codex --limit 5`
- Planned validation through `python scripts/validate-skills.py`
