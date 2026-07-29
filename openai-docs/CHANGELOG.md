# Changelog

All notable changes to the `openai-docs` skill are documented here.

## [2026-07-29] - Version 2.0 Client Support Reset

### Added

- Promoted this skill from a verified `.codex` or `.claude` child path into the parent catalog.
- Added the current GitHub Copilot, Claude Code, and Codex portability baseline.

### Changed

- **BREAKING:** Removed Gemini CLI and Antigravity as supported clients.
- Added host-aware Docs MCP and official-domain fallbacks for Claude Code,
  including sessions using the GLM Coding Plan endpoint.
- Refreshed catalog metadata and last-updated state for the 2026-07-29 maintenance pass.
- Kept the retained-client portability, MCP fallback, Anti-Patterns, Verification Protocol, and Related Skills sections aligned.

### Fixed

- Prevented catalog modernization from reintroducing removed Gemini or Antigravity guidance.
