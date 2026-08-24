# Changelog

All notable changes to the `gemini-interactions-api` skill are documented here.

## [2026-08-24] - Catalog Freshness And Source Sync

### Added

- Refreshed the catalog metadata and retained-client portability baseline.

### Changed

- Updated the catalog metadata and last-updated state for the 2026-08-24 maintenance pass.
- Kept the retained-client portability, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.

### Fixed

- Preserved explicit no-MCP fallbacks and the catalog's safety, approval, and source-boundary guidance.

## [2026-08-16] - Catalog Freshness And Source Sync

### Added

- Promoted this skill from a verified `.codex` or `.claude` child path into the parent catalog.
- Refreshed the catalog metadata and retained-client portability baseline.

### Changed

- Updated the catalog metadata and last-updated state for the 2026-08-16 maintenance pass.
- Kept the retained-client portability, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.
- Added an explicit route to `gemini-api-dev`; the Interactions workflow remains
  separate because it owns its own managed-agent, state, streaming, and
  migration boundary.

### Fixed

- Preserved explicit no-MCP fallbacks and the catalog's safety, approval, and source-boundary guidance.
