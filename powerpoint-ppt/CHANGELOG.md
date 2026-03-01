# PowerPoint Presentation Skill - MCP Enhancement (2026-02-19)

## Summary

The `powerpoint-ppt` skill has been extracted from the original `office-documents` skill to focus specifically on Microsoft PowerPoint (.pptx) presentation manipulation using MCP server tools.

## Key Changes

### 1. Technology Migration

**From (Old - Removed):**
- `pptxgenjs` JavaScript library for PowerPoint
- Manual XML unpack/pack operations for .pptx files
- LibreOffice integration for file conversions

**To (New - Added):**
- **PowerPoint MCP Tools**: Presentation creation and management
- Direct MCP server integration for PowerPoint format

### 2. New MCP Tool Categories

#### PowerPoint Presentations (4+ tool groups)
- Presentation creation and management
- Content management (images, fonts, text with `mcp_ppt_manage_text`)
- Template application (`mcp_ppt_apply_template`)
- Information extraction and management

### 3. Activation Triggers Updated

```python
if any(kw in ['pptx', 'powerpoint', 'presentation', 'ppt', 'slide', 'deck', 'mcp_ppt', 'powerpoint mcp']):
    activate('powerpoint-ppt')
```

## Benefits

### Simplified Workflow
- Single activation point for PowerPoint presentations
- No need to manage multiple JavaScript libraries
- Direct tool calls instead of library wrapping

### Better Error Handling
- MCP servers handle errors gracefully
- Clear error messages from MCP tools
- Easier debugging and troubleshooting

### Future-Proof
- MCP servers update independently
- New tools added without skill updates
- Community contributions to MCP ecosystem

---

## [2026-02-28] — Description Rewrite & Cross-References

### Changed
- Rewrote skill description to ~200 characters with clear, specific activation keywords
- Improved keyword specificity to reduce overlap with related skills

### Added
- `## Related Skills` cross-reference table with 2-4 related skills and "Use When" guidance

## Migration Notes

For existing code using old libraries:
1. Identify the operation (create, edit, convert)
2. Find the equivalent MCP tool from quick reference
3. Follow MCP tool parameter structure
4. Test with sample files before full migration

## Files Changed

- `SKILL.md` - Extracted from office-documents (PowerPoint-specific content)
- `references/README.md` - PowerPoint references
- `scripts/README.md` - PowerPoint scripts

## Related Skills

- `word-document` - Word document manipulation
- `excel-sheet` - Excel spreadsheet manipulation

---

**Updated**: 2026-02-19
**Compatibility**: Requires MCP server installed and configured:
- Presentation MCP server for PowerPoint operations
