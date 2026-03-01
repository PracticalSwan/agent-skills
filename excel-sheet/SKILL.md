---
name: excel-sheet
description: Excel (.xlsx) manipulation via MCP server. Use for creating workbooks, formatting cells, writing formulas, building charts, pivot tables, data analysis, or any task involving Excel spreadsheets.
license: Complete terms in LICENSE.txt
---



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`


Comprehensive skill for working with Microsoft Excel spreadsheets using MCP servers.

## When to Use This Skill

- Any task where .xlsx is an input, output, or transformation target
- Creating, editing, formatting, or analyzing Excel files
- Building workbooks from data or templates
- Applying consistent formatting and formulas
- Automating Excel workflows via MCP tools

### Typical Activation Triggers

- .xlsx work: spreadsheets, workbooks, worksheets, data analysis
- Cell operations: read, write, format, merge/unmerge
- Worksheet management: create, copy, delete, rename
- Analysis: charts, pivot tables, formulas

---

## Part 1: Excel Spreadsheets (.xlsx) via MCP

## Quick Reference

| Task | Activation / Tool |
|------|-------------------|
| Create workbook; create/copy/delete/rename worksheets; add charts; add pivot tables | `activate_worksheet_management_tools` |
| Copy/delete/format/merge/unmerge cells; delete rows | `activate_cell_management_tools` |
| Insert/delete columns | `activate_column_management_tools` |

> **Note:** There is no `activate_workbook_management` — workbook creation is part of `activate_worksheet_management_tools`.

### Tool Activation Order

```javascript
activate_worksheet_management_tools();  // workbook + sheet management, charts, pivot tables
activate_cell_management_tools();        // cell CRUD, formatting, merge/unmerge, delete rows
activate_column_management_tools();      // insert/delete columns
```

---

### Workbook and Worksheet Operations

```javascript
// Create a new workbook
mcp_excel_create_workbook({ filename: "report.xlsx" })

// Create worksheets (call per sheet needed)
mcp_excel_create_worksheet({ filename: "report.xlsx", sheet_name: "Summary" })
mcp_excel_create_worksheet({ filename: "report.xlsx", sheet_name: "Raw Data" })
mcp_excel_create_worksheet({ filename: "report.xlsx", sheet_name: "Charts" })

// Copy a worksheet (good for applying template structure)
mcp_excel_copy_worksheet({ filename: "report.xlsx", source_sheet: "Summary", destination_sheet: "Summary_Q2" })

// Rename a worksheet
mcp_excel_rename_worksheet({ filename: "report.xlsx", old_name: "Sheet1", new_name: "Dashboard" })

// Delete a worksheet
mcp_excel_delete_worksheet({ filename: "report.xlsx", sheet_name: "Sheet1" })
```

---

### Cell Content: Write, Copy, Delete

> Activate: `activate_cell_management_tools()`

```javascript
// Write a value or formula to a cell
mcp_excel_write_cell({ filename: "report.xlsx", sheet_name: "Summary", cell: "B2", value: "Revenue" })
mcp_excel_write_cell({ filename: "report.xlsx", sheet_name: "Summary", cell: "C2", value: 1800000 })
// Write a formula
mcp_excel_write_cell({ filename: "report.xlsx", sheet_name: "Summary", cell: "D2", value: "=C2-B2" })

// Copy a cell range to another location (e.g. duplicate template rows)
mcp_excel_copy_range({
  filename: "report.xlsx",
  sheet_name: "Raw Data",
  source_range: "A1:F1",           // header row
  destination_cell: "A100"          // paste starting cell
})

// Delete a cell range (clear content)
mcp_excel_delete_range({ filename: "report.xlsx", sheet_name: "Raw Data", range: "G2:G50" })

// Delete an entire row (rows shift up)
mcp_excel_delete_row({ filename: "report.xlsx", sheet_name: "Raw Data", row_index: 5 })
```

---

### Cell Formatting

```javascript
// Format a single cell (header style)
mcp_excel_format_cell({
  filename: "report.xlsx",
  sheet_name: "Summary",
  cell: "A1",
  bold: true,
  font_size: 12,
  font_color: "FFFFFF",
  bg_color: "1B3A5C",
  alignment: "center",
  border: "thin"
})

// Format a range (apply consistent styling across headers)
mcp_excel_format_range({
  filename: "report.xlsx",
  sheet_name: "Summary",
  range: "A1:F1",
  bold: true,
  font_color: "FFFFFF",
  bg_color: "1B3A5C",
  alignment: "center"
})

// Format data rows (alternate shading — apply to even rows manually or via range loop)
mcp_excel_format_range({
  filename: "report.xlsx",
  sheet_name: "Summary",
  range: "A2:F2",
  bg_color: "D6EAF8"
})
```

---

### Merge and Unmerge Cells

```javascript
// Merge cells for a section header spanning columns
mcp_excel_merge_cells({ filename: "report.xlsx", sheet_name: "Summary", range: "A1:F1" })

// Unmerge if editing is needed
mcp_excel_unmerge_cells({ filename: "report.xlsx", sheet_name: "Summary", range: "A1:F1" })
```

---

### Column Management

> Activate: `activate_column_management_tools()`

```javascript
// Insert a blank column before column C (index 2, 0-based)
mcp_excel_insert_column({ filename: "report.xlsx", sheet_name: "Summary", column_index: 2 })

// Delete a column (e.g. remove a scratch column)
mcp_excel_delete_column({ filename: "report.xlsx", sheet_name: "Summary", column_index: 6 })
```

---

### Charts

> Activate: `activate_worksheet_management_tools()`

```javascript
// Add a chart to a worksheet
mcp_excel_create_chart({
  filename: "report.xlsx",
  sheet_name: "Charts",
  chart_type: "bar",         // bar | line | pie | column | area
  data_sheet: "Summary",
  data_range: "A1:D5",
  title: "Revenue by Quarter",
  position: { left: 1, top: 1, width: 8, height: 5 }  // inches
})
```

---

### Pivot Tables

```javascript
// Create a pivot table from raw data
mcp_excel_create_pivot_table({
  filename: "report.xlsx",
  source_sheet: "Raw Data",
  source_range: "A1:F200",
  destination_sheet: "Pivot",
  destination_cell: "A3",
  rows: ["Region", "Product"],
  columns: ["Quarter"],
  values: [{ field: "Revenue", aggregation: "sum" }]
})
```

---

### End-to-End Excel Workbook Workflow

```javascript
// ── 1. Activate ──────────────────────────────────────────────────
activate_worksheet_management_tools();
activate_cell_management_tools();
activate_column_management_tools();

// ── 2. Create workbook and sheets ────────────────────────────────
mcp_excel_create_workbook({ filename: "q3_report.xlsx" })
mcp_excel_rename_worksheet({ filename: "q3_report.xlsx", old_name: "Sheet1", new_name: "Summary" })
mcp_excel_create_worksheet({ filename: "q3_report.xlsx", sheet_name: "Raw Data" })
mcp_excel_create_worksheet({ filename: "q3_report.xlsx", sheet_name: "Charts" })

// ── 3. Write headers (Summary sheet) ─────────────────────────────
const headers = [["Region","Q1","Q2","Q3","Total","Change%"]]
// write each header cell then format the range
mcp_excel_write_cell({ filename:"q3_report.xlsx", sheet_name:"Summary", cell:"A1", value:"Region" })
mcp_excel_write_cell({ filename:"q3_report.xlsx", sheet_name:"Summary", cell:"F1", value:"Change%" })
mcp_excel_format_range({ filename:"q3_report.xlsx", sheet_name:"Summary", range:"A1:F1",
  bold:true, font_color:"FFFFFF", bg_color:"1B3A5C", alignment:"center" })

// ── 4. Write data rows + formulas ────────────────────────────────
mcp_excel_write_cell({ filename:"q3_report.xlsx", sheet_name:"Summary", cell:"A2", value:"APAC" })
mcp_excel_write_cell({ filename:"q3_report.xlsx", sheet_name:"Summary", cell:"B2", value:1200000 })
mcp_excel_write_cell({ filename:"q3_report.xlsx", sheet_name:"Summary", cell:"E2", value:"=SUM(B2:D2)" })
mcp_excel_write_cell({ filename:"q3_report.xlsx", sheet_name:"Summary", cell:"F2", value:"=(D2-B2)/B2" })

// ── 5. Style data rows (alternating) ─────────────────────────────
mcp_excel_format_range({ filename:"q3_report.xlsx", sheet_name:"Summary", range:"A2:F2", bg_color:"D6EAF8" })
mcp_excel_format_range({ filename:"q3_report.xlsx", sheet_name:"Summary", range:"A3:F3", bg_color:"FFFFFF" })

// ── 6. Add chart ─────────────────────────────────────────────────
mcp_excel_create_chart({ filename:"q3_report.xlsx", sheet_name:"Charts",
  chart_type:"column", data_sheet:"Summary", data_range:"A1:D5",
  title:"Revenue by Region & Quarter", position:{ left:1, top:1, width:9, height:5 } })

// ── 7. Pivot table ───────────────────────────────────────────────
mcp_excel_create_pivot_table({ filename:"q3_report.xlsx",
  source_sheet:"Raw Data", source_range:"A1:F200",
  destination_sheet:"Summary", destination_cell:"A20",
  rows:["Region"], columns:["Quarter"], values:[{ field:"Revenue", aggregation:"sum" }] })
```

---

## Part 2: Workbook Structure Standards

### Excel Workbook Structure

1. **Summary Sheet**: Key metrics and insights
2. **Data Source Sheet**: Raw data
3. **Calculations Sheet**: Formulas and logic
4. **Analysis Sheets**: Pivot tables, charts
5. **Documentation Sheet**: Assumptions and notes

### Formatting Standards

#### Fonts
- **Headings**: Bold, larger (12-14pt)
- **Body**: Readable size (10-11pt)
- **Consistency**: Use same font families throughout

#### Colors
- **Headers**: Brand color background, white text
- **Data rows**: Alternating colors for readability
- **Highlights**: Use for key metrics or alerts

#### Spacing
- **Consistent column widths**: Auto-fit or standard widths
- **Row heights**: appropriate for content
- **Alignment**: Left for text, right for numbers

---

## Part 3: Quality Checklist

```markdown
## Excel Quality Checklist

### Structure
- [ ] Separate sheets: Summary | Raw Data | Charts | (Pivot)
- [ ] Sheet 1 renamed from "Sheet1" to "Summary" or "Dashboard"
- [ ] Header row formatted (bold, brand color bg, white text)
- [ ] Header row frozen (row 1) where needed

### Data Integrity
- [ ] Formulas used for totals/ratios (never hardcoded)
- [ ] No merged cells inside data ranges (only in header/title areas)
- [ ] Consistent column data types (all numbers, all dates, etc.)
- [ ] Empty rows/columns cleaned up (delete_row / delete_column)

### Analysis
- [ ] Chart added to Charts sheet with clear title and labeled axes
- [ ] Pivot table added for large datasets
- [ ] Alternating row shading applied for readability

### Validation
- [ ] Formulas reference correct sheet and range (test with sample values)
- [ ] Pivot table source range includes all data rows
- [ ] Chart data range verified to match actual data
```

---

## Part 4: Common Excel Formulas

### Lookup Formulas

#### VLOOKUP

```
=VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])
```

**Examples:**
```
=VLOOKUP("SKU-100", A2:D50, 3, FALSE)
  → Find SKU-100 in column A, return value from column C

=VLOOKUP(B2, Products!A:E, 4, FALSE)
  → Cross-sheet lookup; find B2's value in Products sheet column A, return column D
```

#### XLOOKUP

```
=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])
```

**Examples:**
```
=XLOOKUP("Widget", B2:B100, E2:E100, "Not found")
  → Search B column for "Widget", return corresponding E value

=XLOOKUP(TODAY(), A2:A100, B2:B100, , -1)
  → Find today's date or nearest earlier date, return column B
```

### Math Formulas

#### SUM

```
=SUM(A1:A100)                    → Sum a range
=SUM(A1:A100, C1:C100)           → Sum multiple ranges
```

#### SUMIF / SUMIFS

```
=SUMIF(range, criteria, [sum_range])
=SUMIFS(sum_range, criteria_range1, criteria1, [criteria_range2, criteria2, ...])
```

**Examples:**
```
=SUMIF(B2:B100, "Electronics", D2:D100)
  → Sum column D where column B = "Electronics"

=SUMIFS(E2:E100, B2:B100, "West", C2:C100, ">=2025-01-01")
  → Sum E where region is "West" AND date ≥ Jan 1 2025
```

### Text Formulas

#### CONCATENATE / CONCAT / TEXTJOIN

```
=CONCATENATE(A1, " ", B1)          → "John Smith" (legacy)
=CONCAT(A1, " ", B1)               → Same, modern
=A1 & " " & B1                     → Operator shorthand

=TEXTJOIN(", ", TRUE, A1:A10)
  → Join non-empty cells with comma+space: "Alpha, Beta, Gamma"
```

### Date Formulas

#### TODAY / NOW

```
=TODAY()          → Current date (no time)
=NOW()            → Current date and time
=TODAY() + 30     → 30 days from today
```

#### DATEDIF

```
=DATEDIF(start_date, end_date, unit)
```

| Unit  | Returns                          |
|-------|----------------------------------|
| "Y"   | Complete years                   |
| "M"   | Complete months                  |
| "D"   | Days                             |

**Examples:**
```
=DATEDIF(A1, TODAY(), "Y")         → Years since date in A1
=DATEDIF(A1, A2, "M")             → Months between two dates
```

### Statistical Formulas

#### AVERAGE / MEDIAN

```
=AVERAGE(A1:A100)                → Arithmetic mean
=AVERAGEIF(B1:B100, ">0")       → Average of positive values only
=MEDIAN(A1:A100)                 → Middle value
```

#### COUNT / COUNTA / COUNTIF / COUNTIFS

```
=COUNT(A1:A100)                                → Count numeric cells
=COUNTA(A1:A100)                               → Count non-empty cells
=COUNTIF(B1:B100, "Complete")                  → Count cells matching criteria
=COUNTIF(C1:C100, ">500")                      → Count cells > 500
=COUNTIFS(B1:B100, "East", C1:C100, ">1000")   → Multiple criteria
```

### Conditional Formulas

#### IF

```
=IF(condition, value_if_true, value_if_false)
```

**Examples:**
```
=IF(A1>=90, "A", IF(A1>=80, "B", IF(A1>=70, "C", "F")))
  → Nested grade assignment

=IF(AND(B1>0, C1>0), B1*C1, 0)
  → Multiply only if both positive
```

#### IFS (Excel 2019+)

Evaluates multiple conditions in order — first TRUE wins.

```
=IFS(A1>=90, "A", A1>=80, "B", A1>=70, "C", TRUE, "F")
  → Cleaner than nested IF; TRUE acts as default/else
```

---

## Part 5: MCP Tool Activation Guide

### Activation Commands

When working with Excel spreadsheets, use these MCP activation patterns:

```javascript
// Excel documents (no activate_workbook_management — worksheet tools cover workbook creation)
activate_worksheet_management_tools();  // create workbook, worksheets, charts, pivot tables
activate_cell_management_tools();        // write/copy/delete cells, formatting, merge/unmerge
activate_column_management_tools();      // insert/delete columns
```

### Workflow Examples

#### Template-Based Workbook Generation

1. **Start with template** (Excel)
2. **Copy template** to new filename
3. **Write data** to appropriate cells
4. **Apply formulas** for calculations
5. **Apply formatting** consistently across sheets
6. **Save final version**

---

## Part 6: Best Practices

### MCP-Specific Best Practices

- **Activate tools as needed**: Enable MCP tool groups only when required to avoid unnecessary overhead
- **Validate operations**: Confirm operations completed successfully, especially for batch operations
- **Handle errors gracefully**: Catch and report MCP tool errors with context for troubleshooting
- **Batch operations**: Use array-based operations when available for efficiency
- **Document file paths**: Use clear, relative paths and maintain documentation of file locations

### Excel Best Practices

- **Use formulas**: Never hardcode calculated values
- **Consistent formatting**: Apply same styles across sheets
- **Clear naming**: Use descriptive sheet and range names
- **Data validation**: Use dropdown lists and constraints
- **Test formulas**: Verify with sample data before distribution

---

## References & Resources

### Documentation
- [Excel Formulas Reference](./references/excel-formulas-reference.md) — Excel formula patterns and Power Query M basics

### Examples
- [Excel Workbook Examples](./examples/excel-workbook-examples.md) — Examples of creating workbooks programmatically

### Scripts
- [CSV to XLSX Converter](./scripts/csv-to-xlsx.py) — Python script to convert CSV files to formatted Excel workbooks

### Usage

```bash
# Basic usage
python csv-to-xlsx.py input.csv

# Specify output file
python csv-to-xlsx.py input.csv -o output.xlsx

# Custom header colors
python csv-to-xlsx.py input.csv --header-color 2E74B5 --header-font-color FFFFFF

# Generate chart from numeric columns
python csv-to-xlsx.py input.csv --chart --chart-type bar
```

### Requirements

```bash
pip install openpyxl
```

---


---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [microsoft-development](../microsoft-development/SKILL.md) | Microsoft SDK and docs reference |
| [powerbi-modeling](../powerbi-modeling/SKILL.md) | Export data for Power BI modeling |
| [word-document](../word-document/SKILL.md) | Embed Excel data in Word reports |
| [powerpoint-ppt](../powerpoint-ppt/SKILL.md) | Insert charts into presentations |
