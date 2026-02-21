# WCAG 2.2 Accessibility Checklist

Practical accessibility checklist for web developers. Organized by WCAG principle with code examples, testing methods, and common fixes.

---

## 1. Perceivable

Content must be presentable to users in ways they can perceive.

### 1.1 Text Alternatives (Level A)

**What to check:** Every non-text element (images, icons, charts) has a text alternative.

**How to check:**
- Inspect all `<img>` tags for `alt` attributes
- Check icon buttons for `aria-label` or screen-reader-only text
- Verify decorative images use `alt=""`

**Compliant examples:**

```html
<!-- Informative image -->
<img src="/recipe.jpg" alt="Thai green curry with jasmine rice in a white bowl" />

<!-- Decorative image (no alt needed) -->
<img src="/divider.svg" alt="" role="presentation" />

<!-- Icon button -->
<button aria-label="Delete recipe">
  <svg aria-hidden="true">...</svg>
</button>

<!-- Icon with visible label (no aria-label needed) -->
<button>
  <svg aria-hidden="true">...</svg>
  <span>Delete</span>
</button>
```

**Common violations:**
- Missing `alt` on `<img>` tags
- Icon-only buttons without `aria-label`
- `alt="image"` or `alt="photo"` — describe the content, not the format

### 1.2 Time-Based Media (Level A/AA)

**What to check:** Audio and video content has captions and/or transcripts.

**How to check:**
- Verify `<video>` elements include `<track>` for captions
- Check for transcript links near media elements

```html
<video controls>
  <source src="/demo.mp4" type="video/mp4" />
  <track kind="captions" src="/demo-captions.vtt" srclang="en" label="English" default />
</video>
```

### 1.3 Adaptable — Info and Relationships (Level A)

**What to check:** Semantic HTML conveys structure and relationships.

**How to check:**
- Headings use `<h1>`–`<h6>` in logical order
- Lists use `<ul>`, `<ol>`, `<li>`
- Tables use `<th>` with `scope` attributes
- Form inputs have associated `<label>` elements

```html
<!-- Form with proper labels -->
<div>
  <label for="recipe-name">Recipe Name</label>
  <input id="recipe-name" type="text" />
</div>

<!-- Table with proper headers -->
<table>
  <thead>
    <tr>
      <th scope="col">Ingredient</th>
      <th scope="col">Amount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Coconut milk</td>
      <td>400ml</td>
    </tr>
  </tbody>
</table>
```

**Common violations:**
- Using `<div>` or `<span>` where semantic elements exist
- Inputs without associated labels (placeholder is NOT a label)
- Heading hierarchy skips (H2 → H4)

### 1.4 Distinguishable — Color Contrast (Level AA)

**What to check:**
- **Normal text** (< 18pt / < 14pt bold): contrast ratio >= 4.5:1
- **Large text** (>= 18pt / >= 14pt bold): contrast ratio >= 3:1
- **UI components** (borders, icons, focus indicators): contrast ratio >= 3:1

**How to check:**
- Browser DevTools → Accessibility panel → Contrast ratio
- Use the `contrast-checker.py` script from this skill
- Chrome Lighthouse accessibility audit

**Common violations:**
- Light gray text on white: `#999` on `#fff` = 2.85:1 (FAIL)
- Placeholder text too light: ensure >= 4.5:1
- Disabled states still need 3:1 against background

### 1.4 Distinguishable — Non-Text Contrast (Level AA)

**What to check:** UI components and graphical objects have >= 3:1 contrast against adjacent colors.

```html
<!-- Input border must contrast with background -->
<input class="border border-gray-400 bg-white ..." />
<!-- gray-400 (#9ca3af) on white = 3.04:1 — passes for UI components -->

<!-- Focus ring must be visible -->
<input class="... focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2" />
```

### 1.4 Distinguishable — Resize Text (Level AA)

**What to check:** Text can scale to 200% without loss of content.

**How to check:**
- Browser zoom to 200% — verify no content is clipped or overlapping
- Verify layout adapts (use `rem`/`em` units, not fixed `px` for text)

---

## 2. Operable

User interface components must be operable by all users.

### 2.1 Keyboard Accessible (Level A)

**What to check:** All interactive elements are reachable and operable with keyboard alone.

**How to check:**
- Tab through the entire page — every interactive element should receive focus
- Enter/Space activates buttons and links
- Arrow keys navigate within composite widgets (tabs, menus, radio groups)
- Escape closes modals and popups
- No keyboard traps (user can always Tab away)

**Keyboard navigation patterns:**

```jsx
// React: Tab panel with arrow key navigation
function TabList({ tabs, activeTab, onSelect }) {
  const handleKeyDown = (e, index) => {
    let newIndex;
    if (e.key === 'ArrowRight') {
      newIndex = (index + 1) % tabs.length;
    } else if (e.key === 'ArrowLeft') {
      newIndex = (index - 1 + tabs.length) % tabs.length;
    } else if (e.key === 'Home') {
      newIndex = 0;
    } else if (e.key === 'End') {
      newIndex = tabs.length - 1;
    } else {
      return;
    }
    e.preventDefault();
    onSelect(newIndex);
  };

  return (
    <div role="tablist">
      {tabs.map((tab, i) => (
        <button
          key={tab.id}
          role="tab"
          aria-selected={i === activeTab}
          tabIndex={i === activeTab ? 0 : -1}
          onKeyDown={(e) => handleKeyDown(e, i)}
          onClick={() => onSelect(i)}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}
```

**Common violations:**
- Custom buttons using `<div onClick>` without `tabIndex`, `role`, or `onKeyDown`
- Modals that don't trap focus
- Dropdown menus that can't be navigated with arrow keys

### 2.1 No Keyboard Trap (Level A)

**What to check:** Focus can always move away from any component.

**Modal focus trap (correct implementation):**

```jsx
import { useEffect, useRef } from 'react';

function Modal({ isOpen, onClose, children }) {
  const modalRef = useRef(null);

  useEffect(() => {
    if (!isOpen) return;
    const modal = modalRef.current;
    const focusableEls = modal.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstEl = focusableEls[0];
    const lastEl = focusableEls[focusableEls.length - 1];

    firstEl?.focus();

    function trapFocus(e) {
      if (e.key === 'Tab') {
        if (e.shiftKey && document.activeElement === firstEl) {
          e.preventDefault();
          lastEl.focus();
        } else if (!e.shiftKey && document.activeElement === lastEl) {
          e.preventDefault();
          firstEl.focus();
        }
      }
      if (e.key === 'Escape') onClose();
    }

    modal.addEventListener('keydown', trapFocus);
    return () => modal.removeEventListener('keydown', trapFocus);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div role="dialog" aria-modal="true" ref={modalRef}>
      {children}
    </div>
  );
}
```

### 2.4 Focus Visible (Level AA)

**What to check:** All interactive elements show a visible focus indicator.

```css
/* Never do this globally */
/* *:focus { outline: none; } */

/* Do this instead — custom focus style */
*:focus-visible {
  outline: 2px solid #4f46e5;
  outline-offset: 2px;
}

/* Tailwind equivalent */
/* focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2 */
```

### 2.4 Page Titled (Level A)

**What to check:** Every page has a descriptive `<title>`.

```jsx
// React with document title
useEffect(() => {
  document.title = 'Thai Green Curry — Kitchen Odyssey';
}, []);
```

### 2.4 Focus Order (Level A)

**What to check:** Focus order follows a logical reading sequence.

**How to check:** Tab through the page — focus should move top-to-bottom, left-to-right (for LTR languages), matching visual layout.

**Common violations:**
- CSS `order` or `flex-direction: row-reverse` changes visual order but not DOM/focus order
- Dynamically-inserted content placed at the wrong DOM position

### 2.5 Target Size (Level AA — New in WCAG 2.2)

**What to check:** Interactive targets are at least 24x24 CSS pixels, with exceptions for inline text links.

```html
<!-- Minimum touch target -->
<button class="min-h-[44px] min-w-[44px] p-2">
  <svg class="h-5 w-5">...</svg>
</button>
```

---

## 3. Understandable

Information and UI operation must be understandable.

### 3.1 Language of Page (Level A)

**What to check:** The `<html>` element declares the page language.

```html
<html lang="en">
```

### 3.2 Labels or Instructions (Level A)

**What to check:** Form fields have visible labels and required fields are identified.

```html
<label for="servings">
  Number of Servings <span class="text-red-500" aria-hidden="true">*</span>
  <span class="sr-only">(required)</span>
</label>
<input id="servings" type="number" required aria-required="true" min="1" />
```

### 3.3 Error Identification (Level A)

**What to check:** Errors are clearly identified and described in text (not just color).

```jsx
function FormField({ label, error, id, ...props }) {
  const errorId = `${id}-error`;
  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <input
        id={id}
        aria-invalid={!!error}
        aria-describedby={error ? errorId : undefined}
        {...props}
      />
      {error && (
        <p id={errorId} role="alert" className="mt-1 text-sm text-red-600">
          {error}
        </p>
      )}
    </div>
  );
}
```

### 3.3 Error Suggestion (Level AA)

**What to check:** Suggestions for correction are provided when input errors are detected.

```html
<p id="email-error" role="alert" class="text-sm text-red-600">
  Please enter a valid email address (e.g., user@example.com).
</p>
```

### 3.2 Consistent Navigation (Level AA)

**What to check:** Navigation appears in the same relative order across pages.

### 3.2 On Input (Level A)

**What to check:** Changing a form control does not cause an unexpected context change (page navigation, modal opening, focus shift) unless the user is warned.

---

## 4. Robust

Content must be robust enough to work with current and future technologies.

### 4.1 Parsing / Valid HTML (Level A)

**What to check:**
- No duplicate `id` attributes
- All elements are properly nested and closed
- ARIA attributes use valid values

**How to check:**
- W3C Validator: https://validator.w3.org/
- `axe-core` browser extension
- ESLint `eslint-plugin-jsx-a11y`

### 4.1 Name, Role, Value (Level A)

**What to check:** Custom components expose correct ARIA semantics.

```jsx
// Custom toggle/switch
function Toggle({ checked, onChange, label }) {
  return (
    <button
      role="switch"
      aria-checked={checked}
      aria-label={label}
      onClick={() => onChange(!checked)}
      className={`relative h-6 w-11 rounded-full transition-colors ${
        checked ? 'bg-indigo-600' : 'bg-gray-300'
      }`}
    >
      <span
        className={`block h-5 w-5 rounded-full bg-white shadow transition-transform ${
          checked ? 'translate-x-5' : 'translate-x-0.5'
        }`}
      />
    </button>
  );
}
```

### 4.1 Status Messages (Level AA)

**What to check:** Status messages (search results count, form submission confirmation, loading states) are announced to screen readers without receiving focus.

```html
<!-- Live region for dynamic updates -->
<div aria-live="polite" aria-atomic="true" class="sr-only">
  12 recipes found matching "chicken"
</div>

<!-- Toast/notification -->
<div role="status" aria-live="polite">
  Recipe saved successfully.
</div>

<!-- Error alert -->
<div role="alert">
  Failed to save recipe. Please try again.
</div>
```

---

## Screen Reader Patterns

### Visually Hidden (Screen Reader Only) Text

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

Tailwind: `class="sr-only"`

### Skip Navigation Link

```html
<a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:rounded focus:bg-indigo-600 focus:px-4 focus:py-2 focus:text-white">
  Skip to main content
</a>
<!-- ... header/nav ... -->
<main id="main-content" tabindex="-1">
  <!-- Main content -->
</main>
```

### Announcing Dynamic Content

```jsx
function SearchResults({ results, query }) {
  return (
    <>
      {/* Announced to screen readers when results change */}
      <div role="status" aria-live="polite" className="sr-only">
        {results.length} recipes found for "{query}"
      </div>

      <h2>{results.length} Results</h2>
      <ul>
        {results.map((r) => (
          <li key={r.id}>{r.title}</li>
        ))}
      </ul>
    </>
  );
}
```

---

## Focus Management Patterns

### Return Focus After Modal Close

```jsx
function useModal() {
  const [isOpen, setIsOpen] = useState(false);
  const triggerRef = useRef(null);

  const open = () => setIsOpen(true);
  const close = () => {
    setIsOpen(false);
    triggerRef.current?.focus();
  };

  return { isOpen, open, close, triggerRef };
}

function App() {
  const { isOpen, open, close, triggerRef } = useModal();
  return (
    <>
      <button ref={triggerRef} onClick={open}>
        Open Settings
      </button>
      {isOpen && <Modal onClose={close}>...</Modal>}
    </>
  );
}
```

### Focus on Route Change (SPA)

```jsx
import { useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';

function FocusOnRouteChange() {
  const location = useLocation();
  const mainRef = useRef(null);

  useEffect(() => {
    mainRef.current?.focus();
  }, [location.pathname]);

  return <main ref={mainRef} tabIndex={-1}>{/* page content */}</main>;
}
```

---

## Testing Tools

| Tool | Type | What It Catches |
|------|------|-----------------|
| **axe DevTools** | Browser extension | Automated WCAG violations |
| **Lighthouse** | Built into Chrome | Accessibility scoring |
| **eslint-plugin-jsx-a11y** | Linter | React-specific a11y issues |
| **NVDA** / **VoiceOver** | Screen reader | Real-world screen reader behavior |
| **Keyboard only** | Manual testing | Focus order, keyboard traps, visibility |
| **Color contrast analyzers** | Manual/automated | Contrast ratio compliance |
| **WAVE** | Browser extension | Visual overlay of a11y issues |

### Quick Manual Test (5-minute check)

1. **Tab through page** — Can you reach and operate every interactive element?
2. **Screen reader** — Turn on VoiceOver (Mac) or NVDA (Windows), navigate the page. Does it make sense?
3. **Zoom to 200%** — Is content still readable without horizontal scrolling?
4. **Check forms** — Do all inputs have labels? Are errors described in text?
5. **Check images** — Do informative images have meaningful alt text?

---

## Checklist Summary

### Level A (Minimum)

- [ ] All images have appropriate `alt` text
- [ ] Videos have captions
- [ ] Semantic HTML used (headings, lists, tables, landmarks)
- [ ] Page has `<html lang="...">`
- [ ] All form inputs have labels
- [ ] No keyboard traps
- [ ] All functionality keyboard accessible
- [ ] Focus order is logical
- [ ] Page has descriptive `<title>`
- [ ] Errors identified in text (not just color)
- [ ] No auto-playing media
- [ ] Custom controls have name, role, value

### Level AA (Standard Compliance)

- [ ] Color contrast >= 4.5:1 (normal text) / >= 3:1 (large text)
- [ ] Non-text contrast >= 3:1 (UI components)
- [ ] Text resizable to 200% without loss
- [ ] Focus indicator visible on all interactive elements
- [ ] Consistent navigation across pages
- [ ] Error suggestions provided
- [ ] Status messages announced via `aria-live` or `role`
- [ ] Target size >= 24x24 CSS pixels
- [ ] Skip navigation link present
- [ ] Heading hierarchy logical (no skipped levels)
