# DESIGN.md Example

This example shows a compact Stitch-ready design-system document. It is based on
local HTML, screenshots, or user-provided product context rather than assuming
screen-retrieval MCP tools are available.

```markdown
# Design System: FoodieHub

## 1. Visual Theme & Atmosphere

FoodieHub feels warm, practical, and welcoming. The interface should read like a
modern recipe workspace: bright surfaces, clear hierarchy, restrained warmth,
and fast scanning for recipe metadata.

## 2. Color Palette & Roles

- Warm Orange (#EA580C): Primary actions, active navigation, search emphasis.
- Soft Amber Wash (#FFF7ED): Hero and recipe-highlight backgrounds.
- Charcoal Text (#111827): Primary headings and high-emphasis labels.
- Muted Slate (#6B7280): Secondary text, descriptions, helper copy.
- Fresh Green (#15803D): Dietary labels and positive status badges.
- Border Gray (#E5E7EB): Structural dividers and card borders.

## 3. Typography Rules

- Display headings use a bold sans-serif with compact line height and strong
  contrast against the page background.
- Body text uses a readable sans-serif, 16px baseline, and relaxed leading for
  recipe instructions.
- Metadata such as time, difficulty, and servings uses smaller text with muted
  color and consistent icon spacing.

## 4. Component Stylings

- Navigation: horizontal desktop bar with logo, primary links, and one sign-in
  action.
- Search: wide input paired with a warm primary button; preserve large tap
  targets on mobile.
- Recipe cards: white surfaces, subtle border, 12px radius, image crop at the
  top, badge and title hierarchy below.
- Detail pages: large hero image, compact metadata row, clear two-column content
  on desktop, single-column flow on mobile.

## 5. Layout Principles

- Use generous section spacing on marketing or discovery pages.
- Keep recipe grids predictable: 3 columns on desktop, 2 on tablet, 1 on mobile.
- Avoid overlapping content and decorative clutter.
- Let food imagery carry visual richness; keep UI chrome simple.

## 6. Stitch Generation Notes

- Describe screens with sections first: navigation, hero/search, recipe grid,
  detail content, footer.
- Use the palette names above when writing prompts.
- Do not invent recipe statistics or user counts. Use placeholders when data is
  not supplied.
```

## Verification Notes

- Values in a real DESIGN.md should be traced to source files, exported HTML,
  screenshots, or explicit user choices.
- Upload through `stitch-manage-design-system` when the user wants this design
  system created in Stitch.
