# PRD: Recipe Search Enhancement

**Author:** Kitchen Odyssey Product Team
**Status:** Approved
**Created:** 2026-01-15
**Last Updated:** 2026-02-08
**Related:** [Design Overhaul Plan](../../../Kitchen_Odyssey/plan/design-overhaul-1.md)

---

## 1. Problem Statement

Kitchen Odyssey users currently browse recipes through a simple list on the Home page or navigate to the Search page, which supports only basic text matching against recipe titles. User feedback and analytics reveal significant friction:

- **72% of search sessions end without a recipe selection** — users cannot find what they are looking for.
- **Users search by ingredient** ("chicken thighs", "leftover rice") but the system only matches titles.
- **No filtering by dietary restriction** — vegetarian, vegan, gluten-free, and dairy-free users must scan results manually.
- **No sorting options** — results appear in insertion order regardless of relevance, rating, or preparation time.
- **Mobile users abandon search 2x more often** than desktop users due to cramped filter UX.

Improving search directly impacts user engagement, recipe discovery, and retention.

## 2. Goals & Non-Goals

### Goals

- Enable ingredient-based search so users can find recipes by what they have on hand.
- Provide filterable, sortable search results with dietary, cuisine, difficulty, and time filters.
- Deliver a mobile-first search experience that is fast and intuitive.
- Increase search-to-view conversion rate from 28% to 55% within 60 days of launch.

### Non-Goals

- Full-text search across recipe instructions (deferred to Phase 2).
- AI-powered recipe recommendations (separate initiative).
- Search across external recipe APIs or third-party content.
- Changes to recipe creation or editing flows.

## 3. User Stories

### Story 1: Home Cook — Search by Ingredient

> As a home cook, I want to search for recipes by the ingredients I have, so that I can decide what to make without going to the store.

**Acceptance Criteria:**
- [ ] Given I type "chicken, broccoli" in the search bar, when I submit, then I see recipes that include both "chicken" and "broccoli" in their ingredient lists.
- [ ] Given a recipe contains "chicken breast" and I search for "chicken", then that recipe appears in results (partial ingredient matching).
- [ ] Given I search for an ingredient that matches zero recipes, then I see a friendly empty state with suggestions.

### Story 2: Health-Conscious User — Filter by Dietary Restriction

> As a health-conscious user, I want to filter search results by dietary labels, so that I only see recipes I can eat.

**Acceptance Criteria:**
- [ ] Given I select the "Vegetarian" filter, when results load, then every displayed recipe is tagged as vegetarian.
- [ ] Given I select multiple filters ("Gluten-Free" + "Under 30 min"), then results match ALL selected filters (AND logic).
- [ ] Given I clear all filters, then the full unfiltered result set is displayed.
- [ ] Given filters are applied, then the active filter count is shown on the filter button (mobile).

### Story 3: Busy Parent — Sort by Preparation Time

> As a busy parent, I want to sort recipes by total preparation time, so that I can find quick meals on weeknights.

**Acceptance Criteria:**
- [ ] Given I select "Sort by: Prep Time (Low to High)", then results reorder by ascending total time.
- [ ] Given I change the sort to "Rating (High to Low)", then results reorder by descending average rating.
- [ ] Given the current sort is active, then the sort button label reflects the active sort option.

### Story 4: Mobile User — Responsive Filter Panel

> As a mobile user, I want to access filters in a slide-up panel, so that I can refine results without losing my scroll position.

**Acceptance Criteria:**
- [ ] Given I am on a screen narrower than 768px, when I tap the filter icon, then a bottom sheet slides up with all filter options.
- [ ] Given I apply filters in the bottom sheet and tap "Apply", then results update and the sheet closes.
- [ ] Given I am on desktop (>=1024px), then filters appear as a sidebar alongside results.

### Story 5: Guest User — Search Without Account

> As a guest user, I want to search and filter recipes without logging in, so that I can explore before creating an account.

**Acceptance Criteria:**
- [ ] Given I am not logged in, when I use search, then I see the same search/filter functionality as authenticated users.
- [ ] Given I try to save a recipe from search results as a guest, then I am prompted to sign up.

## 4. Success Metrics

| Metric | Baseline | Target | Measurement Method |
|--------|----------|--------|--------------------|
| Search-to-view conversion rate | 28% | 55% | Analytics: search result clicks / total searches |
| Average searches per session | 1.2 | 2.0 | Analytics: search events per session |
| Search abandonment rate | 72% | 35% | Analytics: searches with 0 result clicks |
| Filter usage rate | 0% (N/A) | 40% of searches | Analytics: searches with ≥1 filter applied |
| Mobile search task completion | 38% | 65% | Analytics: mobile search-to-view conversion |
| Page load time (search results) | N/A | < 500ms (P95) | Performance monitoring |

## 5. Design & UX

### 5.1 Search Bar Enhancement

- Unified search bar at the top of the Home and Search pages.
- Supports both title and ingredient search with auto-detection.
- Placeholder text cycles: "Search recipes...", "Try 'pasta with tomatoes'...", "Search by ingredient..."
- Shows recent searches (stored locally) when focused.

### 5.2 Search Results Page

**Desktop (≥1024px):**
- Left sidebar (280px): Filters panel — always visible.
- Main content: Recipe cards in a responsive grid (3 columns).
- Top bar: Result count, active sort dropdown, view toggle (grid/list).

**Tablet (768px–1023px):**
- Collapsible filter sidebar with toggle button.
- Recipe cards in 2-column grid.

**Mobile (<768px):**
- Full-width search bar with filter icon button.
- Filter bottom sheet (slide-up panel) triggered by filter icon.
- Recipe cards in single-column stack.
- Infinite scroll with "Load more" fallback.

### 5.3 Filter Panel Design

| Filter Category | Type | Options |
|----------------|------|---------|
| Dietary | Multi-select checkboxes | Vegetarian, Vegan, Gluten-Free, Dairy-Free, Nut-Free |
| Cuisine | Multi-select checkboxes | Thai, Italian, Mexican, Japanese, Indian, American, Mediterranean, Other |
| Difficulty | Single-select radio | Easy, Medium, Hard |
| Prep Time | Range slider | 0–120+ minutes |
| Rating | Minimum rating stars | 1–5 stars |

### 5.4 Empty & Error States

- **No results:** Illustration + "No recipes found. Try different ingredients or relax your filters." + "Clear all filters" button.
- **Search error:** "Something went wrong. Please try again." + Retry button.
- **Loading:** Skeleton cards matching the recipe card layout.

## 6. Technical Requirements

### 6.1 Frontend (React + Vite + Tailwind)

- New `SearchFilters` component with debounced input (300ms).
- New `FilterPanel` component (responsive: sidebar on desktop, bottom sheet on mobile).
- Update existing `RecipeCard` component to highlight matched ingredients.
- URL-based filter state (`/search?q=chicken&diet=vegetarian&sort=time`) for shareable search links.
- Client-side filter/sort logic for the current dataset size (<500 recipes). Migrate to server-side if dataset exceeds 1,000.

### 6.2 Data Model Changes

Add fields to existing recipe schema:

| Field | Type | Description |
|-------|------|-------------|
| `ingredients` | `string[]` | Normalized ingredient list (lowercase, trimmed) |
| `dietaryTags` | `string[]` | Dietary labels: `vegetarian`, `vegan`, `gluten-free`, etc. |
| `cuisine` | `string` | Cuisine category |
| `difficulty` | `string` | `easy` \| `medium` \| `hard` |
| `prepTimeMinutes` | `number` | Total preparation time in minutes |
| `averageRating` | `number` | Computed average rating (1.0–5.0) |

### 6.3 Search Algorithm

1. **Title match:** Fuzzy match against recipe title (Levenshtein distance ≤ 2 or substring match).
2. **Ingredient match:** Substring match against normalized ingredient list. Score by number of matched ingredients.
3. **Combined ranking:** `relevanceScore = (titleMatchWeight * 0.6) + (ingredientMatchWeight * 0.4)`. Apply dietary/cuisine/difficulty filters as post-filter (AND logic). Sort by selected sort option or relevance by default.

### 6.4 Performance

- Search results must render within 500ms (P95) on a 4G mobile connection.
- Debounce input to prevent excessive re-renders.
- Virtualize result lists beyond 50 items using a windowing library.
- Lazy-load recipe card images with placeholder skeletons.

### 6.5 Accessibility

- All filter controls must be keyboard-navigable.
- Screen reader announcements for result count updates ("12 recipes found").
- Filter panel must trap focus when open on mobile (modal behavior).
- Minimum touch target size: 44x44px for mobile filter controls.
- Color contrast ratio ≥ 4.5:1 for all filter labels and result text.

## 7. Dependencies

| Dependency | Owner | Status | Risk |
|------------|-------|--------|------|
| Recipe data migration (add new fields) | Backend team | Not started | Medium — blocks filter functionality |
| Design mockups finalized | Design team | In progress | Low — 80% complete |
| Guest mode feature | Frontend team | In progress | Low — search works with existing auth context |
| RecipeCard component update | Frontend team | Not started | Low — isolated component change |

## 8. Rollout Plan

### Phase 1: Internal Testing (Week 1–2)
- Deploy to staging environment.
- QA regression testing on all breakpoints (mobile, tablet, desktop).
- Accessibility audit with screen reader and keyboard-only testing.
- Performance benchmarking against P95 latency target.

### Phase 2: Beta Release (Week 3)
- Enable for 20% of users via feature flag.
- Monitor search conversion metrics and error rates.
- Collect qualitative feedback via in-app survey.
- Fix critical issues identified during beta.

### Phase 3: General Availability (Week 4)
- Enable for 100% of users.
- Remove feature flag.
- Publish user-facing changelog entry.
- Monitor metrics for 2 weeks post-launch.

### Phase 4: Iteration (Week 5–8)
- Analyze search analytics for common queries with low conversion.
- Add autocomplete suggestions based on popular searches.
- Evaluate full-text search across recipe instructions for Phase 2.

## 9. Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Recipe data missing `ingredients` field for existing recipes | High | High | Run data backfill script; flag incomplete recipes for admin review |
| Search performance degrades with dataset growth | Medium | Medium | Implement client-side indexing; plan server-side search migration |
| Filter UX too complex for casual users | Medium | Medium | Progressive disclosure: show top 3 filters, "More filters" expandable |
| Mobile bottom sheet conflicts with browser gestures | Low | Medium | Test on iOS Safari and Android Chrome; use native-feel spring animation |
| Accessibility regression in existing components | Low | High | Run automated a11y tests in CI; manual screen reader testing |

## 10. Open Questions

- [ ] Should we support search by recipe tags in addition to ingredients and titles?
- [ ] Do we need an "Advanced Search" mode or keep everything unified?
- [ ] What is the maximum number of concurrent filters before UX degrades?
- [ ] Should dietary tags be self-reported by recipe authors or computed from ingredients?

## Appendix

### A. Competitive Analysis

| Feature | Kitchen Odyssey (Current) | AllRecipes | Tasty | Cookpad |
|---------|--------------------------|-----------|-------|---------|
| Ingredient search | No | Yes | Yes | Yes |
| Dietary filters | No | Yes (6 types) | Yes (4 types) | Limited |
| Sort options | No | 4 options | 3 options | 2 options |
| Mobile filter UX | N/A | Bottom sheet | Inline | Modal |
| Search autocomplete | No | Yes | Yes | No |

### B. User Research Highlights

- 8 of 10 interviewed users mentioned "search by ingredient" as their most-wanted feature.
- 6 of 10 users said they would use dietary filters at least weekly.
- Mobile users specifically requested a "less cluttered" filter experience.
- Users preferred seeing ingredient matches highlighted in results.

### C. Wireframe References

- Desktop search layout: [Figma link placeholder]
- Mobile bottom sheet filter: [Figma link placeholder]
- Empty state design: [Figma link placeholder]
