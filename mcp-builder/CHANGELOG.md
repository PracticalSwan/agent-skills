# Changelog

## [2026-04-04] - Initial Import and Catalog Upgrade

### Added

- Imported `mcp-builder` from the `awesome-claude-skills` discovery catalog using the official Anthropic skill as the canonical source
- Rewrote the top-level skill into the repo house style while preserving the upstream reference library and helper scripts
- Added a maintained `CHANGELOG.md` so the skill is tracked like the rest of the editable catalog

### Tested

- Ran `python -m py_compile mcp-builder/scripts/connections.py mcp-builder/scripts/evaluation.py`
- Planned validation through `python scripts/validate-skills.py`
