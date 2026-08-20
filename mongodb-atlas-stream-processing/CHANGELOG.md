# Changelog

All notable changes to the `mongodb-atlas-stream-processing` skill are documented here.

## [2026-08-20] - Vendor Skill Import

### Added

- Imported the canonical `skills/mongodb-atlas-stream-processing` workflow from `https://github.com/mongodb/agent-skills` at commit `b4ea8150a020b9babaddc6c271c6dc177c06a83f`.
- Normalized catalog metadata, retained-client portability, MCP fallback, safety, verification, and related-skill routing.

### Changed

- Preserved the upstream workflow and support files while adding this catalog's cross-client wrapper.

### Fixed

- Added explicit fallback and approval boundaries so the skill does not assume unavailable host tools or credentials.
