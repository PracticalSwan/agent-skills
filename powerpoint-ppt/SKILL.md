---
name: powerpoint-ppt
description: PowerPoint (.pptx) manipulation via MCP server. Use for creating slides, formatting presentations, managing placeholders, adding images, applying templates, or extracting text from .pptx files.
license: Complete terms in LICENSE.txt
---



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`


Comprehensive skill for working with Microsoft PowerPoint presentations using MCP servers.

## When to Use This Skill

- Any task where .pptx is an input, output, or transformation target
- Creating, editing, formatting, or analyzing PowerPoint files
- Building slide decks from data or templates
- Applying consistent branding across presentations
- Automating PowerPoint workflows via MCP tools

### Typical Activation Triggers

- .pptx work: presentations, slide decks, templates, slide creation/editing
- Slide content: text placeholders, bullet points, images, charts
- Design: templates, layouts, fonts, colors, themes
- Analysis: text extraction, structure inspection

---

## Part 1: PowerPoint Presentations (.pptx) via MCP

## Quick Reference

| Task | Activation / Tool |
|------|-------------------|
| Create/open presentation; add/copy/delete/rename slides | `activate_presentation_creation_and_management` |
| **Populate placeholders with text / bullet points** | `activate_text_placeholder_management` |
| Add/edit free text boxes; format inline runs | **`mcp_ppt_manage_text`** ← direct |
| Add images; analyze/optimize fonts | `activate_content_management_tools` |
| Apply theme or .pptx template | `activate_template_application_tools` |
| Extract text; inspect slide masters & layouts | `activate_information_extraction_and_management` |

> **Note:** Speaker notes, slide transitions, and animations are not exposed by the PPT MCP server.

### Tool Activation Order

```javascript
activate_presentation_creation_and_management(); // create/open, add/copy/delete slides
activate_text_placeholder_management();          // populate & bullet-point placeholders
activate_content_management_tools();             // images, fonts, text enhancement
activate_template_application_tools();           // apply .pptx theme/template
activate_information_extraction_and_management();// extract text, masters, layouts
```

---

### Create Presentation and Manage Slides

```javascript
// Create a new blank presentation
mcp_ppt_create_presentation({ filename: "deck.pptx", title: "Q3 Results" })

// Open an existing presentation
mcp_ppt_open_presentation({ filename: "deck.pptx" })

// Add a slide (append to end)
mcp_ppt_add_slide({ filename: "deck.pptx", layout_index: 1 })  // 0=blank,1=title,2=content

// Copy slide (e.g. duplicate a template slide)
mcp_ppt_copy_slide({ filename: "deck.pptx", source_index: 1, destination_index: 2 })

// Delete a slide
mcp_ppt_delete_slide({ filename: "deck.pptx", slide_index: 4 })

// Save
mcp_ppt_save_presentation({ filename: "deck.pptx" })
```

---

### Populate Placeholders (Recommended for Structured Layouts)

> Activate: `activate_text_placeholder_management()`
> Placeholders are the pre-defined text areas from the slide layout (title, body, subtitle).
> **Prefer placeholders over free text boxes** — they respect the theme's font/color.

```javascript
// Fill a title placeholder (index 0 = title on most layouts)
mcp_ppt_populate_placeholder({
  slide_index: 0,
  placeholder_index: 0,
  text: "Q3 2025 Performance Review"
})

// Fill a subtitle/body placeholder (index 1)
mcp_ppt_populate_placeholder({
  slide_index: 0,
  placeholder_index: 1,
  text: "Finance Division · October 2025"
})

// Add bullet points to a content placeholder
mcp_ppt_add_bullet_points_to_placeholder({
  slide_index: 2,
  placeholder_index: 1,
  bullet_points: [
    "Revenue up 20% YoY",
    "APAC led growth at +35%",
    "Operational costs held flat"
  ]
})
```

---

### Add and Format Free Text Boxes

> Direct tool: **`mcp_ppt_manage_text`** — no activation needed.

```javascript
// Add a new text box (position in inches from top-left)
mcp_ppt_manage_text({
  slide_index: 1,
  operation: "add",
  text: "Source: Internal BI System Q3 2025",
  font_size: 10,
  italic: true,
  color: [120, 120, 120],   // RGB
  alignment: "right",
  left: 6.5, top: 6.8, width: 3.0, height: 0.3
})

// Edit text in an existing shape
mcp_ppt_manage_text({
  slide_index: 2,
  shape_index: 1,
  operation: "edit",
  text: "Updated callout text",
  font_size: 14,
  bold: true,
  alignment: "center"
})

// Mixed inline formatting (text_runs)
mcp_ppt_manage_text({
  slide_index: 3,
  shape_index: 0,
  operation: "edit",
  text_runs: [
    { text: "KPI: ", bold: true, color: [30, 116, 69] },
    { text: "$1.8M revenue", bold: false },
    { text: " ▲12%", bold: true, color: [46, 116, 181] }
  ]
})

// Validate text fits (check auto_fit before commit)
mcp_ppt_manage_text({
  slide_index: 1,
  shape_index: 0,
  operation: "add",
  text: "Long content...",
  auto_fit: true,      // shrink to fit
  min_font_size: 10,   // don't go below 10pt
  max_font_size: 24,
  validation_only: true  // dry-run: returns fit result without saving
})
```

---

### Images and Font Management

> Activate: `activate_content_management_tools()`

```javascript
// Add an image to a slide
mcp_ppt_manage_image({
  slide_index: 2,
  operation: "add",
  image_path: "./chart_q3.png",
  left: 1.0, top: 1.5, width: 5.5, height: 3.5
})

// Analyze fonts used (identify inconsistencies)
mcp_ppt_manage_fonts({
  slide_index: null,   // null = all slides
  operation: "analyze"
})

// Replace a non-brand font across all slides
mcp_ppt_manage_fonts({
  operation: "replace",
  find_font: "Calibri",
  replace_font: "Arial"
})
```

---

### Apply Theme / Template

> Activate: `activate_template_application_tools()`

```javascript
// Apply a .pptx template to all slides (inherits master, layouts, colors)
mcp_ppt_apply_template({
  filename: "deck.pptx",
  template_name: "BrandTemplate.pptx",
  apply_to_all: true
})

// Apply a specific slide layout to one slide
mcp_ppt_apply_slide_layout({
  filename: "deck.pptx",
  slide_index: 3,
  layout_name: "Two Content"
})
```

---

### Extract Text and Inspect Structure

> Activate: `activate_information_extraction_and_management()`

```javascript
// Extract all slide text (returns slide-by-slide array)
mcp_ppt_extract_text({
  filename: "deck.pptx",
  include_slide_numbers: true
})

// Extract text from a specific slide
mcp_ppt_extract_text({ filename: "deck.pptx", slide_index: 2 })

// List available slide layouts from the master
mcp_ppt_get_slide_layouts({ filename: "deck.pptx" })

// Get slide master details (useful before applying template)
mcp_ppt_get_slide_master({ filename: "deck.pptx" })
```

---

### End-to-End Presentation Workflow

```javascript
// ── 1. Activate ──────────────────────────────────────────────────
activate_presentation_creation_and_management();
activate_text_placeholder_management();
activate_content_management_tools();
activate_template_application_tools();

// ── 2. Create + apply brand template ────────────────────────────
mcp_ppt_create_presentation({ filename: "deck.pptx", title: "Q3 Results" })
mcp_ppt_apply_template({ filename: "deck.pptx", template_name: "BrandTemplate.pptx", apply_to_all: true })

// ── 3. Title slide (slide 0 already exists) ──────────────────────
mcp_ppt_populate_placeholder({ slide_index: 0, placeholder_index: 0, text: "Q3 2025 Results" })
mcp_ppt_populate_placeholder({ slide_index: 0, placeholder_index: 1, text: "Finance Division · Oct 2025" })

// ── 4. Add content slides ────────────────────────────────────────
mcp_ppt_add_slide({ filename: "deck.pptx", layout_index: 2 })  // content layout
mcp_ppt_populate_placeholder({ slide_index: 1, placeholder_index: 0, text: "Financial Highlights" })
mcp_ppt_add_bullet_points_to_placeholder({
  slide_index: 1, placeholder_index: 1,
  bullet_points: ["Revenue: $1.8M (+20%)", "Profit margin: 33%", "APAC growth: +35%"]
})

// ── 5. Chart slide ───────────────────────────────────────────────
mcp_ppt_add_slide({ filename: "deck.pptx", layout_index: 2 })
mcp_ppt_manage_image({ slide_index: 2, operation: "add", image_path: "./chart_q3.png", left: 1, top: 1.5, width: 8, height: 4.5 })
mcp_ppt_manage_text({ slide_index: 2, operation: "add", text: "Source: BI System", font_size: 9, italic: true, left: 7.5, top: 6.8, width: 2.0, height: 0.3 })

// ── 6. Fix fonts + save ──────────────────────────────────────────
mcp_ppt_manage_fonts({ operation: "replace", find_font: "Calibri", replace_font: "Arial" })
mcp_ppt_save_presentation({ filename: "deck.pptx" })
```

---

## Part 2: Presentation Structure Standards

### PowerPoint Presentation Structure

1. **Title Slide**: Hook, topic, presenter
2. **Agenda/Overview**: What will be covered
3. **Content Slides**: Main information (1 idea per slide)
4. **Conclusion Summary**: Key takeaways
5. **Q&A / Next Steps**: What audience should do

### Formatting Standards

#### Fonts
- **Headings**: Bold, larger (32-44pt)
- **Body**: Readable size (24-32pt)
- **Consistency**: Use same font families throughout

#### Colors
- **Primary**: Main brand or accent color (use 60-70%)
- **Secondary**: Supporting colors (20-30%)
- **Neutral**: Backgrounds, borders (remaining %)

#### Spacing
- **White space**: Don't crowd slides
- **Alignment**: Use grid-based spacing
- **Visual hierarchy**: Size and weight guide eye

#### Slide Design
- **1 idea per slide**: Maximum 50 words
- **Bullet points**: Use for lists, not paragraphs
- **Images**: High quality, relevant to content
- **Consistency**: Same layout for similar content

---

## Part 3: Quality Checklist

```markdown
## Presentation Quality Checklist

### Content
- [ ] Placeholders used for title/body (not free text boxes) — preserves theme styling
- [ ] 1 main idea per slide; ≤50 words
- [ ] Bullet points via add_bullet_points_to_placeholder (not manual text boxes)
- [ ] Charts/images provided as high-res PNG/SVG at correct aspect ratio
- [ ] Source labels added as small text boxes on data slides

### Design
- [ ] Brand template applied (mcp_ppt_apply_template)
- [ ] Fonts consistent — run font analysis and replace non-brand fonts
- [ ] Title slide: title + subtitle placeholders both populated
- [ ] No placeholder default text remaining ("Click to add title" etc.)

### Structure
- [ ] Slide 0: title slide
- [ ] Slide 1: agenda or key takeaway
- [ ] Content slides: one section per major point
- [ ] Final slide: summary / next steps

### Validation
- [ ] auto_fit checked on text-heavy slides (validation_only: true)
- [ ] Font replacement run across all slides
- [ ] Presentation saved before distribution
```

---

## Part 4: MCP Tool Activation Guide

### Activation Commands

When working with PowerPoint presentations, use these MCP activation patterns:

```javascript
// PowerPoint documents
activate_presentation_creation_and_management(); // create/open, add/copy/delete slides
activate_text_placeholder_management();          // populate placeholders, add bullet points
activate_content_management_tools();             // add images, analyze/replace fonts
activate_template_application_tools();           // apply .pptx theme or template
activate_information_extraction_and_management();// extract text, slide masters, layouts
```

### Workflow Examples

#### Template-Based Presentation Generation

1. **Start with template** (PowerPoint)
2. **Copy template** to new filename
3. **Populate placeholders** with actual content
4. **Add slides** as needed
5. **Apply styling** consistently across slides
6. **Save final version**

---

## Part 5: Best Practices

### MCP-Specific Best Practices

- **Activate tools as needed**: Enable MCP tool groups only when required to avoid unnecessary overhead
- **Validate operations**: Confirm operations completed successfully, especially for batch operations
- **Handle errors gracefully**: Catch and report MCP tool errors with context for troubleshooting
- **Batch operations**: Use array-based operations when available for efficiency
- **Document file paths**: Use clear, relative paths and maintain documentation of file locations

### Presentation Best Practices

- **Use placeholders**: They respect theme styling and are easier to maintain
- **Limit text**: One idea per slide, maximum 50 words
- **High-quality images**: Use PNG/SVG at correct resolution
- **Consistent branding**: Apply template to all slides
- **Font consistency**: Run font analysis and replace non-brand fonts
- **Test before presenting**: Validate all placeholders are populated

---

## References & Resources

### Documentation
- [PowerPoint References](./references/) — PowerPoint formatting and manipulation reference

### Examples
- [Presentation Examples](./examples/presentation-examples.md) — Examples of creating presentations programmatically

### Scripts
- [PPT Automation Script](./scripts/ppt-automation.py) — Python script for presentation automation

---


---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [microsoft-development](../microsoft-development/SKILL.md) | Microsoft SDK/docs reference |
| [excel-sheet](../excel-sheet/SKILL.md) | Embed Excel data/charts in slides |
| [word-document](../word-document/SKILL.md) | Companion Office document creation |
