# Changelog

All notable changes to the `jupyter-notebook` skill will be documented in this file.

## [2026-07-11] - Catalog Maintenance Refresh

### Added

- Added the current catalog verification baseline where it was missing.

### Changed

- Refreshed catalog metadata and last-updated state for the 2026-07-11 maintenance pass.
- Kept the cross-client, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.
- Reclassified historical `Tested` or `Verified` changelog headings under the allowed changelog vocabulary without dropping their evidence.

### Fixed

- Closed validator and documentation drift so the enforced schema matches the documented skill baseline.

## [2026-06-09] - Catalog Normalization and Validation Baseline

### Added
- Added the repo-standard `Anti-Patterns`, `Verification Protocol`, portability, MCP fallback, and related-skills sections.
- Added a per-skill changelog so future updates can be tracked in the maintained catalog.

### Changed
- Updated the frontmatter to the shared `version: "1.2"` / `last_updated: 2026-06-09` schema used by this repository.
- Kept the existing core workflow intact while aligning this import with the shared validation and export requirements.

### Fixed
- Removed this skill from the repo's known schema-exception set so catalog validation can reason over it normally.
