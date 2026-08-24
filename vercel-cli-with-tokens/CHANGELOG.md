# Changelog

All notable changes to the `vercel-cli-with-tokens` skill are documented here.

## [2026-08-24] - Catalog Freshness And Source Sync

### Added

- Refreshed the catalog metadata and retained-client portability baseline.

### Changed

- Updated the catalog metadata and last-updated state for the 2026-08-24 maintenance pass.
- Kept the retained-client portability, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.

### Fixed

- Preserved explicit no-MCP fallbacks and the catalog's safety, approval, and source-boundary guidance.

## [2026-08-20] - Vendor Skill Import

### Added

- Imported the canonical `skills/vercel-cli-with-tokens` workflow from `https://github.com/vercel-labs/agent-skills` at commit `b8caa260a420a73042e35521de4b5c8baf6446cc`.
- Normalized catalog metadata, retained-client portability, MCP fallback, safety, verification, and related-skill routing.

### Changed

- Preserved the upstream workflow and support files while adding this catalog's cross-client wrapper.

### Fixed

- Added explicit fallback and approval boundaries so the skill does not assume unavailable host tools or credentials.
- Removed instructions that printed or requested Vercel token values; authentication now stops at an approved secret-manager or local-login handoff.
