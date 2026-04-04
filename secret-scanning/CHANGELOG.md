# Changelog

## [2026-04-04] - Initial Import and Catalog Upgrade

### Added

- Imported `secret-scanning` from the `awesome-copilot` reference catalog into the canonical maintained workspace
- Rewrote the top-level skill into the repo house style while preserving the detailed upstream reference notes
- Added `scripts/precommit-secret-audit.py` as a client-neutral local fallback for pre-commit secret checks

### Tested

- Ran `python secret-scanning/scripts/precommit-secret-audit.py --path secret-scanning/scripts`
- Planned validation through `python scripts/validate-skills.py`
