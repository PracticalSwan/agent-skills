# Excel Workbook Examples

## Example 1: Creating a Quarterly Report

```javascript
// Activate required tools
activate_worksheet_management_tools();
activate_cell_management_tools();
activate_column_management_tools();

// Create workbook
mcp_excel_create_workbook({ filename: "q3_report.xlsx" });

// Rename and create sheets
mcp_excel_rename_worksheet({ filename: "q3_report.xlsx", old_name: "Sheet1", new_name: "Summary" });
mcp_excel_create_worksheet({ filename: "q3_report.xlsx", sheet_name: "Raw Data" });
mcp_excel_create_worksheet({ filename: "q3_report.xlsx", sheet_name: "Charts" });

// Write headers to Summary sheet
mcp_excel_write_cell({ filename: "q3_report.xlsx", sheet_name: "Summary", cell: "A1", value: "Region" });
mcp_excel_write_cell({ filename: "q3_report.xlsx", sheet_name: "Summary", cell: "B1", value: "Q1" });
mcp_excel_write_cell({ filename: "q3_report.xlsx", sheet_name: "Summary", cell: "C1", value: "Q2" });
mcp_excel_write_cell({ filename: "q3_report.xlsx", sheet_name: "Summary", cell: "D1", value: "Q3" });
mcp_excel_write_cell({ filename: "q3_report.xlsx", sheet_name: "Summary", cell: "E1", value: "Total" });
mcp_excel_write_cell({ filename: "q3_report.xlsx", sheet_name: "Summary", cell: "F1", value: "Change %" });

// Format header row
mcp_excel_format_range({
  filename: "q3_report.xlsx",
  sheet_name: "Summary",
  range: "A1:F1",
  bold: true,
  font_color: "FFFFFF",
  bg_color: "1B3A5C",
  alignment: "center"
});

// Write data rows
mcp_excel_write_cell({ filename: "q3_report.xlsx", sheet_name: "Summary", cell: "A2", value: "Americas" });
mcp_excel_write_cell({ filename: "q3_report.xlsx", sheet_name: "Summary", cell: "B2", value: 1200000 });
mcp_excel_write_cell({ filename: "q3_report.xlsx", sheet_name: "Summary", cell: "C2", value: 1350000 });
mcp_excel_write_cell({ filename: "q3_report.xlsx", sheet_name: "Summary", cell: "D2", value: 1380000 });
mcp_excel_write_cell({ filename: "q3_report.xlsx", sheet_name: "Summary", cell: "E2", value: "=SUM(B2:D2)" });
mcp_excel_write_cell({ filename: "q3_report.xlsx", sheet_name: "Summary", cell: "F2", value: "=(D2-B2)/B2" });

// Format data row
mcp_excel_format_range({
  filename: "q3_report.xlsx",
  sheet_name: "Summary",
  range: "A2:F2",
  bg_color: "D6EAF8"
});

// Add chart
mcp_excel_create_chart({
  filename: "q3_report.xlsx",
  sheet_name: "Charts",
  chart_type: "column",
  data_sheet: "Summary",
  data_range: "A1:E3",
  title: "Revenue by Region & Quarter",
  position: { left: 1, top: 1, width: 8, height: 5 }
});
```

## Example 2: Data Analysis Workbook

```javascript
// Create data analysis workbook
activate_worksheet_management_tools();
activate_cell_management_tools();

mcp_excel_create_workbook({ filename: "data_analysis.xlsx" });
mcp_excel_rename_worksheet({ filename: "data_analysis.xlsx", old_name: "Sheet1", new_name: "Data" });
mcp_excel_create_worksheet({ filename: "data_analysis.xlsx", sheet_name: "Analysis" });
mcp_excel_create_worksheet({ filename: "data_analysis.xlsx", sheet_name: "Pivot" });

// Write data headers
const headers = ["Date", "Product", "Category", "Region", "Sales", "Quantity"];
headers.forEach((h, i) => {
  mcp_excel_write_cell({
    filename: "data_analysis.xlsx",
    sheet_name: "Data",
    cell: String.fromCharCode(65 + i) + "1",
    value: h
  });
});

// Format headers
mcp_excel_format_range({
  filename: "data_analysis.xlsx",
  sheet_name: "Data",
  range: "A1:F1",
  bold: true,
  bg_color: "4472C4",
  font_color: "FFFFFF"
});

// Write sample data
const data = [
  ["2025-01-15", "Widget A", "Electronics", "Americas", 15000, 100],
  ["2025-01-16", "Widget B", "Electronics", "EMEA", 12000, 80],
  ["2025-01-17", "Gadget C", "Accessories", "APAC", 8500, 120]
];

data.forEach((row, rowIndex) => {
  row.forEach((value, colIndex) => {
    mcp_excel_write_cell({
      filename: "data_analysis.xlsx",
      sheet_name: "Data",
      cell: String.fromCharCode(65 + colIndex) + (rowIndex + 2),
      value: value
    });
  });
});

// Create pivot table
mcp_excel_create_pivot_table({
  filename: "data_analysis.xlsx",
  source_sheet: "Data",
  source_range: "A1:F100",
  destination_sheet: "Pivot",
  destination_cell: "A3",
  rows: ["Region", "Category"],
  columns: [],
  values: [{ field: "Sales", aggregation: "sum" }]
});
```

## Example 3: Budget Tracker

```javascript
// Create personal budget tracker
activate_worksheet_management_tools();
activate_cell_management_tools();

mcp_excel_create_workbook({ filename: "budget_tracker.xlsx" });
mcp_excel_rename_worksheet({ filename: "budget_tracker.xlsx", old_name: "Sheet1", new_name: "Budget" });

// Budget template headers
mcp_excel_write_cell({ filename: "budget_tracker.xlsx", sheet_name: "Budget", cell: "A1", value: "Category" });
mcp_excel_write_cell({ filename: "budget_tracker.xlsx", sheet_name: "Budget", cell: "B1", value: "Budgeted" });
mcp_excel_write_cell({ filename: "budget_tracker.xlsx", sheet_name: "Budget", cell: "C1", value: "Actual" });
mcp_excel_write_cell({ filename: "budget_tracker.xlsx", sheet_name: "Budget", cell: "D1", value: "Difference" });
mcp_excel_write_cell({ filename: "budget_tracker.xlsx", sheet_name: "Budget", cell: "E1", value: "Status" });

// Format headers
mcp_excel_format_range({
  filename: "budget_tracker.xlsx",
  sheet_name: "Budget",
  range: "A1:E1",
  bold: true,
  bg_color: "203864",
  font_color: "FFFFFF"
});

// Budget categories
const categories = [
  ["Housing", 2000, "=C2"],
  ["Food", 600, "=C3"],
  ["Transportation", 400, "=C4"],
  ["Utilities", 300, "=C5"],
  ["Entertainment", 200, "=C6"],
  ["Savings", 1000, "=C7"]
];

categories.forEach((cat, i) => {
  const row = i + 2;
  mcp_excel_write_cell({ filename: "budget_tracker.xlsx", sheet_name: "Budget", cell: `A${row}`, value: cat[0] });
  mcp_excel_write_cell({ filename: "budget_tracker.xlsx", sheet_name: "Budget", cell: `B${row}`, value: cat[1] });
  mcp_excel_write_cell({ filename: "budget_tracker.xlsx", sheet_name: "Budget", cell: `D${row}`, value: `=C${row}-B${row}` });

  // Status formula
  mcp_excel_write_cell({
    filename: "budget_tracker.xlsx",
    sheet_name: "Budget",
    cell: `E${row}`,
    value: `=IF(D${row}>0,"Under Budget",IF(D${row}<0,"Over Budget","On Target"))`
  });

  // Alternate row shading
  const bgColor = i % 2 === 0 ? "FFFFFF" : "E7E6E6";
  mcp_excel_format_range({
    filename: "budget_tracker.xlsx",
    sheet_name: "Budget",
    range: `A${row}:E${row}`,
    bg_color: bgColor
  });
});

// Total row
const totalRow = categories.length + 2;
mcp_excel_write_cell({ filename: "budget_tracker.xlsx", sheet_name: "Budget", cell: `A${totalRow}`, value: "TOTAL" });
mcp_excel_write_cell({ filename: "budget_tracker.xlsx", sheet_name: "Budget", cell: `B${totalRow}`, value: `=SUM(B2:B${totalRow-1})` });
mcp_excel_write_cell({ filename: "budget_tracker.xlsx", sheet_name: "Budget", cell: `C${totalRow}`, value: `=SUM(C2:C${totalRow-1})` });
mcp_excel_write_cell({ filename: "budget_tracker.xlsx", sheet_name: "Budget", cell: `D${totalRow}`, value: `=C${totalRow}-B${totalRow}` });

// Format total row
mcp_excel_format_range({
  filename: "budget_tracker.xlsx",
  sheet_name: "Budget",
  range: `A${totalRow}:E${totalRow}`,
  bold: true,
  bg_color: "203864",
  font_color: "FFFFFF"
});
```

## Example 4: Project Timeline Tracker

```javascript
// Create project timeline workbook
activate_worksheet_management_tools();
activate_cell_management_tools();

mcp_excel_create_workbook({ filename: "project_timeline.xlsx" });
mcp_excel_rename_worksheet({ filename: "project_timeline.xlsx", old_name: "Sheet1", new_name: "Timeline" });

// Timeline headers
mcp_excel_write_cell({ filename: "project_timeline.xlsx", sheet_name: "Timeline", cell: "A1", value: "Task" });
mcp_excel_write_cell({ filename: "project_timeline.xlsx", sheet_name: "Timeline", cell: "B1", value: "Start Date" });
mcp_excel_write_cell({ filename: "project_timeline.xlsx", sheet_name: "Timeline", cell: "C1", value: "End Date" });
mcp_excel_write_cell({ filename: "project_timeline.xlsx", sheet_name: "Timeline", cell: "D1", value: "Duration (Days)" });
mcp_excel_write_cell({ filename: "project_timeline.xlsx", sheet_name: "Timeline", cell: "E1", value: "Status" });
mcp_excel_write_cell({ filename: "project_timeline.xlsx", sheet_name: "Timeline", cell: "F1", value: "Assigned To" });

// Format headers
mcp_excel_format_range({
  filename: "project_timeline.xlsx",
  sheet_name: "Timeline",
  range: "A1:F1",
  bold: true,
  bg_color: "2E5090",
  font_color: "FFFFFF"
});

// Project tasks
const tasks = [
  ["Requirements Gathering", "2025-01-01", "2025-01-14", "=C2-B2", "Completed", "Alice"],
  ["Design Phase", "2025-01-15", "2025-01-31", "=C3-B3", "Completed", "Bob"],
  ["Development", "2025-02-01", "2025-02-28", "=C4-B4", "In Progress", "Charlie"],
  ["Testing", "2025-03-01", "2025-03-15", "=C5-B5", "Not Started", "Diana"],
  ["Deployment", "2025-03-16", "2025-03-20", "=C6-B6", "Not Started", "Alice"]
];

tasks.forEach((task, i) => {
  const row = i + 2;
  task.forEach((value, colIndex) => {
    mcp_excel_write_cell({
      filename: "project_timeline.xlsx",
      sheet_name: "Timeline",
      cell: String.fromCharCode(65 + colIndex) + row,
      value: value
    });
  });

  // Format data row
  mcp_excel_format_range({
    filename: "project_timeline.xlsx",
    sheet_name: "Timeline",
    range: `A${row}:F${row}`,
    bg_color: i % 2 === 0 ? "FFFFFF" : "D9E1F2"
  });
});

// Merge cells for project title
mcp_excel_merge_cells({
  filename: "project_timeline.xlsx",
  sheet_name: "Timeline",
  range: "A1:F1"
});
```
