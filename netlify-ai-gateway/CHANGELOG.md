# Changelog

All notable changes to the `netlify-ai-gateway` skill are documented here.

## [2026-08-20] - Vendor Skill Import

### Added

- Imported the canonical `skills/netlify-ai-gateway` workflow from `https://github.com/netlify/context-and-tools` at commit `5a62a5694417640a2bba11a0701c8995ecc40bcc`.
- Normalized catalog metadata, retained-client portability, MCP fallback, safety, verification, and related-skill routing.

### Changed

- Preserved the upstream workflow and support files while adding this catalog's cross-client wrapper.

### Fixed

- Added explicit fallback and approval boundaries so the skill does not assume unavailable host tools or credentials.
