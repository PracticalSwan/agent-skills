# Changelog

All notable changes to this skill will be documented in this file.

## [2026-03-09] - Workspace Modernization

### Changed
- Rewrote the skill to describe Excel MCP as host-specific rather than assuming universal wrapper commands
- Repositioned `scripts/csv-to-xlsx.py` as the local fallback when spreadsheet MCP tools are unavailable

## [2026-02-28] - Description Rewrite and Cross-References

### Changed
- Rewrote the skill description to concise activation-focused wording
- Improved keyword specificity to reduce overlap with related skills

### Added
- Added the related-skills cross-reference table

## [2026-02-19] - Excel MCP Extraction

### Changed
- Split Excel workflow guidance out of the former shared office-documents skill into an Excel-specific skill
- Replaced library-first guidance with MCP-oriented spreadsheet workflows
- Updated activation triggers around workbook, worksheet, spreadsheet, and Excel MCP use cases

### Added
- Added Excel-specific references and local CSV-to-XLSX fallback automation
- Added workbook, worksheet, cell, chart, and pivot-table workflow coverage

### Fixed
- Reduced ambiguity between generic document handling and Excel-specific spreadsheet tasks
