# Design Principles Reference

Comprehensive reference for fundamental design principles applied to digital and canvas-based visual creation.

---

## Gestalt Principles

The Gestalt principles describe how humans perceive visual elements as organized patterns and unified wholes rather than isolated parts.

### Proximity

Elements placed close together are perceived as a group.

**Application:**
- Group related form fields (label + input + helper text) with tight spacing
- Separate distinct sections with generous margins
- Navigation items clustered by category signal relatedness

**Canvas example:**
```
✅ Grouped (perceived as related)     ❌ Even spacing (no grouping)

  [Icon] Title                         [Icon]
  Description text                     Title
  [Action Button]                      Description text
                                       [Action Button]
  [Icon] Title
  Description text
  [Action Button]
```

**Practical values:**
- Related elements: 4–8px gap
- Grouped sections: 24–48px gap
- Major page sections: 64–96px gap

---

### Similarity

Elements sharing visual characteristics (color, shape, size, texture) are perceived as related.

**Application:**
- All primary actions share the same button style (color, border-radius, font weight)
- Card components across a grid use identical structure so users recognize them as a collection
- Tags/badges use a consistent pill shape with varied background colors to signal category

**Canvas example:**
```
Primary actions → all solid, rounded, brand-colored
Secondary actions → all outlined, same border-radius
Destructive actions → all solid, red-toned
```

**Tip:** Break similarity intentionally to draw attention. A single red card in a grid of white cards immediately becomes a focal point.

---

### Closure

The mind fills in missing visual information to perceive a complete shape.

**Application:**
- Progress indicators (partially filled circles/bars) imply completion without drawing every state
- Icon design: simple outlines suggest objects without drawing every detail
- Cropped images at container edges imply content continues beyond the viewport

**Canvas example:**
```
[████████░░░░] 65% complete
     ↑
Users perceive a full bar with a "filled" portion —
closure completes the empty segment as "remaining."
```

---

### Continuity

Elements arranged along a line or curve are perceived as more related than randomly placed elements.

**Application:**
- Horizontal timelines guide the eye left-to-right through sequential steps
- Curved paths in onboarding flows create a sense of journey
- Alignment along a grid column makes vertical lists feel connected

**Canvas example:**
```
Step 1 ──────── Step 2 ──────── Step 3 ──────── Step 4
  ●                ●                ●                ○

The connecting line guides the eye and implies order.
```

---

### Figure/Ground

The brain separates visual fields into a foreground subject (figure) and background.

**Application:**
- Modal overlays use dimmed/blurred backgrounds to push content behind and elevate the dialog
- Cards with subtle shadows float above the page background
- Selected list items use a highlighted background to distinguish them from siblings

**Canvas example:**
```
┌──────────────────────────────┐
│  ░░░░░░░░░░░░░░░░░░░░░░░░░  │  ← Background (dimmed)
│  ░░┌────────────────┐░░░░░  │
│  ░░│  Modal Content  │░░░░░  │  ← Figure (elevated)
│  ░░│  [Confirm] [X]  │░░░░░  │
│  ░░└────────────────┘░░░░░  │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░  │
└──────────────────────────────┘
```

---

## Visual Hierarchy

Visual hierarchy controls the order in which the eye processes information. It is achieved by manipulating size, weight, color, contrast, spacing, and position.

### Size Scale

Larger elements are perceived as more important.

| Level | Use Case | Example Size |
|-------|----------|-------------|
| H1 | Page title | 32–48px |
| H2 | Section heading | 24–32px |
| H3 | Subsection | 20–24px |
| Body | Paragraph text | 16px |
| Caption | Supporting text | 12–14px |

### Weight & Emphasis

- **Bold** (600–700) for headings and labels
- **Medium** (500) for buttons and interactive text
- **Regular** (400) for body copy
- **Light** (300) used sparingly for large display text

### Color as Hierarchy

- High-contrast text (near-black on white) for primary content
- Medium-contrast (gray-600) for secondary/supporting text
- Low-contrast (gray-400) for placeholders, disabled states, metadata

### Position

- Top-left (in LTR layouts) is scanned first — place the most important element there
- F-pattern and Z-pattern scanning models guide content placement
- "Above the fold" content gets more attention

---

## Balance & Symmetry

### Symmetrical Balance

Equal visual weight distributed on both sides of a central axis. Creates stability, formality, and order.

**Use for:** Landing pages, centered hero sections, login forms, about pages.

```
        ┌──────────────────┐
        │   Brand Logo     │
        │                  │
        │  Headline Text   │
        │  Subheading      │
        │                  │
        │  [Get Started]   │
        └──────────────────┘
```

### Asymmetrical Balance

Unequal elements balanced by visual weight (a large light element can counterbalance a small dark element).

**Use for:** Dashboards, magazine-style layouts, editorial content, creative portfolios.

```
┌───────────────┬─────────┐
│               │  Small  │
│  Large Image  │  Text   │
│               │  Block  │
│               │  +CTA   │
└───────────────┴─────────┘
```

### Radial Balance

Elements radiate from a central point, drawing the eye inward.

**Use for:** Infographics, feature overviews arranged in a circle, dashboard widgets around a central metric.

---

## Contrast

Contrast creates visual distinction and draws attention. It operates across multiple dimensions:

| Dimension | Low Contrast | High Contrast |
|-----------|-------------|---------------|
| Color | Gray on light gray | Black on white |
| Size | 14px vs 16px | 14px vs 48px |
| Weight | Regular vs Medium | Light vs Bold |
| Shape | Rounded rect vs Rounded rect | Circle vs Sharp rectangle |
| Texture | Flat vs Flat | Flat vs Textured/gradient |

**WCAG Contrast Requirements:**
- Normal text (< 18px): minimum 4.5:1 ratio against background
- Large text (≥ 18px or 14px bold): minimum 3:1 ratio
- UI components and graphical objects: minimum 3:1 ratio

---

## Repetition & Pattern

Repeating visual elements creates consistency, rhythm, and learnability.

**Application:**
- Consistent card structure across recipe listings (image → title → meta → action)
- Repeated icon style (outlined, 24px, 1.5px stroke) throughout the UI
- Uniform spacing rhythm (multiples of 4px or 8px)
- Same animation easing for all micro-interactions

**Spacing rhythm example (8px base):**
```
8px  → icon padding, inline gaps
16px → form field spacing, card padding
24px → section internal padding
32px → between card groups
48px → major section gaps
64px → page section dividers
```

---

## Alignment

Alignment creates visual connections and order. Even when elements differ in size or type, alignment along shared edges or axes unifies them.

### Types of Alignment

| Type | Description | Best For |
|------|-------------|----------|
| Left | Elements share a left edge | Body text, forms, lists |
| Center | Elements share a center axis | Hero sections, dialogs, headings |
| Right | Elements share a right edge | Numeric data, price columns |
| Baseline | Text baselines align horizontally | Mixed-size inline text |

**Rule:** Every element on a canvas should be visually connected to at least one other element through alignment. If something looks "off," check alignment first.

---

## Whitespace (Negative Space)

Whitespace is not empty — it is an active design element that provides breathing room, focus, and elegance.

### Micro vs Macro Whitespace

- **Micro whitespace:** Space between letters (tracking), lines (leading), inline elements. Affects readability.
- **Macro whitespace:** Space between sections, around page content, margins. Affects layout and emphasis.

### Whitespace Guidelines

| Context | Recommended Spacing |
|---------|-------------------|
| Line height (body text) | 1.5–1.75× font size |
| Paragraph spacing | 1× font size |
| Card padding | 16–24px |
| Section margin | 48–96px |
| Page margin (desktop) | 64–120px |
| Page margin (mobile) | 16–24px |

**Principle:** When in doubt, add more whitespace. Cramped layouts feel amateur; generous spacing feels premium.

---

## Typography Pairing Rules

### The Core Rules

1. **Limit to 2 typefaces** — one for headings, one for body. Three is the absolute maximum.
2. **Contrast in structure, harmony in quality** — pair a serif with a sans-serif, or a geometric sans with a humanist sans.
3. **Match x-heights** — typefaces with similar x-heights feel cohesive at the same size.
4. **Avoid pairing fonts from the same classification** — two geometric sans-serifs compete rather than complement.

### Proven Pairings

| Heading | Body | Mood |
|---------|------|------|
| Playfair Display (serif) | Inter (sans-serif) | Elegant, modern editorial |
| Montserrat (geometric sans) | Merriweather (serif) | Confident, readable |
| Poppins (geometric sans) | Lora (serif) | Friendly, warm |
| Space Grotesk (sans) | IBM Plex Sans (sans) | Technical, clean |
| Fraunces (soft serif) | Work Sans (sans) | Approachable, crafted |

### Type Scale

Use a modular scale for consistent sizing. Common ratios:

| Ratio | Name | Scale (base 16px) |
|-------|------|-------------------|
| 1.200 | Minor Third | 16, 19, 23, 28, 33 |
| 1.250 | Major Third | 16, 20, 25, 31, 39 |
| 1.333 | Perfect Fourth | 16, 21, 28, 38, 50 |
| 1.414 | Augmented Fourth | 16, 23, 32, 45, 64 |
| 1.618 | Golden Ratio | 16, 26, 42, 68, 110 |

---

## The Golden Ratio (φ ≈ 1.618)

The golden ratio appears throughout nature and has been used in art and architecture for centuries. In digital design, it provides a mathematically pleasing proportion.

### Applications

**Layout proportions:**
```
Total width: 960px
├── Content area: 593px  (960 / 1.618)
└── Sidebar: 367px       (960 - 593)
```

**Typography scale:**
```
Body: 16px
H3:  16 × 1.618 ≈ 26px
H2:  26 × 1.618 ≈ 42px
H1:  42 × 1.618 ≈ 68px
```

**Spacing:**
```
Base unit: 8px
Next: 8 × 1.618 ≈ 13px
Next: 13 × 1.618 ≈ 21px
Next: 21 × 1.618 ≈ 34px
Next: 34 × 1.618 ≈ 55px
```

**Golden rectangle in image composition:**
Divide a rectangle into a square and a smaller rectangle — the smaller rectangle has the same aspect ratio as the whole. Use the spiral to guide focal point placement.

---

## Grid Systems

Grids provide structure, consistency, and alignment across layouts.

### 12-Column Grid

The most common grid for web design. 12 divides evenly by 1, 2, 3, 4, 6, and 12, enabling flexible layouts.

```
|  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 |

Full width:      ├──────────────────────────────────────────────┤
Two halves:      ├─────────────────────┤├─────────────────────┤
Thirds:          ├──────────────┤├──────────────┤├──────────────┤
Sidebar + Main:  ├──────┤├──────────────────────────────────────┤
                  (3 col)              (9 col)
```

### Grid Terminology

| Term | Definition | Typical Values |
|------|-----------|---------------|
| Column | Vertical content blocks | 12 columns |
| Gutter | Space between columns | 16–32px |
| Margin | Space outside the grid on each side | 16–64px |
| Max width | Maximum content width | 1200–1440px |

### Responsive Breakpoints

| Breakpoint | Columns | Gutter | Margin |
|-----------|---------|--------|--------|
| Mobile (< 640px) | 4 | 16px | 16px |
| Tablet (640–1024px) | 8 | 24px | 32px |
| Desktop (> 1024px) | 12 | 32px | 64px |

### 8px Grid (Spatial Grid)

All dimensions and spacing snap to multiples of 8px. This creates a consistent rhythm and simplifies responsive math.

```
Padding: 8, 16, 24, 32, 40, 48 ...
Heights: 32 (small), 40 (medium), 48 (large)
Icon size: 16, 24, 32
Border radius: 4, 8, 12, 16
```

**Why 8px:** Scales cleanly across screen densities (1x, 1.5x, 2x, 3x) without sub-pixel rendering issues.

---

## Quick Reference: Principle Checklist

Use this checklist when reviewing any canvas or digital design:

- [ ] **Proximity** — Are related items grouped? Are unrelated items separated?
- [ ] **Similarity** — Do similar elements share visual treatment?
- [ ] **Closure** — Can shapes or patterns be simplified while still being understood?
- [ ] **Continuity** — Do elements guide the eye along intentional paths?
- [ ] **Figure/Ground** — Is the focal element clearly distinguished from the background?
- [ ] **Hierarchy** — Can a viewer identify the #1, #2, #3 most important elements within 3 seconds?
- [ ] **Balance** — Does the layout feel stable (symmetrical or intentionally asymmetrical)?
- [ ] **Contrast** — Is there sufficient contrast for readability and emphasis?
- [ ] **Repetition** — Are patterns and components used consistently?
- [ ] **Alignment** — Is every element visually anchored to at least one other?
- [ ] **Whitespace** — Is there enough breathing room? Does the layout feel spacious, not cramped?
- [ ] **Typography** — Are fonts limited to 2–3? Is the type scale consistent?
- [ ] **Grid** — Are elements placed on a consistent grid or spatial system?
