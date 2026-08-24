# Changelog

All notable changes to the `netlify-blobs` skill are documented here.

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

- Imported the canonical `skills/netlify-blobs` workflow from `https://github.com/netlify/context-and-tools` at commit `5a62a5694417640a2bba11a0701c8995ecc40bcc`.
- Normalized catalog metadata, retained-client portability, MCP fallback, safety, verification, and related-skill routing.

### Changed

- Preserved the upstream workflow and support files while adding this catalog's cross-client wrapper.

### Fixed

- Added explicit fallback and approval boundaries so the skill does not assume unavailable host tools or credentials.
