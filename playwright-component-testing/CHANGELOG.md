# Changelog

All notable changes to the `playwright-component-testing` skill are documented here.

## [2026-09-12] - Playwright Stable Source Refresh

### Added

- Imported the stable component-testing story-gallery workflow from
  `microsoft/playwright@v1.63.0` and kept its gallery references together.

### Changed

- Documented the required project-local `@playwright/test` dependency and
  approval-gated browser setup; the retired experimental component-testing
  runtime is not required.
- Kept the retained-client portability, MCP fallback, Anti-Patterns,
  Verification Protocol, and Related Skills sections aligned.

### Fixed

- Corrected the prerequisite wording so the built-in `mount` fixture is not
  presented as package-free.
