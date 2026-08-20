# Changelog

All notable changes to the `figma-create-new-file` skill are documented here.

## [2026-08-20] - Vendor Skill Import

### Added

- Imported the canonical `skills/figma-create-new-file` workflow from `https://github.com/figma/mcp-server-guide` at commit `7f6562c4900fafb46e5e8fd3cc8ced954779bab3`.
- Normalized catalog metadata, retained-client portability, MCP fallback, safety, verification, and related-skill routing.

### Changed

- Preserved the upstream workflow and support files while adding this catalog's cross-client wrapper.

### Fixed

- Added explicit fallback and approval boundaries so the skill does not assume unavailable host tools or credentials.
