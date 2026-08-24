# Changelog

All notable changes to the `deepstream-dev` skill will be documented in this file.

## [2026-08-24] - Catalog Freshness And Source Sync

### Added

- Refreshed the catalog metadata and retained-client portability baseline.

### Changed

- Updated the catalog metadata and last-updated state for the 2026-08-24 maintenance pass.
- Kept the retained-client portability, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.

### Fixed

- Preserved explicit no-MCP fallbacks and the catalog's safety, approval, and source-boundary guidance.

## [2026-08-14] - Catalog Freshness And Source Sync

### Added

- Refreshed the catalog metadata and retained-client portability baseline.

### Changed

- Updated the catalog metadata and last-updated state for the 2026-08-14 maintenance pass.
- Kept the retained-client portability, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.

### Fixed

- Preserved explicit no-MCP fallbacks and the catalog's safety, approval, and source-boundary guidance.

## [2026-07-29] - Version 2.0 Client Support Reset

### Added

- Added the current GitHub Copilot, Claude Code, and Codex portability baseline.

### Changed

- **BREAKING:** Removed Gemini CLI and Antigravity as supported clients.
- Refreshed catalog metadata and last-updated state for the 2026-07-29 maintenance pass.
- Kept the retained-client portability, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.

### Fixed

- Prevented catalog modernization from reintroducing removed Gemini or Antigravity guidance.

## [2026-07-11] - Catalog Maintenance Refresh

### Added

- Added the current catalog verification baseline where it was missing.

### Changed

- Refreshed catalog metadata and last-updated state for the 2026-07-11 maintenance pass.
- Kept the cross-client, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.
- Reclassified historical `Tested` or `Verified` changelog headings under the allowed changelog vocabulary without dropping their evidence.

### Fixed

- Closed validator and documentation drift so the enforced schema matches the documented skill baseline.

## [2026-06-09] - Initial Import and Catalog Normalization

### Added

- Imported `deepstream-dev` from `https://github.com/NVIDIA/skills` at `skills/deepstream-dev` pinned to `129a1087a1853f32a950e2f7bbc0fd7d57b9d422`.
- Added repo-standard `Anti-Patterns`, `Verification Protocol`, portability, MCP fallback, and related-skills sections.
- Preserved the upstream benchmark, signature, skill card, and bundled references or scripts for provenance and later refreshes.

### Changed

- Normalized `SKILL.md` frontmatter to the shared catalog schema with `version: "1.2"` and `last_updated: 2026-06-09`.
- Moved upstream-only top-level metadata into the nested `metadata` block so validation, export, and downstream sync stay consistent.

### Fixed

- Aligned the imported skill with this repository's maintained-skill requirements and downstream sync workflow.
