# Excel Formulas and Data Manipulation Reference

Comprehensive reference for Excel formulas, data patterns, and programmatic spreadsheet manipulation.

---

## Lookup Formulas

### VLOOKUP

Searches the first column of a range and returns a value from a specified column.

```
=VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])
```

| Parameter     | Description                                      |
|---------------|--------------------------------------------------|
| lookup_value  | Value to search for in the first column           |
| table_array   | Range containing the data                         |
| col_index_num | Column number to return (1-based)                 |
| range_lookup  | FALSE = exact match, TRUE = approximate match     |

**Examples:**

```
=VLOOKUP("SKU-100", A2:D50, 3, FALSE)
  → Find SKU-100 in column A, return value from column C

=VLOOKUP(B2, Products!A:E, 4, FALSE)
  → Cross-sheet lookup; find B2's value in Products sheet column A, return column D
```

**Limitations:** Only searches left-to-right. Use INDEX/MATCH or XLOOKUP for reverse lookups.

### XLOOKUP

Modern replacement for VLOOKUP — searches any direction, supports multiple match modes.

```
=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])
```

| Parameter     | Description                                                        |
|---------------|--------------------------------------------------------------------|
| lookup_value  | Value to search for                                                |
| lookup_array  | Array or range to search                                           |
| return_array  | Array or range to return from                                      |
| if_not_found  | Value to return if no match (default: #N/A)                        |
| match_mode    | 0 = exact, -1 = exact or next smaller, 1 = exact or next larger    |
| search_mode   | 1 = first-to-last, -1 = last-to-first, 2 = binary asc, -2 = desc  |

**Examples:**

```
=XLOOKUP("Widget", B2:B100, E2:E100, "Not found")
  → Search B column for "Widget", return corresponding E value

=XLOOKUP(TODAY(), A2:A100, B2:B100, , -1)
  → Find today's date or nearest earlier date, return column B

=XLOOKUP(D2, Products[SKU], Products[Name]&" - "&Products[Category])
  → Return concatenated result from structured table
```

### INDEX / MATCH

The classic flexible lookup combination — works in any direction.

```
=INDEX(return_range, MATCH(lookup_value, lookup_range, match_type))
```

MATCH `match_type`: 0 = exact, 1 = largest value ≤ lookup (sorted asc), -1 = smallest value ≥ lookup (sorted desc).

**Examples:**

```
=INDEX(C2:C100, MATCH("Target", A2:A100, 0))
  → Find "Target" in column A, return corresponding column C value

=INDEX(A2:A100, MATCH(MAX(D2:D100), D2:D100, 0))
  → Return the name (column A) for the row with the highest value in column D

=INDEX(B2:D100, MATCH("ID-55", A2:A100, 0), 3)
  → Two-dimensional: find row by ID in A, return 3rd column of B:D range
```

---

## Math Formulas

### SUM

```
=SUM(A1:A100)                    → Sum a range
=SUM(A1:A100, C1:C100)           → Sum multiple ranges
=SUM(Sheet1:Sheet3!B5)           → 3D sum across sheets
```

### SUMIF / SUMIFS

```
=SUMIF(range, criteria, [sum_range])
=SUMIFS(sum_range, criteria_range1, criteria1, [criteria_range2, criteria2, ...])
```

**Examples:**

```
=SUMIF(B2:B100, "Electronics", D2:D100)
  → Sum column D where column B = "Electronics"

=SUMIF(A2:A100, ">1000")
  → Sum values in A that are greater than 1000

=SUMIFS(E2:E100, B2:B100, "West", C2:C100, ">=2025-01-01")
  → Sum E where region is "West" AND date ≥ Jan 1 2025
```

### SUMPRODUCT

Array-aware multiplication and summation without Ctrl+Shift+Enter.

```
=SUMPRODUCT(array1, [array2], ...)
```

**Examples:**

```
=SUMPRODUCT(B2:B100, C2:C100)
  → Multiply each B×C pair, then sum all products (weighted total)

=SUMPRODUCT((A2:A100="East")*(C2:C100>50)*D2:D100)
  → Conditional sum: total D where region="East" AND quantity>50

=SUMPRODUCT((MONTH(A2:A100)=3)*B2:B100)
  → Sum B for all March entries
```

### ROUND / ROUNDUP / ROUNDDOWN

```
=ROUND(3.14159, 2)     → 3.14
=ROUNDUP(3.141, 2)     → 3.15
=ROUNDDOWN(3.149, 2)   → 3.14
=ROUND(1234, -2)       → 1200    (round to nearest hundred)
```

---

## Text Formulas

### CONCATENATE / CONCAT / TEXTJOIN

```
=CONCATENATE(A1, " ", B1)          → "John Smith" (legacy)
=CONCAT(A1, " ", B1)               → Same, modern
=A1 & " " & B1                     → Operator shorthand

=TEXTJOIN(", ", TRUE, A1:A10)
  → Join non-empty cells with comma+space: "Alpha, Beta, Gamma"
```

### LEFT / RIGHT / MID

```
=LEFT(A1, 3)       → First 3 characters
=RIGHT(A1, 4)      → Last 4 characters
=MID(A1, 5, 3)     → 3 characters starting at position 5
```

**Practical example — extract area code:**

```
=MID(A1, 2, 3)     → From "(555) 123-4567" extracts "555"
```

### TRIM / CLEAN / SUBSTITUTE

```
=TRIM(A1)                            → Remove leading/trailing/extra spaces
=CLEAN(A1)                           → Remove non-printable characters
=SUBSTITUTE(A1, "old", "new")        → Replace all occurrences
=SUBSTITUTE(A1, " ", "", 1)          → Remove only the first space
```

### TEXT (Number Formatting)

```
=TEXT(A1, "0.00")             → "1234.50"
=TEXT(A1, "$#,##0.00")        → "$1,234.50"
=TEXT(A1, "yyyy-mm-dd")       → "2025-03-15"
=TEXT(A1, "dddd, mmmm d")    → "Saturday, March 15"
=TEXT(A1, "0.0%")             → "85.3%"
```

### LEN / FIND / SEARCH

```
=LEN(A1)                     → Character count
=FIND("@", A1)               → Position of @ (case-sensitive, error if missing)
=SEARCH("word", A1)          → Position (case-insensitive, supports wildcards)
=IFERROR(FIND("x", A1), 0)   → Return 0 if not found
```

---

## Date Formulas

### TODAY / NOW

```
=TODAY()          → Current date (no time)
=NOW()            → Current date and time
=TODAY() + 30     → 30 days from today
```

### DATEDIF

Calculates the difference between two dates. Not shown in autocomplete but works.

```
=DATEDIF(start_date, end_date, unit)
```

| Unit  | Returns                          |
|-------|----------------------------------|
| "Y"   | Complete years                   |
| "M"   | Complete months                  |
| "D"   | Days                             |
| "YM"  | Months remaining after years     |
| "YD"  | Days remaining after years       |
| "MD"  | Days remaining after months      |

**Examples:**

```
=DATEDIF(A1, TODAY(), "Y")         → Years since date in A1
=DATEDIF(A1, A2, "M")             → Months between two dates
=DATEDIF(B1, B2, "Y") & " years, " & DATEDIF(B1, B2, "YM") & " months"
  → "3 years, 7 months"
```

### EDATE / EOMONTH

```
=EDATE(A1, 3)        → Date 3 months after A1
=EDATE(A1, -6)       → Date 6 months before A1
=EOMONTH(A1, 0)      → Last day of A1's month
=EOMONTH(A1, 1)      → Last day of next month
```

### DATE / YEAR / MONTH / DAY

```
=DATE(2025, 6, 15)       → June 15, 2025
=YEAR(A1)                → Extract year
=MONTH(A1)               → Extract month (1-12)
=DAY(A1)                 → Extract day (1-31)
=WEEKDAY(A1, 2)          → Day of week (Monday=1 with type 2)
```

### WORKDAY / NETWORKDAYS

```
=WORKDAY(A1, 10)                → 10 business days after A1
=WORKDAY(A1, 10, holidays)      → Excluding listed holidays
=NETWORKDAYS(A1, B1)            → Business days between two dates
```

---

## Statistical Formulas

### AVERAGE / MEDIAN

```
=AVERAGE(A1:A100)                → Arithmetic mean
=AVERAGEIF(B1:B100, ">0")       → Average of positive values only
=AVERAGEIFS(D1:D100, B1:B100, "East", C1:C100, ">100")
=MEDIAN(A1:A100)                 → Middle value
```

### STDEV / VAR

```
=STDEV(A1:A100)       → Sample standard deviation (STDEV.S)
=STDEVP(A1:A100)      → Population standard deviation (STDEV.P)
=VAR(A1:A100)         → Sample variance
```

### COUNT / COUNTA / COUNTBLANK / COUNTIF / COUNTIFS

```
=COUNT(A1:A100)                                → Count numeric cells
=COUNTA(A1:A100)                               → Count non-empty cells
=COUNTBLANK(A1:A100)                           → Count empty cells
=COUNTIF(B1:B100, "Complete")                  → Count cells matching criteria
=COUNTIF(C1:C100, ">500")                      → Count cells > 500
=COUNTIFS(B1:B100, "East", C1:C100, ">1000")   → Multiple criteria
```

### PERCENTILE / QUARTILE

```
=PERCENTILE.INC(A1:A100, 0.9)    → 90th percentile (inclusive)
=QUARTILE.INC(A1:A100, 1)        → First quartile (25th percentile)
=QUARTILE.INC(A1:A100, 3)        → Third quartile (75th percentile)
```

### MIN / MAX / LARGE / SMALL

```
=MIN(A1:A100)              → Smallest value
=MAX(A1:A100)              → Largest value
=LARGE(A1:A100, 3)         → 3rd largest value
=SMALL(A1:A100, 2)         → 2nd smallest value
```

---

## Conditional Formulas

### IF

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

### IFS (Excel 2019+)

Evaluates multiple conditions in order — first TRUE wins.

```
=IFS(A1>=90, "A", A1>=80, "B", A1>=70, "C", TRUE, "F")
  → Cleaner than nested IF; TRUE acts as default/else
```

### SWITCH

Match a value against a list of cases.

```
=SWITCH(A1,
  "N", "North",
  "S", "South",
  "E", "East",
  "W", "West",
  "Unknown"
)
```

### AND / OR / NOT / XOR

```
=AND(A1>0, B1>0)       → TRUE if both conditions met
=OR(A1="Yes", B1="Yes") → TRUE if either condition met
=NOT(A1="Error")        → Invert boolean
=XOR(A1>0, B1>0)        → TRUE if exactly one condition met
```

### IFERROR / IFNA

```
=IFERROR(A1/B1, 0)              → Return 0 instead of #DIV/0!
=IFNA(VLOOKUP(...), "Missing")  → Handle #N/A specifically
```

---

## Pivot Table Patterns

### When to Use Pivot Tables

- Summarizing large datasets by category
- Cross-tabulating two dimensions
- Calculating subtotals, averages, counts per group
- Drilling down into data hierarchies

### Common Pivot Configurations

| Goal                            | Rows         | Columns    | Values              |
|---------------------------------|--------------|------------|----------------------|
| Sales by region                 | Region       | —          | SUM of Revenue       |
| Monthly sales by product        | Product      | Month      | SUM of Revenue       |
| Average order value by customer | Customer     | —          | AVERAGE of OrderTotal|
| Count of orders by status       | Status       | —          | COUNT of OrderID     |
| Revenue % by category           | Category     | —          | SUM of Revenue (Show as % of Grand Total) |

### Calculated Fields

```
Revenue per Unit = Revenue / Quantity
Profit Margin = (Revenue - Cost) / Revenue
```

### Pivot Table Best Practices

- Source data: one row per record, no merged cells, consistent headers
- Refresh after source data changes
- Group dates by Month/Quarter/Year for time analysis
- Use Slicers for interactive filtering
- Name ranges or use structured tables as source

---

## Data Validation Rules

### Dropdown List

```
Source: "Option A,Option B,Option C"
  or
Source: =NamedRange
```

### Numeric Constraints

| Validation          | Settings                        |
|---------------------|---------------------------------|
| Whole number 1-100  | Allow: Whole number, Between, 1, 100 |
| Decimal ≥ 0         | Allow: Decimal, >=, 0           |
| Percentage 0-1      | Allow: Decimal, Between, 0, 1   |

### Date Constraints

```
Allow: Date, Between, =TODAY(), =TODAY()+365
  → Only accept dates within the next year
```

### Custom Formula Validation

```
=AND(LEN(A1)=10, LEFT(A1,3)="PRJ")
  → Must be 10 chars starting with "PRJ"

=COUNTIF($A:$A, A1)<=1
  → Prevent duplicate entries in column A
```

---

## Conditional Formatting Patterns

### Color Scales

Apply 2-color or 3-color gradient based on cell value — useful for heat maps.

### Data Bars

In-cell bar chart proportional to value — quick visual comparison.

### Icon Sets

Arrows, traffic lights, stars, flags based on value thresholds.

### Formula-Based Rules

```
=AND($D2>1000, $E2="Open")
  → Highlight row where amount > 1000 AND status = Open

=MOD(ROW(), 2)=0
  → Alternating row shading

=$B2=MAX($B$2:$B$100)
  → Highlight the row with maximum value

=TODAY()-$C2>30
  → Highlight dates older than 30 days
```

---

## Chart Types and Use Cases

| Chart Type     | Best For                                    | Data Shape                |
|----------------|---------------------------------------------|---------------------------|
| Column/Bar     | Comparing categories                        | Categories + values       |
| Line           | Trends over time                            | Time series               |
| Pie/Donut      | Parts of a whole (≤ 6 slices)               | Categories + proportions  |
| Scatter (XY)   | Correlation between two variables           | Paired numeric values     |
| Area           | Cumulative trends, stacked comparisons      | Time series, stacked      |
| Combo          | Two different scales on one chart            | Mixed series types        |
| Waterfall      | Sequential gains and losses                 | Start, changes, end       |
| Histogram      | Distribution of values                      | Single numeric column     |
| Box & Whisker  | Distribution comparison across groups       | Groups + numeric values   |
| Treemap        | Hierarchical proportions                    | Category + subcategory    |

### Chart Best Practices

- Title every chart clearly
- Label axes with units
- Limit pie charts to ≤ 6 slices; use bar chart otherwise
- Start Y-axis at 0 for bar/column charts (avoid misleading scales)
- Use consistent colors across related charts
- Remove chart junk: unnecessary gridlines, 3D effects, borders

---

## Power Query M Basics

Power Query (Get & Transform) uses the M language for data transformation.

### Common M Patterns

```m
// Load CSV
let
    Source = Csv.Document(File.Contents("C:\data\sales.csv"), [Delimiter=",", Encoding=65001]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedTypes = Table.TransformColumnTypes(PromotedHeaders, {
        {"Date", type date}, {"Amount", type number}, {"Region", type text}
    })
in
    ChangedTypes
```

### Filtering Rows

```m
Table.SelectRows(Source, each [Region] = "East" and [Amount] > 1000)
```

### Adding Calculated Columns

```m
Table.AddColumn(Source, "Profit", each [Revenue] - [Cost], type number)
Table.AddColumn(Source, "Year", each Date.Year([OrderDate]), Int64.Type)
Table.AddColumn(Source, "Quarter", each "Q" & Text.From(Date.QuarterOfYear([OrderDate])))
```

### Grouping and Aggregation

```m
Table.Group(Source, {"Region"}, {
    {"TotalRevenue", each List.Sum([Revenue]), type number},
    {"OrderCount", each Table.RowCount(_), Int64.Type},
    {"AvgOrder", each List.Average([Revenue]), type number}
})
```

### Unpivoting Columns

```m
Table.UnpivotOtherColumns(Source, {"Product", "Region"}, "Month", "Sales")
  // Convert wide format (Jan, Feb, Mar columns) to long format
```

### Merging Tables (JOIN)

```m
Table.NestedJoin(Orders, {"CustomerID"}, Customers, {"ID"}, "CustomerData", JoinKind.LeftOuter)
// Then expand: Table.ExpandTableColumn(Merged, "CustomerData", {"Name", "Email"})
```

### Practical Transform Pipeline

```m
let
    Source = Excel.Workbook(File.Contents("C:\data\raw.xlsx"), null, true),
    Sheet1 = Source{[Item="Sheet1", Kind="Sheet"]}[Data],
    Headers = Table.PromoteHeaders(Sheet1),
    Typed = Table.TransformColumnTypes(Headers, {
        {"Date", type date}, {"Revenue", type number}, {"Cost", type number}
    }),
    Cleaned = Table.SelectRows(Typed, each [Revenue] <> null and [Revenue] > 0),
    WithProfit = Table.AddColumn(Cleaned, "Profit", each [Revenue] - [Cost], type number),
    WithMargin = Table.AddColumn(WithProfit, "Margin", each [Profit] / [Revenue], type number),
    Sorted = Table.Sort(WithMargin, {{"Date", Order.Ascending}})
in
    Sorted
```
