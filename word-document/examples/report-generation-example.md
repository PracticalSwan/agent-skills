# Professional Word Report Generation Example

Complete example of generating a multi-section business report using the `docx` npm package.

## Output Structure

```
1. Title Page — company logo, report title, subtitle, date, author
2. Table of Contents — auto-generated from headings
3. Executive Summary — narrative overview
4. Key Metrics Table — formatted data table with alternating row colors
5. Quarterly Breakdown — detail section with sub-tables
6. Chart Placeholder — described image placeholder
7. Appendix — supplementary data, methodology notes
```

---

## Style Configuration

Reusable style object for consistent branding across reports.

```javascript
const REPORT_STYLES = {
  colors: {
    primary: "1F4E79",      // dark blue
    primaryLight: "D6E4F0",  // light blue background
    accent: "2E75B6",        // medium blue
    text: "333333",
    textLight: "666666",
    headerBg: "1F4E79",
    headerText: "FFFFFF",
    altRowBg: "F2F7FB",
    borderColor: "B4C6E0",
    success: "28A745",
    warning: "FFC107",
    danger: "DC3545",
  },
  fonts: {
    heading: "Calibri Light",
    body: "Calibri",
    monospace: "Consolas",
  },
  sizes: {
    title: 52,           // 26pt
    subtitle: 28,        // 14pt
    heading1: 32,        // 16pt
    heading2: 26,        // 13pt
    heading3: 22,        // 11pt
    body: 22,            // 11pt
    small: 18,           // 9pt
    caption: 16,         // 8pt
  },
  spacing: {
    afterHeading1: 240,  // 12pt
    afterHeading2: 160,
    afterParagraph: 120, // 6pt
    lineSpacing: 276,    // 1.15x
  },
  page: {
    marginTop: 1440,     // 1 inch in twips
    marginBottom: 1440,
    marginLeft: 1440,
    marginRight: 1440,
    headerMargin: 720,
    footerMargin: 720,
  },
};
```

---

## Complete Report Code

```javascript
import fs from "fs";
import {
  Document, Packer, Paragraph, TextRun, ImageRun,
  Header, Footer, PageNumber, NumberFormat,
  Table, TableRow, TableCell,
  AlignmentType, HeadingLevel, TabStopType,
  BorderStyle, ShadingType, WidthType, VerticalAlign,
  TableOfContents, PageOrientation, SectionType,
  convertInchesToTwip, LevelFormat,
} from "docx";

const S = REPORT_STYLES; // alias for brevity

// ─── Helper: Create a styled paragraph ──────────────────────────────

function styledParagraph(text, options = {}) {
  return new Paragraph({
    spacing: { after: S.spacing.afterParagraph, line: S.spacing.lineSpacing },
    ...options,
    children: [
      new TextRun({
        text,
        font: S.fonts.body,
        size: S.sizes.body,
        color: S.colors.text,
        ...(options.run || {}),
      }),
    ],
  });
}

// ─── Helper: Create a table cell ────────────────────────────────────

function cell(text, options = {}) {
  const isHeader = options.header || false;
  return new TableCell({
    width: options.width || { size: 0, type: WidthType.AUTO },
    shading: options.shading || (isHeader
      ? { fill: S.colors.headerBg, type: ShadingType.SOLID, color: "auto" }
      : undefined),
    verticalAlign: VerticalAlign.CENTER,
    margins: {
      top: 40, bottom: 40, left: 80, right: 80,
    },
    children: [
      new Paragraph({
        alignment: options.alignment || (isHeader ? AlignmentType.CENTER : AlignmentType.LEFT),
        children: [
          new TextRun({
            text: String(text),
            bold: isHeader,
            font: S.fonts.body,
            size: isHeader ? S.sizes.body : S.sizes.body,
            color: isHeader ? S.colors.headerText : S.colors.text,
          }),
        ],
      }),
    ],
  });
}

// ─── Helper: Data table with alternating rows ───────────────────────

function dataTable(headers, rows, columnWidths) {
  const headerRow = new TableRow({
    tableHeader: true,
    children: headers.map((h, i) =>
      cell(h, {
        header: true,
        width: columnWidths?.[i] ? { size: columnWidths[i], type: WidthType.DXA } : undefined,
        alignment: AlignmentType.CENTER,
      })
    ),
  });

  const dataRows = rows.map((row, rowIdx) =>
    new TableRow({
      children: row.map((value, colIdx) =>
        cell(value, {
          width: columnWidths?.[colIdx] ? { size: columnWidths[colIdx], type: WidthType.DXA } : undefined,
          shading: rowIdx % 2 === 1
            ? { fill: S.colors.altRowBg, type: ShadingType.SOLID, color: "auto" }
            : undefined,
          alignment: typeof value === "number" ? AlignmentType.RIGHT : AlignmentType.LEFT,
        })
      ),
    })
  );

  return new Table({
    rows: [headerRow, ...dataRows],
    width: { size: 100, type: WidthType.PERCENTAGE },
  });
}

// ─── Helper: Section divider ────────────────────────────────────────

function sectionDivider() {
  return new Paragraph({
    spacing: { before: 200, after: 200 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 1, color: S.colors.borderColor, space: 8 } },
    children: [],
  });
}

// ─── Section 1: Title Page ──────────────────────────────────────────

function buildTitlePage() {
  // For a real logo, replace with: fs.readFileSync("logo.png")
  const logoPlaceholder = styledParagraph("[Company Logo]", {
    alignment: AlignmentType.CENTER,
    spacing: { before: 2400, after: 600 },
    run: { size: S.sizes.subtitle, color: S.colors.textLight, italics: true },
  });

  return [
    logoPlaceholder,
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 200 },
      children: [
        new TextRun({
          text: "Annual Performance Report",
          font: S.fonts.heading,
          size: S.sizes.title,
          bold: true,
          color: S.colors.primary,
        }),
      ],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 400 },
      children: [
        new TextRun({
          text: "Fiscal Year 2025 — Q1 through Q4",
          font: S.fonts.heading,
          size: S.sizes.subtitle,
          color: S.colors.accent,
        }),
      ],
    }),
    sectionDivider(),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 120 },
      children: [
        new TextRun({
          text: "Prepared by: Analytics Department",
          font: S.fonts.body,
          size: S.sizes.body,
          color: S.colors.textLight,
        }),
      ],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 120 },
      children: [
        new TextRun({
          text: `Date: ${new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" })}`,
          font: S.fonts.body,
          size: S.sizes.body,
          color: S.colors.textLight,
        }),
      ],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [
        new TextRun({
          text: "CONFIDENTIAL",
          font: S.fonts.body,
          size: S.sizes.small,
          bold: true,
          color: S.colors.danger,
        }),
      ],
    }),
  ];
}

// ─── Section 2: Table of Contents ───────────────────────────────────

function buildTableOfContents() {
  return [
    new Paragraph({
      text: "Table of Contents",
      heading: HeadingLevel.HEADING_1,
      spacing: { after: 300 },
    }),
    new TableOfContents("Table of Contents", {
      hyperlink: true,
      headingStyleRange: "1-3",
    }),
  ];
}

// ─── Section 3: Executive Summary ───────────────────────────────────

function buildExecutiveSummary() {
  return [
    new Paragraph({
      text: "Executive Summary",
      heading: HeadingLevel.HEADING_1,
    }),
    styledParagraph(
      "This report presents a comprehensive analysis of organizational performance across all four quarters of Fiscal Year 2025. Key findings indicate strong growth in digital channels, improved operational efficiency, and expanding market share in the Asia-Pacific region."
    ),
    styledParagraph(
      "Total revenue reached $48.2M, representing a 12.4% year-over-year increase. Operating margins improved by 2.1 percentage points to 23.7%, driven by process automation initiatives and strategic vendor consolidation."
    ),
    new Paragraph({
      text: "Key Highlights",
      heading: HeadingLevel.HEADING_2,
    }),
    styledParagraph("Revenue grew 12.4% YoY to $48.2M, exceeding the $45M target.", {
      numbering: { reference: "report-bullets", level: 0 },
    }),
    styledParagraph("Customer acquisition cost decreased by 18% through optimized digital campaigns.", {
      numbering: { reference: "report-bullets", level: 0 },
    }),
    styledParagraph("Employee satisfaction score improved to 4.3/5.0 (up from 3.9).", {
      numbering: { reference: "report-bullets", level: 0 },
    }),
    styledParagraph("Three new enterprise clients onboarded, adding $6.1M in annual recurring revenue.", {
      numbering: { reference: "report-bullets", level: 0 },
    }),
  ];
}

// ─── Section 4: Key Metrics ─────────────────────────────────────────

function buildMetricsSection() {
  const metricsHeaders = ["Metric", "Q1", "Q2", "Q3", "Q4", "YoY Change"];
  const metricsData = [
    ["Revenue ($M)",        "10.8",  "11.5",  "12.1",  "13.8",  "+12.4%"],
    ["Operating Margin",    "22.1%", "23.0%", "24.2%", "25.5%", "+2.1pp"],
    ["Customer Count",      "1,240", "1,385", "1,510", "1,678", "+35.3%"],
    ["NPS Score",           "62",    "65",    "68",    "71",    "+9pts"],
    ["Employee Headcount",  "342",   "358",   "371",   "389",   "+13.7%"],
    ["Churn Rate",          "3.2%",  "2.8%",  "2.5%",  "2.1%",  "-1.1pp"],
  ];

  return [
    new Paragraph({
      text: "Key Performance Metrics",
      heading: HeadingLevel.HEADING_1,
    }),
    styledParagraph(
      "The following table summarizes core business metrics tracked across all quarters."
    ),
    dataTable(metricsHeaders, metricsData, [2800, 1400, 1400, 1400, 1400, 1600]),
    new Paragraph({ spacing: { after: 200 }, children: [] }),
  ];
}

// ─── Section 5: Quarterly Breakdown ─────────────────────────────────

function buildQuarterlyBreakdown() {
  const regionHeaders = ["Region", "Revenue ($M)", "Growth", "Margin"];
  const regionData = [
    ["North America", "22.4", "+8.2%",  "26.1%"],
    ["Europe",        "12.8", "+11.5%", "22.3%"],
    ["Asia-Pacific",  "9.6",  "+24.1%", "19.8%"],
    ["Latin America", "3.4",  "+15.7%", "18.2%"],
  ];

  return [
    new Paragraph({
      text: "Quarterly Breakdown",
      heading: HeadingLevel.HEADING_1,
    }),
    new Paragraph({
      text: "Revenue by Region",
      heading: HeadingLevel.HEADING_2,
    }),
    styledParagraph(
      "Regional performance showed strong gains across all territories, with Asia-Pacific leading growth at 24.1%."
    ),
    dataTable(regionHeaders, regionData, [2800, 2200, 1800, 1800]),
    new Paragraph({ spacing: { after: 300 }, children: [] }),
    new Paragraph({
      text: "Product Line Performance",
      heading: HeadingLevel.HEADING_2,
    }),
    styledParagraph(
      "The SaaS platform remains the primary revenue driver at 62% of total revenue, while professional services grew 19% driven by implementation engagements with new enterprise clients."
    ),
  ];
}

// ─── Section 6: Chart Placeholder ───────────────────────────────────

function buildChartPlaceholder() {
  return [
    new Paragraph({
      text: "Visual Analytics",
      heading: HeadingLevel.HEADING_1,
    }),
    styledParagraph(
      "The following charts illustrate revenue trends and regional distribution."
    ),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 400, after: 200 },
      border: {
        top:    { style: BorderStyle.DASHED, size: 1, color: S.colors.borderColor },
        bottom: { style: BorderStyle.DASHED, size: 1, color: S.colors.borderColor },
        left:   { style: BorderStyle.DASHED, size: 1, color: S.colors.borderColor },
        right:  { style: BorderStyle.DASHED, size: 1, color: S.colors.borderColor },
      },
      children: [
        new TextRun({
          text: "[Chart Placeholder: Revenue Trend — Line chart showing Q1–Q4 revenue growth]",
          font: S.fonts.body,
          size: S.sizes.body,
          color: S.colors.textLight,
          italics: true,
        }),
      ],
    }),
    new Paragraph({ spacing: { after: 200 }, children: [] }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 200, after: 400 },
      border: {
        top:    { style: BorderStyle.DASHED, size: 1, color: S.colors.borderColor },
        bottom: { style: BorderStyle.DASHED, size: 1, color: S.colors.borderColor },
        left:   { style: BorderStyle.DASHED, size: 1, color: S.colors.borderColor },
        right:  { style: BorderStyle.DASHED, size: 1, color: S.colors.borderColor },
      },
      children: [
        new TextRun({
          text: "[Chart Placeholder: Regional Distribution — Pie chart of revenue by region]",
          font: S.fonts.body,
          size: S.sizes.body,
          color: S.colors.textLight,
          italics: true,
        }),
      ],
    }),
    styledParagraph(
      "Note: Replace chart placeholders with actual chart images using ImageRun. Generate charts externally (e.g., Chart.js rendered to PNG via canvas) and embed with the ImageRun API.",
      { run: { size: S.sizes.small, italics: true, color: S.colors.textLight } }
    ),
  ];
}

// ─── Section 7: Appendix ────────────────────────────────────────────

function buildAppendix() {
  return [
    new Paragraph({
      text: "Appendix",
      heading: HeadingLevel.HEADING_1,
    }),
    new Paragraph({
      text: "A. Methodology",
      heading: HeadingLevel.HEADING_2,
    }),
    styledParagraph(
      "Financial data was sourced from the ERP system (SAP S/4HANA) and reconciled against audited quarterly filings. Customer metrics were extracted from the CRM (Salesforce) with a data freshness cutoff of December 31, 2025."
    ),
    styledParagraph(
      "Year-over-year calculations compare FY2025 figures against FY2024 actuals. Operating margin is calculated as (Revenue - COGS - OpEx) / Revenue."
    ),
    new Paragraph({
      text: "B. Definitions",
      heading: HeadingLevel.HEADING_2,
    }),
    styledParagraph("NPS (Net Promoter Score): Percentage of promoters minus detractors on a 0-10 scale.", {
      numbering: { reference: "report-bullets", level: 0 },
    }),
    styledParagraph("ARR (Annual Recurring Revenue): Annualized value of active subscription contracts.", {
      numbering: { reference: "report-bullets", level: 0 },
    }),
    styledParagraph("Churn Rate: Percentage of customers who cancelled in a given quarter.", {
      numbering: { reference: "report-bullets", level: 0 },
    }),
    new Paragraph({
      text: "C. Data Sources",
      heading: HeadingLevel.HEADING_2,
    }),
    styledParagraph("SAP S/4HANA — Financial transactions and GL data", {
      numbering: { reference: "report-bullets", level: 0 },
    }),
    styledParagraph("Salesforce CRM — Customer records, pipeline, and activity logs", {
      numbering: { reference: "report-bullets", level: 0 },
    }),
    styledParagraph("Workday HCM — Employee headcount and satisfaction surveys", {
      numbering: { reference: "report-bullets", level: 0 },
    }),
    styledParagraph("Google Analytics — Web traffic and conversion metrics", {
      numbering: { reference: "report-bullets", level: 0 },
    }),
  ];
}

// ─── Header and Footer ─────────────────────────────────────────────

function buildHeader() {
  return new Header({
    children: [
      new Paragraph({
        children: [
          new TextRun({
            text: "Acme Corp",
            font: S.fonts.heading,
            size: S.sizes.small,
            bold: true,
            color: S.colors.primary,
          }),
          new TextRun({ text: "\t" }),
          new TextRun({
            text: "Annual Performance Report — FY2025",
            font: S.fonts.body,
            size: S.sizes.caption,
            color: S.colors.textLight,
          }),
        ],
        tabStops: [{ type: TabStopType.RIGHT, position: 9026 }],
        border: {
          bottom: { style: BorderStyle.SINGLE, size: 1, color: S.colors.borderColor, space: 4 },
        },
      }),
    ],
  });
}

function buildFooter() {
  return new Footer({
    children: [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        border: {
          top: { style: BorderStyle.SINGLE, size: 1, color: S.colors.borderColor, space: 4 },
        },
        children: [
          new TextRun({
            text: "CONFIDENTIAL  |  ",
            font: S.fonts.body,
            size: S.sizes.caption,
            color: S.colors.textLight,
          }),
          new TextRun({
            text: "Page ",
            font: S.fonts.body,
            size: S.sizes.caption,
            color: S.colors.textLight,
          }),
          new TextRun({
            children: [PageNumber.CURRENT],
            font: S.fonts.body,
            size: S.sizes.caption,
            color: S.colors.text,
          }),
          new TextRun({
            text: " of ",
            font: S.fonts.body,
            size: S.sizes.caption,
            color: S.colors.textLight,
          }),
          new TextRun({
            children: [PageNumber.TOTAL_PAGES],
            font: S.fonts.body,
            size: S.sizes.caption,
            color: S.colors.text,
          }),
        ],
      }),
    ],
  });
}

// ─── Assemble Document ──────────────────────────────────────────────

const doc = new Document({
  creator: "Analytics Department",
  title: "Annual Performance Report — FY2025",
  description: "Comprehensive fiscal year performance analysis",
  features: { updateFields: true },
  numbering: {
    config: [
      {
        reference: "report-bullets",
        levels: [
          {
            level: 0,
            format: LevelFormat.BULLET,
            text: "\u2022",
            alignment: AlignmentType.START,
            style: {
              paragraph: { indent: { left: 720, hanging: 360 } },
            },
          },
          {
            level: 1,
            format: LevelFormat.BULLET,
            text: "\u25E6",
            alignment: AlignmentType.START,
            style: {
              paragraph: { indent: { left: 1440, hanging: 360 } },
            },
          },
        ],
      },
    ],
  },
  styles: {
    default: {
      document: {
        run: {
          font: S.fonts.body,
          size: S.sizes.body,
          color: S.colors.text,
        },
        paragraph: {
          spacing: { after: S.spacing.afterParagraph, line: S.spacing.lineSpacing },
        },
      },
      heading1: {
        run: {
          font: S.fonts.heading,
          size: S.sizes.heading1,
          bold: true,
          color: S.colors.primary,
        },
        paragraph: {
          spacing: { before: 360, after: S.spacing.afterHeading1 },
        },
      },
      heading2: {
        run: {
          font: S.fonts.heading,
          size: S.sizes.heading2,
          bold: true,
          color: S.colors.accent,
        },
        paragraph: {
          spacing: { before: 240, after: S.spacing.afterHeading2 },
        },
      },
      heading3: {
        run: {
          font: S.fonts.heading,
          size: S.sizes.heading3,
          bold: true,
          color: S.colors.text,
        },
        paragraph: {
          spacing: { before: 160, after: 80 },
        },
      },
    },
  },
  sections: [
    // Title Page (no header/footer)
    {
      properties: {
        page: {
          margin: {
            top: S.page.marginTop,
            bottom: S.page.marginBottom,
            left: S.page.marginLeft,
            right: S.page.marginRight,
          },
        },
        titlePage: true,
      },
      children: buildTitlePage(),
    },
    // Table of Contents
    {
      properties: {
        type: SectionType.NEXT_PAGE,
        page: {
          margin: {
            top: S.page.marginTop,
            bottom: S.page.marginBottom,
            left: S.page.marginLeft,
            right: S.page.marginRight,
          },
          pageNumbers: { start: 1, formatType: NumberFormat.LOWER_ROMAN },
        },
      },
      headers: { default: buildHeader() },
      footers: { default: buildFooter() },
      children: buildTableOfContents(),
    },
    // Main Content
    {
      properties: {
        type: SectionType.NEXT_PAGE,
        page: {
          margin: {
            top: S.page.marginTop,
            bottom: S.page.marginBottom,
            left: S.page.marginLeft,
            right: S.page.marginRight,
          },
          pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL },
        },
      },
      headers: { default: buildHeader() },
      footers: { default: buildFooter() },
      children: [
        ...buildExecutiveSummary(),
        ...buildMetricsSection(),
        ...buildQuarterlyBreakdown(),
        ...buildChartPlaceholder(),
        ...buildAppendix(),
      ],
    },
  ],
});

// ─── Export ──────────────────────────────────────────────────────────

async function generateReport(outputPath = "annual-report-fy2025.docx") {
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);
  console.log(`Report generated: ${outputPath}`);
}

generateReport();
```

---

## How to Use

### Install

```bash
npm install docx
```

### Run

```bash
node generate-report.mjs
```

### Customization Points

| What to Change                | Where                                        |
|-------------------------------|----------------------------------------------|
| Company branding colors       | `REPORT_STYLES.colors`                       |
| Fonts                         | `REPORT_STYLES.fonts`                        |
| Page margins                  | `REPORT_STYLES.page`                         |
| Report data                   | `metricsData`, `regionData` arrays           |
| Add a real logo               | Replace `logoPlaceholder` with `ImageRun`    |
| Add real charts               | Render to PNG externally, embed via `ImageRun`|
| Change paper size             | Section `properties.page.size`               |

### Adding a Real Logo

```javascript
const logoBuffer = fs.readFileSync("assets/company-logo.png");

const logo = new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 1200, after: 600 },
  children: [
    new ImageRun({
      data: logoBuffer,
      transformation: { width: 200, height: 60 },
      type: "png",
    }),
  ],
});
```

### Adding a Chart Image

```javascript
// Pre-render your chart to PNG using Chart.js + node-canvas, or any charting library
const chartBuffer = fs.readFileSync("charts/revenue-trend.png");

const chartImage = new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [
    new ImageRun({
      data: chartBuffer,
      transformation: { width: 560, height: 320 },
      type: "png",
    }),
  ],
});
```

---

## Architecture Notes

- **Section-per-purpose**: Title page, TOC, and main content are separate sections so each can have independent headers/footers and page numbering schemes.
- **Helper functions**: `cell()`, `dataTable()`, and `styledParagraph()` reduce boilerplate and enforce consistent styling.
- **Style configuration object**: Centralizes all colors, fonts, and sizes for easy rebranding.
- **`updateFields: true`**: Prompts the user to update the Table of Contents when they first open the document.
- **Alternating row colors**: Applied via the `rowIdx % 2` check in `dataTable()` for readability.
