---
name: word-document
description: Microsoft Word (.docx) document manipulation using MCP server tools. Use this any time a Word document is involved - as input, output, or both. Activate the word-document-server MCP for Word operations. Covers reading, editing, creating, formatting, analyzing, and converting Word documents with professional standards including tables, footnotes, comments, images, and PDF conversion.
license: Complete terms in LICENSE.txt
---



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`


Comprehensive skill for working with Microsoft Word documents using MCP servers.

## When to Use This Skill

- Any task where .docx is an input, output, or transformation target
- Creating, editing, formatting, or analyzing Word files
- Converting data/content into polished Word deliverables
- Applying document structure, table formatting, footnotes, or comments
- Automating Word document workflows via MCP tools

### Typical Activation Triggers

- .docx work: reports, contracts, memos, template generation, search/replace, comments, formatting
- Document structure: headings, paragraphs, lists, tables, images
- Advanced features: footnotes, endnotes, track changes, comments
- Export: PDF conversion, document protection

---

## Part 1: Word Documents (.docx) via MCP

## Quick Reference

| Task | Activation / Tool |
|------|-------------------|
| Create document, custom style | `activate_document_creation_and_styling` |
| Add heading, paragraph, list | `activate_document_structure_tools` |
| Insert image, page break | `activate_basic_document_editing_tools` |
| **Delete paragraph** | `activate_basic_document_editing_tools` |
| **Format existing text** | `activate_basic_document_editing_tools` |
| Add footnote / endnote (basic) | `activate_basic_document_editing_tools` |
| Add / format / merge table cells | `activate_table_management_tools` |
| Alternating row colors | **`mcp_word-document_apply_table_alternating_rows`** ← direct |
| Adv. footnotes (style, validate) | `activate_advanced_footnote_management` |
| Find text, metadata, structure | `activate_document_analysis_tools` |
| Add / get / delete comments | `activate_comment_management_tools_2` |
| Insert content near existing text | `activate_contextual_insertion_tools` |
| Convert to PDF, password protect | `activate_document_security_and_conversion` |
| Search & replace, copy document | `mcp_word-document_search_and_replace` / `_copy_document` ← direct |

> **Note:** Page headers/footers, Table of Contents, and margin settings are not exposed by the Word MCP server — these require opening the `.docx` in Microsoft Word or using `python-docx` directly.

### Tool Activation Order

Activate only what you need. For a full-featured document:

```javascript
activate_document_creation_and_styling();    // create_document, create_custom_style
activate_document_structure_tools();         // add_heading, add_paragraph (lists, styles)
activate_basic_document_editing_tools();     // insert_image, insert_page_break, delete_paragraph, format_text, add_footnote
activate_table_management_tools();           // add_table, borders, shading, merge, padding
activate_advanced_footnote_management();     // style/validate/delete footnotes
activate_document_analysis_tools();          // find_text, get_metadata, get_structure, extract_text
activate_comment_management_tools_2();       // add/get/delete comments
activate_contextual_insertion_tools();       // insert near existing text
activate_document_security_and_conversion(); // convert_to_pdf, protect/unprotect
```

---

### Create Document and Custom Styles

```javascript
mcp_word-document_create_document({
  filename: "report.docx",
  title: "Q3 Performance Report",
  author: "Jane Smith"
})

// Define brand style once; reuse by style_name in headings/paragraphs
mcp_word-document_create_custom_style({
  filename: "report.docx",
  style_name: "BrandHeading",
  bold: true,
  font_size: 18,
  font_name: "Arial",
  color: "1B3A5C",
  base_style: "Heading 1"
})
```

---

### Headings, Paragraphs, and Lists

```javascript
// Heading (level 1–6)
mcp_word-document_add_heading({
  filename: "report.docx",
  text: "Executive Summary",
  level: 1,
  font_name: "Arial",
  font_size: 16,
  bold: true
})

// Plain paragraph
mcp_word-document_add_paragraph({
  filename: "report.docx",
  text: "Performance exceeded expectations across all key metrics.",
  font_name: "Arial",
  font_size: 11,
  alignment: "left"
})

// Numbered list  —  style: "List Number" | "List Number 2" | "List Number 3"
mcp_word-document_add_paragraph({ filename: "report.docx", text: "Review financial summary", style: "List Number" })

// Bulleted list  —  style: "List Bullet" | "List Bullet 2" | "List Bullet 3"
mcp_word-document_add_paragraph({ filename: "report.docx", text: "Revenue up 12%", style: "List Bullet" })
mcp_word-document_add_paragraph({ filename: "report.docx", text: "Driver: APAC region growth", style: "List Bullet 2" })  // nested

// Inline mixed formatting (bold, italic, color in one paragraph via runs)
mcp_word-document_add_paragraph({
  filename: "report.docx",
  runs: [
    { text: "Warning: ", bold: true, color: "CC0000" },
    { text: "Do not exceed " },
    { text: "100 units", bold: true, italic: true },
    { text: " per cycle." }
  ]
})
```

---

### Images, Page Breaks, Delete Paragraph, Format Text

> Activate: `activate_basic_document_editing_tools()`

```javascript
// Insert image
mcp_word-document_insert_image({
  filename: "report.docx",
  image_path: "./chart_q3.png",
  width: 6.0,       // inches
  height: 3.5,
  alignment: "center"
})

// Page break (separate major sections)
mcp_word-document_insert_page_break({ filename: "report.docx" })

// Delete a paragraph by 0-based index
mcp_word-document_delete_paragraph({ filename: "report.docx", paragraph_index: 7 })

// Re-format text in an existing paragraph
mcp_word-document_format_text({
  filename: "report.docx",
  paragraph_index: 3,
  bold: true,
  font_size: 12,
  color: "2E74B5"
})

// Search and replace template placeholders
mcp_word-document_search_and_replace({ filename: "report.docx", find_text: "[CLIENT]", replace_text: "Acme Corp" })

// Duplicate template to new file
mcp_word-document_copy_document({ source_filename: "template.docx", destination_filename: "report_q3.docx" })
```

### Lists and Inline Formatting

> The list examples above (numbered/bulleted/nested/runs) are in the **Headings, Paragraphs, and Lists** section above. No separate activation is needed beyond `activate_document_structure_tools`.

---

### Advanced Table Formatting

#### Activate Table Management Tools

```javascript
activate_table_management_tools(); // borders, shading, merging, cell padding
```

#### Table Borders and Shading

```javascript
// Apply borders to entire table
mcp_word-document_format_table({
  filename: "report.docx",
  table_index: 0,
  border_style: "single",
  border_size: 4,
  border_color: "2E74B5",
  header_bg_color: "2E74B5",
  header_font_color: "FFFFFF",
  header_bold: true
})

// Shade a specific cell
mcp_word-document_shade_cell({
  filename: "report.docx",
  table_index: 0,
  row: 0,
  col: 0,
  bg_color: "D6E4F0"
})
```

#### Alternating Row Colors (Zebra Stripe)

```javascript
// Apply alternating row colors for readability
mcp_word-document_apply_table_alternating_rows({
  filename: "report.docx",
  table_index: 0,
  color1: "FFFFFF",   // white rows
  color2: "EBF3FB"    // light blue rows
})
```

#### Merge Table Cells

```javascript
// Merge cells horizontally (e.g., for a header spanning all columns)
mcp_word-document_merge_cells_horizontal({
  filename: "report.docx",
  table_index: 0,
  row: 0,
  start_col: 0,
  end_col: 3   // merges columns 0–3 in row 0
})

// Merge cells vertically (e.g., row label spanning multiple rows)
mcp_word-document_merge_cells_vertical({
  filename: "report.docx",
  table_index: 0,
  col: 0,
  start_row: 1,
  end_row: 3
})
```

#### Cell Alignment and Padding

```javascript
// Set cell text alignment and internal padding
mcp_word-document_format_cell({
  filename: "report.docx",
  table_index: 0,
  row: 1,
  col: 2,
  alignment: "center",   // left | center | right
  vertical_alignment: "center",
  padding_top: 60,
  padding_bottom: 60,
  padding_left: 100,
  padding_right: 100
})
```

#### Professional Table Recipe (full workflow)

```javascript
// Step 1 – Create the table
mcp_word-document_add_table({
  filename: "report.docx",
  rows: 5,
  cols: 4,
  data: [
    ["Category", "Q1", "Q2", "Q3"],
    ["Revenue", "$1.2M", "$1.5M", "$1.8M"],
    ["Expenses", "$0.9M", "$1.1M", "$1.2M"],
    ["Profit", "$0.3M", "$0.4M", "$0.6M"],
    ["Margin", "25%", "27%", "33%"]
  ]
})
// Step 2 – Style header row and borders
mcp_word-document_format_table({
  filename: "report.docx",
  table_index: 0,
  border_style: "single",
  border_size: 4,
  border_color: "2E74B5",
  header_bg_color: "2E74B5",
  header_font_color: "FFFFFF",
  header_bold: true
})
// Step 3 – Alternating rows
mcp_word-document_apply_table_alternating_rows({
  filename: "report.docx",
  table_index: 0,
  color1: "FFFFFF",
  color2: "D6E4F0"
})
```

---

### Footnotes and Endnotes

#### Activate Footnote Tools

```javascript
activate_advanced_footnote_management(); // add, delete, style, validate footnotes
```

#### Add Footnotes

```javascript
// Add a footnote to a specific paragraph (0-based index)
mcp_word-document_add_footnote({
  filename: "report.docx",
  paragraph_index: 3,
  text: "Source: World Health Organization, 2025 Annual Report.",
  superscript_style: "FootnoteReference"
})

// Add an endnote (appears at end of document)
mcp_word-document_add_endnote({
  filename: "report.docx",
  paragraph_index: 7,
  text: "See Appendix B for full methodology."
})
```

#### Manage and Validate Footnotes

```javascript
// Validate all footnotes for formatting issues
mcp_word-document_validate_footnotes({
  filename: "report.docx"
})

// Delete a footnote by its reference index
mcp_word-document_delete_footnote({
  filename: "report.docx",
  footnote_index: 2
})

// Apply custom footnote style
mcp_word-document_customize_footnote_style({
  filename: "report.docx",
  font_name: "Arial",
  font_size: 9,
  color: "555555"
})
```

---

### Document Analysis and Content Extraction

#### Activate Analysis Tools

```javascript
activate_document_analysis_tools(); // find text, metadata, structure, comments
```

#### Find and Search Text

```javascript
// Find all occurrences of a phrase and return their paragraph indices
mcp_word-document_find_text({
  filename: "report.docx",
  search_text: "annual revenue",
  case_sensitive: false
})
// Returns: [{ paragraph_index: 4, text: "...annual revenue grew by 12%..." }, ...]
```

#### Extract Document Metadata

```javascript
// Get title, author, created date, last modified, word count
mcp_word-document_get_metadata({
  filename: "report.docx"
})
// Returns: { title, author, created, modified, word_count, page_count }
```

#### Get Document Structure

```javascript
// Return a structural outline: all headings, their levels and text
mcp_word-document_get_structure({
  filename: "report.docx"
})
// Returns: [{ level: 1, text: "Introduction" }, { level: 2, text: "Background" }, ...]
```

#### Extract All Text Content

```javascript
// Full text extraction paragraph by paragraph
mcp_word-document_extract_text({
  filename: "report.docx",
  include_tables: true,
  include_headers_footers: true
})
```

---

### Comments and Review Workflow

#### Activate Comment Tools

```javascript
activate_comment_management_tools_2(); // add, get, filter by author/paragraph
```

#### Add Comments

```javascript
// Add a review comment to a paragraph
mcp_word-document_add_comment({
  filename: "report.docx",
  paragraph_index: 5,
  text: "Please verify this statistic with the finance team.",
  author: "Jane Doe"
})
```

#### Retrieve Comments

```javascript
// Get all comments in the document
mcp_word-document_get_comments({
  filename: "report.docx"
})

// Get comments by a specific author
mcp_word-document_get_comments_by_author({
  filename: "report.docx",
  author: "Jane Doe"
})

// Get comments on a specific paragraph
mcp_word-document_get_comments_by_paragraph({
  filename: "report.docx",
  paragraph_index: 5
})
```

#### Resolve / Delete Comments

```javascript
// Delete a comment by its ID
mcp_word-document_delete_comment({
  filename: "report.docx",
  comment_id: "cmt_001"
})
```

---

### Contextual Insertions (Insert Near Existing Content)

#### Activate Contextual Insertion Tools

```javascript
activate_contextual_insertion_tools(); // insert header, lines, numbered lists near text
```

#### Insert Content Near Specific Text

```javascript
// Insert a new heading immediately before a paragraph containing search text
mcp_word-document_insert_heading_near_text({
  filename: "report.docx",
  search_text: "Executive Summary",
  heading_text: "2025 Financial Overview",
  level: 2,
  position: "before"   // before | after
})

// Insert a new line of text after a specific paragraph
mcp_word-document_insert_line_near_text({
  filename: "report.docx",
  search_text: "Total Revenue:",
  insert_text: "All values converted to USD at 2025 exchange rates.",
  position: "after",
  font_size: 9,
  italic: true,
  color: "888888"
})

// Insert a numbered list after a search anchor
mcp_word-document_insert_numbered_list_near_text({
  filename: "report.docx",
  search_text: "Next Steps",
  position: "after",
  items: [
    "Review draft with stakeholders",
    "Incorporate feedback by March 1",
    "Submit final version for approval"
  ]
})
```

---

### Security and Export

```javascript
mcp_word-document_convert_to_pdf({ filename: "report.docx", output_filename: "report.pdf" })
mcp_word-document_protect_document({ filename: "confidential.docx", password: "S3cur3Pass!" })
mcp_word-document_unprotect_document({ filename: "confidential.docx", password: "S3cur3Pass!" })
```

---

### End-to-End Professional Report Workflow

Canonical build order for a polished Word document:

```javascript
// ── 1. Activate ──────────────────────────────────────────────────
activate_document_creation_and_styling();
activate_document_structure_tools();
activate_basic_document_editing_tools();
activate_table_management_tools();
activate_advanced_footnote_management();
activate_document_analysis_tools();
activate_comment_management_tools_2();
activate_contextual_insertion_tools();
activate_document_security_and_conversion();

// ── 2. Create and brand ──────────────────────────────────────────
mcp_word-document_create_document({ filename: "report.docx", title: "Q3 Report", author: "Jane Smith" })
mcp_word-document_create_custom_style({ filename: "report.docx", style_name: "BrandH1", bold: true, font_size: 18, font_name: "Arial", color: "1B3A5C", base_style: "Heading 1" })

// ── 3. Title section ─────────────────────────────────────────────
mcp_word-document_add_heading({ filename: "report.docx", text: "Q3 2025 Performance Report", level: 1 })
mcp_word-document_add_paragraph({ filename: "report.docx", text: "Jane Smith · Finance · October 2025", font_size: 10 })
mcp_word-document_insert_page_break({ filename: "report.docx" })

// ── 4. Body content ──────────────────────────────────────────────
mcp_word-document_add_heading({ filename: "report.docx", text: "Executive Summary", level: 1 })
mcp_word-document_add_paragraph({ filename: "report.docx", text: "..." })
mcp_word-document_add_heading({ filename: "report.docx", text: "Financial Results", level: 2 })

// ── 5. Styled table ───────────────────────────────────────────────
mcp_word-document_add_table({ filename: "report.docx", rows: 4, cols: 3,
  data: [["Metric","Q2","Q3"],["Revenue","$1.5M","$1.8M"],["Profit","$0.4M","$0.6M"],["Margin","27%","33%"]] })
mcp_word-document_format_table({ filename: "report.docx", table_index: 0,
  border_style: "single", header_bg_color: "1B3A5C", header_font_color: "FFFFFF", header_bold: true })
mcp_word-document_apply_table_alternating_rows({ filename: "report.docx", table_index: 0, color1: "FFFFFF", color2: "D6EAF8" })

// ── 6. Image + footnote ───────────────────────────────────────────
mcp_word-document_insert_image({ filename: "report.docx", image_path: "./chart.png", width: 6.0, alignment: "center" })
mcp_word-document_add_footnote({ filename: "report.docx", paragraph_index: 8, text: "Source: Internal BI system, Q3 2025." })

// ── 7. Replace template placeholders ─────────────────────────────
mcp_word-document_search_and_replace({ filename: "report.docx", find_text: "[DIVISION]", replace_text: "Asia Pacific" })

// ── 8. Add review comments for uncertain data ────────────────────
mcp_word-document_add_comment({ filename: "report.docx", paragraph_index: 12, text: "Confirm with regional leads.", author: "Jane Doe" })

// ── 9. Export ────────────────────────────────────────────────────
mcp_word-document_convert_to_pdf({ filename: "report.docx", output_filename: "report_q3_2025.pdf" })
```

---

## Part 2: Document Structure Standards

### Word Document Structure

1. **Title Page**: Document title, subtitle, date, author
2. **Table of Contents**: Auto-generated from headings
3. **Executive Summary**: Key points overview
4. **Main Content**: Structured with headers
5. **Appendices**: Supporting materials

### Formatting Standards

#### Fonts
- **Headings**: Bold, larger (16-24pt)
- **Body**: Readable size (11-12pt)
- **Code**: Monospace font (Consolas, Monaco)
- **Consistency**: Use same font families throughout

#### Colors
- **Primary**: Main brand or accent color (use 60-70%)
- **Secondary**: Supporting colors (20-30%)
- **Neutral**: Headers, borders, backgrounds (remaining %)

#### Spacing
- **Consistent margins**: Standard settings (e.g., 1" margins)
- **White space**: Don't crowd content
- **Alignment**: Use grid-based spacing
- **Visual hierarchy**: Size and weight guide eye

---

## Part 3: Quality Checklist

```markdown
## Word Document Quality Checklist

### Structure
- [ ] Title page with required metadata
- [ ] Clear heading hierarchy (H1 > H2 > H3)
- [ ] Logical content flow with page breaks between major sections
- [ ] Appendices for supporting material

### Content
- [ ] Executive summary for long documents
- [ ] Clear problem/solution structure
- [ ] Numbered/bulleted lists used for sequential or parallel items
- [ ] Inline formatting (bold/italic/color) applied sparingly for emphasis
- [ ] Footnotes/endnotes used for citations (not inline clutter)
- [ ] Tables used for comparative or tabular data (not prose)
- [ ] Appropriate depth for audience

### Formatting
- [ ] Consistent fonts and sizes (Arial 11pt body, 16pt H1, 13pt H2)
- [ ] Proper paragraph spacing (no double blank lines)
- [ ] Tables have styled headers (colored background, white bold text)
- [ ] Tables use alternating row colors for readability
- [ ] Merged header cells where table spans a topic
- [ ] Figures and tables have captions

### Visual Elements
- [ ] Images are high resolution and properly anchored
- [ ] Diagrams are readable when printed (min 600px width)
- [ ] Colors are accessible (sufficient contrast ratio)
- [ ] Captions and alt text included

### Comments and Review
- [ ] Review comments added for sections requiring validation
- [ ] All placeholder comments resolved before final distribution
- [ ] Document metadata (title, author, date) set correctly
```

---

## Part 4: MCP Tool Activation Guide

### Activation Commands

When working with Word documents, use these MCP activation patterns:

```javascript
// Word documents — activate in this order for full capability
activate_document_creation_and_styling();    // create_document, create_custom_style
activate_document_structure_tools();         // add_heading, add_paragraph (lists, custom styles)
activate_basic_document_editing_tools();     // insert_image, insert_page_break, delete_paragraph, format_text, add_footnote, add_endnote
activate_table_management_tools();           // add_table, borders/shading, merge cells, cell padding
activate_advanced_footnote_management();     // advanced footnotes: add, delete, style, validate
activate_document_analysis_tools();          // find_text, get_metadata, get_structure, extract_text
activate_comment_management_tools_2();       // add/get/delete comments (by author or paragraph)
activate_contextual_insertion_tools();       // insert heading/line/list near existing text
activate_document_security_and_conversion(); // convert_to_pdf, protect, unprotect
```

### Workflow Examples

#### Template-Based Document Generation

1. **Start with template** (Word)
2. **Copy template** to new filename
3. **Search and replace** placeholders with actual data
4. **Customize content** with domain-specific information
5. **Apply styling** consistently across document sections
6. **Export final version** in required format

---

## Part 5: Best Practices

### MCP-Specific Best Practices

- **Activate tools as needed**: Enable MCP tool groups only when required to avoid unnecessary overhead
- **Validate operations**: Confirm operations completed successfully, especially for batch operations
- **Handle errors gracefully**: Catch and report MCP tool errors with context for troubleshooting
- **Batch operations**: Use array-based operations when available for efficiency
- **Document file paths**: Use clear, relative paths and maintain documentation of file locations

---

## References & Resources

### Documentation
- [DOCX Formatting Reference](./references/docx-formatting-reference.md) — Word document formatting with docx-js API

### Examples
- [Report Generation Example](./examples/report-generation-example.md) — Professional Word report generation workflow

### Scripts
- [DOC Template Generator](./scripts/doc-template-generator.py) — Python script for document template generation

---
