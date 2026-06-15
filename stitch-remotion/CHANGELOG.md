# Changelog

All notable changes to the `stitch-remotion` skill will be documented in this file.

## [2026-06-15] - Initial Stitch Import and MCP Correction

### Added

- Imported support material from `https://github.com/google-labs-code/stitch-skills` at `plugins/stitch-build/skills/remotion`.
- Added catalog-standard portability, MCP fallback, anti-pattern, verification, and related-skill sections.

### Changed

- Normalized the upstream skill into the local `version: "1.2"` schema with folder-safe naming.
- Routed overlapping behavior through narrower Stitch skills instead of duplicating the old monolithic `stitch-design` guidance.

### Fixed

- Corrected upstream instructions that assumed unverified Stitch MCP screen lookup, generation, or editing tools were always available.
