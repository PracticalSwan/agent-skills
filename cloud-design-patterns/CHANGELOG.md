# Changelog

## [2026-04-04] - Initial Import and Catalog Upgrade

### Added

- Imported `cloud-design-patterns` from the `awesome-copilot` reference catalog into the canonical maintained workspace
- Rewrote the skill into the repo house style with a clearer concern-to-pattern mapping and selection workflow
- Added `scripts/pattern-shortlist.py` to quickly turn workload concerns into reference-backed pattern shortlists

### Tested

- Ran `python cloud-design-patterns/scripts/pattern-shortlist.py --concern reliability --concern migration --concern security`
- Planned validation through `python scripts/validate-skills.py`
