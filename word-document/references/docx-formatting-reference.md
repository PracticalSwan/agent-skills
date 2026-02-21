# Word Document Formatting Reference (docx-js)

Comprehensive reference for programmatic Word document creation using the `docx` npm package.

## Document Structure

### Creating a Document

```javascript
import {
  Document, Packer, Paragraph, TextRun, Header, Footer,
  PageNumber, NumberFormat, Table, TableRow, TableCell,
  ImageRun, AlignmentType, HeadingLevel, TabStopType,
  BorderStyle, ShadingType, WidthType, TableOfContents,
  StyleLevel, PageOrientation, convertInchesToTwip,
  LevelFormat, UnderlineType, SectionType
} from "docx";

const doc = new Document({
  creator: "Author Name",
  title: "Document Title",
  description: "Document description",
  sections: [
    {
      properties: { /* section properties */ },
      headers: { default: new Header({ children: [] }) },
      footers: { default: new Footer({ children: [] }) },
      children: [ /* paragraphs, tables, etc. */ ],
    },
  ],
});
```

### Sections

Each section can have its own page setup, headers, and footers.

```javascript
const doc = new Document({
  sections: [
    {
      properties: {
        type: SectionType.NEXT_PAGE, // CONTINUOUS, EVEN_PAGE, ODD_PAGE
        page: {
          size: { width: 12240, height: 15840 }, // Letter size in twips
          margin: {
            top: convertInchesToTwip(1),
            bottom: convertInchesToTwip(1),
            left: convertInchesToTwip(1.25),
            right: convertInchesToTwip(1.25),
          },
        },
      },
      children: [new Paragraph("Section 1 content")],
    },
    {
      properties: {
        type: SectionType.NEXT_PAGE,
        page: {
          size: { orientation: PageOrientation.LANDSCAPE },
        },
      },
      children: [new Paragraph("Section 2 — landscape")],
    },
  ],
});
```

### Headers and Footers

Three slots per section: `default`, `first`, `even`.

```javascript
const header = new Header({
  children: [
    new Paragraph({
      children: [
        new TextRun({ text: "Company Name", bold: true, size: 18 }),
        new TextRun({ text: "\t" }),
        new TextRun({ text: "Confidential", italics: true, color: "888888" }),
      ],
      tabStops: [{ type: TabStopType.RIGHT, position: 9026 }],
    }),
  ],
});

const footer = new Footer({
  children: [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [
        new TextRun("Page "),
        new TextRun({ children: [PageNumber.CURRENT] }),
        new TextRun(" of "),
        new TextRun({ children: [PageNumber.TOTAL_PAGES] }),
      ],
    }),
  ],
});

// Attach to section
{
  properties: {
    page: {
      pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL },
    },
  },
  headers: { default: header, first: firstPageHeader },
  footers: { default: footer },
  children: [],
}
```

---

## Paragraph Formatting

### Alignment

```javascript
new Paragraph({
  text: "Centered text",
  alignment: AlignmentType.CENTER,
  // LEFT, RIGHT, JUSTIFIED, DISTRIBUTE, BOTH
});
```

### Spacing

All spacing values in half-points (1/20 of a point). Use `convertInchesToTwip` for inches.

```javascript
new Paragraph({
  text: "Spaced paragraph",
  spacing: {
    before: 240,  // 12pt before
    after: 120,   // 6pt after
    line: 276,    // 1.15x line spacing (240 = single, 480 = double)
    lineRule: "auto", // "auto", "exact", "atLeast"
  },
});
```

### Indentation

```javascript
new Paragraph({
  text: "Indented paragraph",
  indent: {
    left: convertInchesToTwip(0.5),
    right: convertInchesToTwip(0.25),
    firstLine: convertInchesToTwip(0.5),  // first-line indent
    // hanging: convertInchesToTwip(0.5), // hanging indent (mutually exclusive with firstLine)
  },
});
```

### Tab Stops

```javascript
new Paragraph({
  children: [
    new TextRun("Left\tCenter\tRight"),
  ],
  tabStops: [
    { type: TabStopType.CENTER, position: 4513 },
    { type: TabStopType.RIGHT, position: 9026 },
    // TabStopType: LEFT, CENTER, RIGHT, DECIMAL, BAR
  ],
});
```

---

## Character Formatting

### TextRun Options

```javascript
new TextRun({
  text: "Formatted text",
  bold: true,
  italics: true,
  underline: { type: UnderlineType.SINGLE, color: "000000" },
  // UnderlineType: SINGLE, DOUBLE, DOTTED, DASH, WAVE, THICK, NONE
  strike: false,
  doubleStrike: false,
  subScript: false,
  superScript: false,
  allCaps: false,
  smallCaps: false,

  font: "Calibri",
  size: 24,          // half-points → 24 = 12pt
  color: "2E74B5",   // hex without #

  highlight: "yellow",
  // yellow, green, cyan, magenta, blue, red, darkBlue, darkCyan,
  // darkGreen, darkMagenta, darkRed, darkYellow, darkGray, lightGray, black

  shading: {
    type: ShadingType.SOLID,
    color: "FFFF00",
    fill: "FFFF00",
  },

  characterSpacing: 20, // 1/20 of a point
});
```

### Font Embedding Considerations

docx-js references fonts by name. The rendering application must have the font installed. Stick to widely available fonts: Calibri, Arial, Times New Roman, Courier New, Segoe UI.

### Hyperlinks

```javascript
import { ExternalHyperlink } from "docx";

new Paragraph({
  children: [
    new ExternalHyperlink({
      children: [
        new TextRun({
          text: "Visit our website",
          style: "Hyperlink", // built-in hyperlink style
        }),
      ],
      link: "https://example.com",
    }),
  ],
});
```

---

## Headings

```javascript
new Paragraph({
  text: "Chapter Title",
  heading: HeadingLevel.HEADING_1,
  // HEADING_1 through HEADING_6, TITLE
});
```

---

## Numbered and Bulleted Lists

### Define Numbering

```javascript
const doc = new Document({
  numbering: {
    config: [
      {
        reference: "my-numbering",
        levels: [
          {
            level: 0,
            format: LevelFormat.DECIMAL,     // 1, 2, 3
            text: "%1.",
            alignment: AlignmentType.START,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } },
          },
          {
            level: 1,
            format: LevelFormat.LOWER_LETTER, // a, b, c
            text: "%2)",
            alignment: AlignmentType.START,
            style: { paragraph: { indent: { left: 1440, hanging: 360 } } },
          },
        ],
      },
      {
        reference: "my-bullets",
        levels: [
          {
            level: 0,
            format: LevelFormat.BULLET,
            text: "\u2022",                  // bullet character
            alignment: AlignmentType.START,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } },
          },
          {
            level: 1,
            format: LevelFormat.BULLET,
            text: "\u25E6",                  // white bullet
            alignment: AlignmentType.START,
            style: { paragraph: { indent: { left: 1440, hanging: 360 } } },
          },
        ],
      },
    ],
  },
  sections: [{ children: [] }],
});
```

### Use in Paragraphs

```javascript
// Numbered list items
new Paragraph({
  text: "First item",
  numbering: { reference: "my-numbering", level: 0 },
});
new Paragraph({
  text: "Sub-item",
  numbering: { reference: "my-numbering", level: 1 },
});

// Bulleted list items
new Paragraph({
  text: "Bullet point",
  numbering: { reference: "my-bullets", level: 0 },
});
```

---

## Table Formatting

### Basic Table

```javascript
const table = new Table({
  rows: [
    new TableRow({
      tableHeader: true, // mark as header row (repeats on page break)
      children: [
        new TableCell({
          children: [new Paragraph({ text: "Header 1", bold: true })],
          shading: { fill: "2E74B5", type: ShadingType.SOLID, color: "auto" },
          width: { size: 3000, type: WidthType.DXA },
        }),
        new TableCell({
          children: [new Paragraph({ text: "Header 2", bold: true })],
          shading: { fill: "2E74B5", type: ShadingType.SOLID, color: "auto" },
          width: { size: 3000, type: WidthType.DXA },
        }),
      ],
    }),
    new TableRow({
      children: [
        new TableCell({ children: [new Paragraph("Row 1, Col 1")] }),
        new TableCell({ children: [new Paragraph("Row 1, Col 2")] }),
      ],
    }),
  ],
  width: { size: 100, type: WidthType.PERCENTAGE },
});
```

### Cell Borders

```javascript
new TableCell({
  children: [new Paragraph("Bordered cell")],
  borders: {
    top: { style: BorderStyle.SINGLE, size: 1, color: "000000" },
    bottom: { style: BorderStyle.SINGLE, size: 1, color: "000000" },
    left: { style: BorderStyle.SINGLE, size: 1, color: "000000" },
    right: { style: BorderStyle.SINGLE, size: 1, color: "000000" },
    // BorderStyle: SINGLE, DOUBLE, DOTTED, DASHED, THICK, NONE, NIL
  },
});
```

### Cell Shading

```javascript
new TableCell({
  children: [new Paragraph("Shaded cell")],
  shading: {
    fill: "D9E2F3",
    type: ShadingType.SOLID,
    color: "auto",
  },
});
```

### Column Widths

```javascript
// Fixed widths (DXA = 1/20 of a point)
{ width: { size: 2400, type: WidthType.DXA } }

// Percentage widths
{ width: { size: 50, type: WidthType.PERCENTAGE } }

// Auto width
{ width: { size: 0, type: WidthType.AUTO } }
```

### Merged Cells

```javascript
// Horizontal merge
new TableRow({
  children: [
    new TableCell({
      children: [new Paragraph("Merged across 3 columns")],
      columnSpan: 3,
    }),
  ],
});

// Vertical merge
new TableCell({
  children: [new Paragraph("Span start")],
  rowSpan: 2, // spans this row + next row
});
```

### Cell Vertical Alignment and Margins

```javascript
import { VerticalAlign } from "docx";

new TableCell({
  children: [new Paragraph("Centered vertically")],
  verticalAlign: VerticalAlign.CENTER, // TOP, CENTER, BOTTOM
  margins: {
    top: convertInchesToTwip(0.05),
    bottom: convertInchesToTwip(0.05),
    left: convertInchesToTwip(0.1),
    right: convertInchesToTwip(0.1),
  },
});
```

---

## Image Handling

### Inline Image

```javascript
import fs from "fs";

const imageBuffer = fs.readFileSync("logo.png");

new Paragraph({
  children: [
    new ImageRun({
      data: imageBuffer,
      transformation: {
        width: 200,  // pixels
        height: 100,
      },
      type: "png", // "png", "jpg", "gif", "bmp"
    }),
  ],
});
```

### Floating Image

```javascript
import { HorizontalPositionAlign, VerticalPositionAlign } from "docx";

new Paragraph({
  children: [
    new ImageRun({
      data: imageBuffer,
      transformation: { width: 150, height: 150 },
      floating: {
        horizontalPosition: {
          align: HorizontalPositionAlign.RIGHT,
        },
        verticalPosition: {
          align: VerticalPositionAlign.TOP,
        },
        wrap: {
          type: "square",   // "square", "tight", "topAndBottom", "none"
          side: "bothSides", // "bothSides", "left", "right", "largest"
        },
        margins: {
          top: convertInchesToTwip(0.1),
          bottom: convertInchesToTwip(0.1),
          left: convertInchesToTwip(0.1),
          right: convertInchesToTwip(0.1),
        },
      },
    }),
  ],
});
```

---

## Styles and Style Inheritance

### Custom Styles

```javascript
const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Calibri", size: 22, color: "333333" },
        paragraph: { spacing: { after: 120, line: 276 } },
      },
      heading1: {
        run: { font: "Calibri Light", size: 32, bold: true, color: "2E74B5" },
        paragraph: { spacing: { before: 360, after: 120 } },
      },
      heading2: {
        run: { font: "Calibri Light", size: 26, bold: true, color: "2E74B5" },
        paragraph: { spacing: { before: 240, after: 80 } },
      },
    },
    paragraphStyles: [
      {
        id: "customQuote",
        name: "Custom Quote",
        basedOn: "Normal",
        next: "Normal",
        run: { italics: true, color: "666666" },
        paragraph: {
          indent: { left: convertInchesToTwip(0.5) },
          spacing: { before: 120, after: 120 },
        },
      },
    ],
    characterStyles: [
      {
        id: "codeInline",
        name: "Inline Code",
        run: { font: "Courier New", size: 20, color: "C7254E" },
      },
    ],
  },
  sections: [{ children: [] }],
});

// Using custom paragraph style
new Paragraph({ text: "A quotation", style: "customQuote" });

// Using custom character style
new TextRun({ text: "codeSnippet", style: "codeInline" });
```

---

## Page Setup

### Margins and Orientation

```javascript
{
  properties: {
    page: {
      size: {
        width: 12240,    // 8.5" in twips
        height: 15840,   // 11" in twips
        orientation: PageOrientation.PORTRAIT,
        // PORTRAIT, LANDSCAPE
      },
      margin: {
        top: convertInchesToTwip(1),
        bottom: convertInchesToTwip(1),
        left: convertInchesToTwip(1),
        right: convertInchesToTwip(1),
        header: convertInchesToTwip(0.5),
        footer: convertInchesToTwip(0.5),
        gutter: 0,
      },
    },
  },
}
```

### Common Paper Sizes (in twips)

| Paper   | Width  | Height |
|---------|--------|--------|
| Letter  | 12240  | 15840  |
| A4      | 11906  | 16838  |
| Legal   | 12240  | 20160  |
| A3      | 16838  | 23811  |

### Page Borders

```javascript
{
  properties: {
    page: {
      borders: {
        pageBorderTop: { style: BorderStyle.SINGLE, size: 3, color: "000000", space: 24 },
        pageBorderBottom: { style: BorderStyle.SINGLE, size: 3, color: "000000", space: 24 },
        pageBorderLeft: { style: BorderStyle.SINGLE, size: 3, color: "000000", space: 24 },
        pageBorderRight: { style: BorderStyle.SINGLE, size: 3, color: "000000", space: 24 },
      },
    },
  },
}
```

---

## Table of Contents

```javascript
const doc = new Document({
  features: { updateFields: true }, // prompt user to update fields on open
  sections: [
    {
      children: [
        new TableOfContents("Table of Contents", {
          hyperlink: true,
          headingStyleRange: "1-3", // include Heading 1–3
          stylesWithLevels: [
            new StyleLevel("customHeading", 1),
          ],
        }),
        new Paragraph({
          text: "",
          pageBreakBefore: true,
        }),
        new Paragraph({
          text: "Introduction",
          heading: HeadingLevel.HEADING_1,
        }),
        new Paragraph("Content under Introduction..."),
      ],
    },
  ],
});
```

---

## Exporting the Document

### To File (Node.js)

```javascript
import { Packer } from "docx";
import fs from "fs";

const buffer = await Packer.toBuffer(doc);
fs.writeFileSync("output.docx", buffer);
```

### To Blob (Browser)

```javascript
const blob = await Packer.toBlob(doc);
const url = URL.createObjectURL(blob);
// Trigger download
const a = document.createElement("a");
a.href = url;
a.download = "output.docx";
a.click();
```

### To Base64

```javascript
const base64 = await Packer.toBase64String(doc);
```

---

## Quick Reference: Import Checklist

```javascript
import {
  Document, Packer, Paragraph, TextRun, ImageRun,
  Header, Footer, PageNumber, NumberFormat,
  Table, TableRow, TableCell,
  AlignmentType, HeadingLevel, TabStopType,
  BorderStyle, ShadingType, WidthType, VerticalAlign,
  ExternalHyperlink, TableOfContents, StyleLevel,
  PageOrientation, SectionType, LevelFormat,
  UnderlineType, HorizontalPositionAlign, VerticalPositionAlign,
  convertInchesToTwip,
} from "docx";
```
