# Design System Example: FoodieHub

Complete example showing how to generate a DESIGN.md from Stitch project screen data.

---

## Step 1: Raw Stitch Screen Data

After calling `mcp_stitch_list_screens` for the FoodieHub project, the response includes HTML for each screen. Below is a simplified extraction of design-relevant data from three screens.

### Screen: Home Page (Desktop)

```html
<div class="min-h-screen bg-white">
  <!-- Nav -->
  <nav class="flex items-center justify-between px-8 py-4 border-b border-gray-200">
    <span class="text-2xl font-bold text-orange-600">FoodieHub</span>
    <div class="flex gap-6">
      <a class="text-sm font-medium text-gray-700 hover:text-orange-600">Recipes</a>
      <a class="text-sm font-medium text-gray-700 hover:text-orange-600">Meal Plans</a>
      <a class="text-sm font-medium text-gray-700 hover:text-orange-600">Community</a>
    </div>
    <button class="px-4 py-2 bg-orange-600 text-white rounded-lg text-sm font-medium">Sign In</button>
  </nav>

  <!-- Hero -->
  <section class="px-8 py-16 bg-gradient-to-r from-orange-50 to-amber-50 text-center">
    <h1 class="text-5xl font-bold text-gray-900 mb-4">Discover Delicious Recipes</h1>
    <p class="text-lg text-gray-600 max-w-xl mx-auto">Find, save, and share your favorite meals.</p>
    <div class="mt-8 flex gap-4 justify-center">
      <input class="px-4 py-3 rounded-lg border border-gray-300 w-80 text-sm" placeholder="Search recipes..." />
      <button class="px-6 py-3 bg-orange-600 text-white rounded-lg font-medium">Search</button>
    </div>
  </section>

  <!-- Recipe Cards Grid -->
  <section class="px-8 py-12 grid grid-cols-3 gap-6">
    <div class="rounded-xl border border-gray-200 overflow-hidden shadow-sm hover:shadow-md transition-shadow">
      <img class="w-full h-48 object-cover" src="pasta.jpg" />
      <div class="p-4">
        <span class="text-xs font-medium px-2 py-1 bg-green-100 text-green-700 rounded-full">Vegetarian</span>
        <h3 class="text-lg font-semibold text-gray-900 mt-2">Creamy Pesto Pasta</h3>
        <p class="text-sm text-gray-500 mt-1">30 min · Easy · 4 servings</p>
        <div class="flex items-center gap-2 mt-3">
          <img class="w-6 h-6 rounded-full" src="avatar.jpg" />
          <span class="text-xs text-gray-500">Chef Maria</span>
        </div>
      </div>
    </div>
  </section>
</div>
```

### Screen: Recipe Detail (Desktop)

```html
<div class="max-w-4xl mx-auto px-8 py-8">
  <img class="w-full h-80 rounded-2xl object-cover" src="detail.jpg" />
  <h1 class="text-3xl font-bold text-gray-900 mt-6">Creamy Pesto Pasta</h1>
  <div class="flex gap-4 mt-3">
    <span class="text-sm text-gray-500">⏱ 30 min</span>
    <span class="text-sm text-gray-500">👤 4 servings</span>
    <span class="text-sm text-gray-500">📊 Easy</span>
  </div>
  <div class="flex gap-2 mt-4">
    <button class="px-4 py-2 bg-orange-600 text-white rounded-lg text-sm">Save Recipe</button>
    <button class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg text-sm">Share</button>
  </div>
  <!-- Ingredients & Steps in 2-column layout -->
  <div class="grid grid-cols-3 gap-8 mt-8">
    <div class="col-span-1 bg-orange-50 rounded-xl p-6">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">Ingredients</h2>
      <ul class="space-y-2 text-sm text-gray-700">...</ul>
    </div>
    <div class="col-span-2">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">Instructions</h2>
      <ol class="space-y-4 text-sm text-gray-700">...</ol>
    </div>
  </div>
</div>
```

### Screen: Profile Page (Desktop)

```html
<div class="max-w-4xl mx-auto px-8 py-8">
  <div class="flex items-center gap-6">
    <img class="w-20 h-20 rounded-full border-2 border-orange-200" src="profile.jpg" />
    <div>
      <h1 class="text-2xl font-bold text-gray-900">Chef Maria</h1>
      <p class="text-sm text-gray-500">Food blogger · 127 recipes · 4.2k followers</p>
    </div>
    <button class="ml-auto px-4 py-2 bg-orange-600 text-white rounded-lg text-sm">Follow</button>
  </div>
  <div class="mt-8 border-b border-gray-200">
    <div class="flex gap-8">
      <button class="pb-3 border-b-2 border-orange-600 text-sm font-medium text-orange-600">Recipes</button>
      <button class="pb-3 text-sm font-medium text-gray-500">Meal Plans</button>
      <button class="pb-3 text-sm font-medium text-gray-500">Saved</button>
    </div>
  </div>
</div>
```

---

## Step 2: Extracted Design Tokens

From the screen HTML above, the following tokens are extracted:

### Colors
| Source Class | Hex | Role |
|-------------|-----|------|
| `text-orange-600`, `bg-orange-600` | `#EA580C` | Primary brand / CTA |
| `bg-orange-50`, `from-orange-50` | `#FFF7ED` | Primary tint / hero background |
| `bg-amber-50` | `#FFFBEB` | Warm accent background |
| `bg-green-100`, `text-green-700` | `#DCFCE7` / `#15803D` | Vegetarian/success tag |
| `text-gray-900` | `#111827` | Heading text |
| `text-gray-700` | `#374151` | Body text |
| `text-gray-500` | `#6B7280` | Secondary/muted text |
| `text-gray-300`, `border-gray-300` | `#D1D5DB` | Borders, input outlines |
| `border-gray-200` | `#E5E7EB` | Dividers, card borders |
| `bg-white` | `#FFFFFF` | Page background |

### Typography
| Element | Classes | Size | Weight |
|---------|---------|------|--------|
| Logo | `text-2xl font-bold` | 1.5rem | 700 |
| Hero H1 | `text-5xl font-bold` | 3rem | 700 |
| Page H1 | `text-3xl font-bold` | 1.875rem | 700 |
| Section H2 | `text-lg font-semibold` | 1.125rem | 600 |
| Card Title | `text-lg font-semibold` | 1.125rem | 600 |
| Body | `text-sm` | 0.875rem | 400 |
| Caption | `text-xs` | 0.75rem | 400/500 |
| Nav Link | `text-sm font-medium` | 0.875rem | 500 |

### Border Radius
| Usage | Class | Value |
|-------|-------|-------|
| Buttons | `rounded-lg` | 0.5rem |
| Cards | `rounded-xl` | 0.75rem |
| Hero image | `rounded-2xl` | 1rem |
| Tags | `rounded-full` | 9999px |
| Avatars | `rounded-full` | 9999px |

### Shadows
| Usage | Class | Description |
|-------|-------|-------------|
| Card default | `shadow-sm` | Subtle elevation |
| Card hover | `shadow-md` | Medium elevation on interaction |

---

## Step 3: Generated DESIGN.md

```markdown
# FoodieHub — Design System

> Design tokens and component patterns extracted from the FoodieHub Stitch project.

## Brand Identity

- **Name:** FoodieHub
- **Tagline:** Discover Delicious Recipes
- **Personality:** Warm, appetizing, approachable, community-driven

## Color Palette

### Primary

| Name | Hex | HSL | Usage |
|------|-----|-----|-------|
| Orange 600 | `#EA580C` | 25 93% 48% | Primary buttons, links, active tabs, brand color |
| Orange 50 | `#FFF7ED` | 33 100% 96% | Hero backgrounds, ingredient panels, light tints |
| Amber 50 | `#FFFBEB` | 48 100% 96% | Gradient pair for hero section |

### Neutral

| Name | Hex | Usage |
|------|-----|-------|
| Gray 900 | `#111827` | Headings, primary text |
| Gray 700 | `#374151` | Body text, nav links |
| Gray 500 | `#6B7280` | Secondary text, metadata |
| Gray 300 | `#D1D5DB` | Input borders, outlines |
| Gray 200 | `#E5E7EB` | Dividers, card borders |
| White | `#FFFFFF` | Page background, card backgrounds |

### Semantic

| Name | Hex | Usage |
|------|-----|-------|
| Green 700 | `#15803D` | Success, vegetarian tags |
| Green 100 | `#DCFCE7` | Tag backgrounds |

### CSS Variables (shadcn/ui mapping)

```css
:root {
  --primary: 25 93% 48%;         /* Orange 600 */
  --primary-foreground: 0 0% 100%;
  --secondary: 33 100% 96%;      /* Orange 50 */
  --secondary-foreground: 25 93% 48%;
  --background: 0 0% 100%;
  --foreground: 222 47% 11%;     /* Gray 900 */
  --muted: 220 13% 91%;          /* Gray 200 */
  --muted-foreground: 220 9% 46%;/* Gray 500 */
  --accent: 48 100% 96%;         /* Amber 50 */
  --accent-foreground: 222 47% 11%;
  --destructive: 0 84% 60%;
  --border: 220 13% 91%;
  --input: 220 13% 87%;
  --ring: 25 93% 48%;
  --radius: 0.5rem;
}
```

## Typography

**Font Family:** System default (Inter recommended for production)

| Scale | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| Display | 3rem (48px) | Bold (700) | 1.1 | Hero headlines |
| H1 | 1.875rem (30px) | Bold (700) | 1.2 | Page titles |
| H2 | 1.5rem (24px) | Semibold (600) | 1.3 | Section headings |
| H3 | 1.125rem (18px) | Semibold (600) | 1.4 | Card titles, subsections |
| Body | 0.875rem (14px) | Regular (400) | 1.5 | Paragraphs, descriptions |
| Caption | 0.75rem (12px) | Medium (500) | 1.4 | Tags, metadata, timestamps |

## Component Styles

### Buttons

| Variant | Background | Text | Border | Radius | Padding |
|---------|-----------|------|--------|--------|---------|
| Primary | Orange 600 | White | None | 0.5rem | 16px 24px |
| Secondary/Outline | White | Gray 700 | Gray 300 1px | 0.5rem | 16px 24px |
| Ghost (nav link) | Transparent | Gray 700 → Orange 600 on hover | None | — | — |

### Cards

- **Border:** 1px Gray 200
- **Radius:** 0.75rem (rounded-xl)
- **Shadow:** shadow-sm default, shadow-md on hover
- **Transition:** `transition-shadow` for smooth hover effect
- **Image:** Full-width, h-48, object-cover, overflow-hidden
- **Padding:** 1rem (16px) on content area

### Tags/Badges

- **Radius:** rounded-full (pill shape)
- **Padding:** 4px 8px
- **Font:** text-xs font-medium
- **Variants:**
  - Vegetarian: Green 100 bg + Green 700 text
  - Default: Gray 100 bg + Gray 600 text

### Navigation

- **Desktop:** Horizontal flex, gap-6, text-sm font-medium
- **Active tab:** border-b-2 border-orange-600, text-orange-600
- **Inactive tab:** text-gray-500
- **Top bar:** border-b border-gray-200, px-8 py-4

### Forms

- **Input:** px-4 py-3, rounded-lg, border border-gray-300
- **Placeholder:** text-sm, gray-400
- **Focus:** ring-2 ring-orange-600 (recommended)

### Profile/Avatar

- **Size:** w-20 h-20 (large), w-6 h-6 (inline)
- **Shape:** rounded-full
- **Border:** 2px orange-200 (profile), none (inline)

## Layout Principles

- **Max width:** max-w-4xl for content pages, full-width for home
- **Horizontal padding:** px-8 (32px) on all sections
- **Section spacing:** py-12 to py-16 between major sections
- **Grid:** 3-column for card grids, 1/3 + 2/3 for detail pages
- **Responsive breakpoints:** md (768px) for 2-col, lg (1024px) for 3-col

## Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | Tight gaps within elements |
| sm | 8px | Tag padding, tight spacing |
| md | 16px | Card padding, section inner spacing |
| lg | 24px | Component gaps, grid gaps |
| xl | 32px | Page horizontal padding |
| 2xl | 48px | Section vertical padding |
| 3xl | 64px | Hero vertical padding |
```

---

## Summary

This example demonstrates the full workflow:

1. **Fetch** Stitch screens with `mcp_stitch_list_screens`
2. **Extract** design tokens from HTML classes and inline styles
3. **Map** Tailwind classes to concrete values (hex, rem, px)
4. **Organize** into a structured DESIGN.md with sections for colors, typography, components, layout, and spacing
5. **Include** CSS variable definitions for shadcn/ui theming
