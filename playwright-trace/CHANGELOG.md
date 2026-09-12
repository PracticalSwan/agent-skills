# Changelog

All notable changes to the `playwright-trace` skill are documented here.

## [2026-09-12] - Playwright Stable Source Refresh

### Added

- Imported the focused trace-inspection workflow from the stable
  `microsoft/playwright@v1.63.0` source.

### Changed

- Documented that trace-file commands require a project-local `playwright`
  executable, while live tracing remains available through `playwright-cli`.
- Kept the retained-client portability, MCP fallback, Anti-Patterns,
  Verification Protocol, and Related Skills sections aligned.

### Fixed

- Removed the implication that the global `@playwright/cli` package also
  provides the `playwright trace` test-runner binary.
- Standardized trace examples on `npx --no-install` so the workflow does not
  trigger an implicit package fetch when a project dependency is missing.
