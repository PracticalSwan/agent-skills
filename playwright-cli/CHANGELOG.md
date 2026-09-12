# Changelog

All notable changes to the `playwright-cli` skill are documented here.

## [2026-09-12] - Playwright CLI Package Refresh

### Added

- Imported the `playwright-cli` workflow from the `@playwright/cli@0.1.19`
  package and installed its global agent skill for the approved `.agents` and
  `.claude` homes.

### Changed

- Documented the current package-first install path, `requests` network
  inspection, `network-state-set`, structured output, and the explicit
  boundary between the CLI and the project `playwright` test runner.
- Kept the retained-client portability, MCP fallback, Anti-Patterns,
  Verification Protocol, and Related Skills sections aligned.

### Fixed

- Removed stale guidance that treated `npx playwright` as an equivalent
  fallback for the global `@playwright/cli` package.
- Standardized project test/debug examples on `npx --no-install` so missing
  local dependencies fail closed instead of triggering an implicit fetch.
- The catalog wrapper now gives a clear Node.js prerequisite error on WSL or
  other shells that can see a Windows shim but cannot execute its runtime.
