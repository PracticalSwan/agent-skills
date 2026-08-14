# Changelog

All notable changes to the `stitch-react-vite-dashboard` skill will be documented in this file.

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

## [2026-07-29] - Upstream Refresh and MCP Correction

### Added

- Refreshed support material from `https://github.com/google-labs-code/stitch-skills` at `plugins/stitch-build/skills/react-vite-dashboard` and commit `7b53207b94e62911777d53d4238b5f8c88c2b519`.

### Changed

- Normalized the refreshed workflow into the local `version: "2.0"` schema with folder-safe naming.
- Preserved the verified design-system MCP boundary while incorporating compatible upstream workflow and helper-script improvements.

### Fixed

- Avoided importing upstream assumptions that unverified Stitch screen lookup, generation, or editing tools are always available.
