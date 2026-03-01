# Changelog

All notable changes to the Copilot Skills repository will be documented in this file.

## [2026-03-01] — Activation Testing & Fixes

### Fixed
- **javascript-development**: Added "TypeScript" keyword to description — prompts about TypeScript without React context now correctly activate this skill instead of react-development
- **frontend-design**: Added generic "CSS", "wireframes", and "writing CSS" keywords — was previously limited to "Tailwind CSS" only
- **web-testing**: Added "unit tests" to description — was previously limited to E2E/Playwright testing only
- **web-design-reviewer**: Added "Not for automated E2E testing" disambiguation and clarified visual inspection language to prevent overlap with web-testing on screenshot prompts

### Tested
- Ran 90+ activation test scenarios across 12 groups covering all 37 non-superpower skills
- Verified keyword matching against diverse prompt patterns (agent delegation, Azure, documentation, frontend, JS/React/Vite, backend, database, office documents, DevOps, miscellaneous, testing, cross-skill overlap)
- Confirmed acceptable context-dependent overlaps (API docs, database schemas, backend API prompts)

### Updated
- **CLAUDE.md**: Updated skill catalog entries to reflect description changes (frontend-design, web-testing, javascript-development, web-design-reviewer)
- **Serena memories**: Created `active-context` and `progress` memories documenting current state

## [2026-02-28] — Description Rewrite & Cross-References

### Changed
- Rewrote all 37 non-superpower skill descriptions to ~200 characters (excluding spaces) with clear, consistent activation keywords
- Fixed overlaps between related skills:
  - javascript-development vs react-development (JS general vs React-specific)
  - devops-tooling vs development-workflow (tools/CI vs lifecycle/specs)
  - 5 documentation skills (authoring, automation, patterns, quality, verification) — each given distinct trigger scope

### Added
- `## Related Skills` cross-reference tables appended to all 37 non-superpower skills
- Each table lists 2-4 related skills with "Use When" guidance for disambiguation
