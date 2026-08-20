# Changelog

All notable changes to the `deploy-to-vercel` skill are documented here.

## [2026-08-20] - Vendor Skill Import

### Added

- Imported the canonical `skills/deploy-to-vercel` workflow from `https://github.com/vercel-labs/agent-skills` at commit `b8caa260a420a73042e35521de4b5c8baf6446cc`.
- Normalized catalog metadata, retained-client portability, MCP fallback, safety, verification, and related-skill routing.

### Changed

- Preserved the upstream workflow and support files while adding this catalog's cross-client wrapper.

### Fixed

- Added explicit fallback and approval boundaries so the skill does not assume unavailable host tools or credentials.
