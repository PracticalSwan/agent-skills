# Changelog

All notable changes to the `stitch-shadcn-ui` skill will be documented in this file.

## [2026-08-14] - Catalog Freshness And Source Sync

### Added

- Refreshed the catalog metadata and retained-client portability baseline.

### Changed

- Updated the catalog metadata and last-updated state for the 2026-08-14 maintenance pass.
- Kept the retained-client portability, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.

### Fixed

- Preserved explicit no-MCP fallbacks and the catalog's safety, approval, and source-boundary guidance.

## [2026-08-02] - Frontend Design Reference Consolidation

### Changed

- Removed the retired `premium-frontend-ui` cross-reference and retained
  `frontend-design` as the canonical general art-direction companion.

## [2026-07-29] - Version 2.0 Client Support Reset

### Added

- Added the current GitHub Copilot, Claude Code, and Codex portability baseline.

### Changed

- **BREAKING:** Removed Gemini CLI and Antigravity as supported clients.
- Refreshed catalog metadata and last-updated state for the 2026-07-29 maintenance pass.
- Kept the retained-client portability, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.

### Fixed

- Prevented catalog modernization from reintroducing removed Gemini or Antigravity guidance.

## [2026-07-29] - Upstream Refresh and MCP Correction

### Added

- Refreshed support material from `https://github.com/google-labs-code/stitch-skills` at `plugins/stitch-build/skills/shadcn-ui` and commit `7b53207b94e62911777d53d4238b5f8c88c2b519`.

### Changed

- Normalized the refreshed workflow into the local `version: "2.0"` schema with folder-safe naming.
- Preserved the verified design-system MCP boundary while incorporating compatible upstream workflow and helper-script improvements.

### Fixed

- Avoided importing upstream assumptions that unverified Stitch screen lookup, generation, or editing tools are always available.

## [2026-07-11] - Catalog Maintenance Refresh

### Added

- Added the current catalog verification baseline where it was missing.

### Changed

- Refreshed catalog metadata and last-updated state for the 2026-07-11 maintenance pass.
- Kept the cross-client, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.
- Reclassified historical `Tested` or `Verified` changelog headings under the allowed changelog vocabulary without dropping their evidence.

### Fixed

- Closed validator and documentation drift so the enforced schema matches the documented skill baseline.

## [2026-07-11] - Upstream Refresh and MCP Correction

### Added

- Refreshed support material from `https://github.com/google-labs-code/stitch-skills` at `plugins/stitch-build/skills/shadcn-ui` and commit `3f64079d75d025bc5890c73669f27c26a2d80b31`.

### Changed

- Normalized the refreshed workflow into the local `version: "1.3"` schema with folder-safe naming.
- Preserved the verified design-system MCP boundary while incorporating compatible upstream workflow and helper-script improvements.

### Fixed

- Avoided importing upstream assumptions that unverified Stitch screen lookup, generation, or editing tools are always available.

## [2026-06-15] - Initial Stitch Import and MCP Correction

### Added

- Imported support material from `https://github.com/google-labs-code/stitch-skills` at `plugins/stitch-build/skills/shadcn-ui`.
- Added catalog-standard portability, MCP fallback, anti-pattern, verification, and related-skill sections.

### Changed

- Normalized the upstream skill into the local `version: "1.2"` schema with folder-safe naming.
- Routed overlapping behavior through narrower Stitch skills instead of duplicating the old monolithic `stitch-design` guidance.

### Fixed

- Corrected upstream instructions that assumed unverified Stitch MCP screen lookup, generation, or editing tools were always available.
