# Changelog

All notable changes to the Copilot Skills repository will be documented in this file.

## [2026-03-09] - Workspace Skill Modernization

### Changed
- Modernized editable skill folders to align with the maintained structure of `SKILL.md`, `scripts/`, and `references/`
- Removed duplicated `## Related Skills` sections across the editable skill set
- Rewrote outdated MCP-heavy skills to reflect current 2026 behavior, especially for Notion, Microsoft Learn, NotebookLM, Power BI, and Office-document workflows
- Updated `README.md` to reflect the real workspace layout, current counts, loading order, and MCP guidance

### Added
- New runnable helper scripts for skills that previously had references only:
  - `breaking-changes-management/scripts/migration-guide-scaffold.py`
  - `code-examples-sync/scripts/example-sync-check.py`
  - `documentation-automation/scripts/docs-pipeline-scaffold.py`
  - `documentation-patterns/scripts/doc-template-picker.py`
  - `documentation-quality/scripts/doc-style-audit.py`
  - `documentation-verification/scripts/doc-link-check.py`
  - `web-design-reviewer/scripts/css-risk-audit.py`
- New current-reference notes:
  - `microsoft-development/references/microsoft-learn-mcp.md`
  - `notion-docs/references/notion-mcp-quickstart.md`
  - `notebooklm-management/scripts/README.md`
- Backfilled `CHANGELOG.md` into every editable skill folder and added a dated `2026-03-09` entry for each skill
- Normalized per-skill changelog headings so only `Added`, `Changed`, `Fixed`, and `Tested` are used

### Fixed
- Replaced broken PowerShell automation in:
  - `azure-integrations/scripts/deploy-appservice.ps1`
  - `microsoft-development/scripts/azure-health-check.ps1`
- Removed stale references to old global skill paths and legacy repo structure assumptions

## [2026-03-01] - Activation Testing and Fixes

### Fixed
- `javascript-development`: Added `TypeScript` to the description so TypeScript prompts without React context activate the right skill
- `frontend-design`: Added generic `CSS`, `wireframes`, and `writing CSS` keywords
- `web-testing`: Added `unit tests` to the description
- `web-design-reviewer`: Added clearer disambiguation against automated E2E testing

### Tested
- Ran 90+ activation test scenarios across 12 groups covering all 37 non-superpower skills at the time
- Tested keyword matching against diverse prompt patterns
- Confirmed a small set of acceptable context-dependent overlaps

## [2026-02-28] - Description Rewrite and Cross-References

### Changed
- Rewrote all 37 non-superpower skill descriptions to concise activation-focused language
- Reduced overlap between related skills, especially JS vs React, DevOps vs Workflow, and the documentation skill cluster

### Added
- Added `## Related Skills` cross-reference tables across the editable skill set
