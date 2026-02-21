# Playwright Selectors Reference

Complete reference for locating elements in Playwright tests.

---

## Selector Types

### Role Selectors (Preferred)

Use ARIA roles for accessible, resilient selectors.

```typescript
// By role
page.getByRole('button', { name: 'Submit' })
page.getByRole('heading', { name: 'Welcome', level: 1 })
page.getByRole('link', { name: 'Sign up' })
page.getByRole('textbox', { name: 'Email' })
page.getByRole('checkbox', { name: 'Remember me' })
page.getByRole('combobox', { name: 'Country' })
page.getByRole('tab', { name: 'Settings' })
page.getByRole('navigation')
page.getByRole('dialog', { name: 'Confirm delete' })
page.getByRole('alert')
page.getByRole('listitem')
page.getByRole('row', { name: 'John Doe' })
page.getByRole('cell', { name: '42' })

// Common roles: button, link, heading, textbox, checkbox, radio,
// combobox, listbox, option, tab, tabpanel, dialog, alert, alertdialog,
// navigation, main, complementary, contentinfo, banner, form, list, listitem,
// table, row, cell, columnheader, rowheader, img, progressbar, slider,
// spinbutton, status, switch, tooltip, treegrid, tree, treeitem
```

### Text Selectors

```typescript
// Exact text match
page.getByText('Welcome back')

// Substring match
page.getByText('Welcome', { exact: false })

// Regular expression
page.getByText(/welcome/i)

// Specific element with text
page.locator('h1').filter({ hasText: 'Dashboard' })
```

### Label Selectors

```typescript
// By associated <label>
page.getByLabel('Email address')
page.getByLabel('Password')
page.getByLabel(/email/i)
```

### Placeholder Selectors

```typescript
page.getByPlaceholder('Search recipes...')
page.getByPlaceholder(/search/i)
```

### Alt Text Selectors

```typescript
page.getByAltText('Company logo')
page.getByAltText(/logo/i)
```

### Title Selectors

```typescript
page.getByTitle('Close dialog')
page.getByTitle(/close/i)
```

### Test ID Selectors

```typescript
// Matches data-testid attribute by default
page.getByTestId('recipe-card')
page.getByTestId('submit-button')

// Configure custom attribute in playwright.config.ts:
// use: { testIdAttribute: 'data-test' }
```

### CSS Selectors

```typescript
page.locator('.recipe-card')
page.locator('#main-content')
page.locator('div.card > h3')
page.locator('[data-status="active"]')
page.locator('input[type="email"]')
page.locator('button.primary:not(:disabled)')
page.locator('ul > li:first-child')
page.locator('.sidebar nav a')
```

### XPath Selectors

```typescript
page.locator('xpath=//button[contains(text(), "Submit")]')
page.locator('xpath=//div[@class="card"]//h3')
page.locator('xpath=//table//tr[position()>1]')
```

---

## Filtering and Chaining

### Filter by Text

```typescript
page.locator('.card').filter({ hasText: 'Pasta' })
page.locator('li').filter({ hasText: /vegetarian/i })

// Exclude text
page.locator('.card').filter({ hasNotText: 'Draft' })
```

### Filter by Child Element

```typescript
// Cards that contain a specific badge
page.locator('.card').filter({
  has: page.getByText('Featured')
})

// Rows that contain a specific button
page.locator('tr').filter({
  has: page.getByRole('button', { name: 'Edit' })
})

// Exclude cards with a delete button
page.locator('.card').filter({
  hasNot: page.getByRole('button', { name: 'Delete' })
})
```

### Chaining Locators

```typescript
// Narrow down step by step
const sidebar = page.locator('.sidebar')
const navLinks = sidebar.getByRole('link')
const activeLink = navLinks.filter({ hasText: 'Dashboard' })

// Within a specific section
page.locator('section.recipes').getByRole('heading', { name: 'Popular' })

// Form within a dialog
const dialog = page.getByRole('dialog')
dialog.getByLabel('Recipe name').fill('New Recipe')
dialog.getByRole('button', { name: 'Save' }).click()
```

### Nth Selectors

```typescript
// First, last, nth
page.locator('.card').first()
page.locator('.card').last()
page.locator('.card').nth(2)           // zero-indexed

// Nth from Playwright selector engine
page.locator('.card >> nth=0')
page.locator('.card >> nth=-1')        // last
```

---

## Advanced Selectors

### Shadow DOM

```typescript
// Piercing shadow DOM (auto-pierced by Playwright CSS engine)
page.locator('my-component').locator('button')

// Explicit CSS piercing
page.locator('css=my-component >> css=button')
```

### Frame Selectors

```typescript
// By name or URL
const frame = page.frameLocator('#payment-iframe')
frame.getByRole('textbox', { name: 'Card number' }).fill('4242...')

// Nested frames
page.frameLocator('#outer').frameLocator('#inner').getByRole('button')
```

### Combining Multiple Conditions

```typescript
// Locator that matches ALL conditions (AND)
page.getByRole('button', { name: 'Save' }).and(page.locator('.primary'))

// Locator that matches ANY condition (OR)
page.getByRole('button', { name: 'Save' }).or(page.getByRole('button', { name: 'Submit' }))
```

### Layout Selectors

```typescript
// Relative to another element
page.getByText('Username').locator('xpath=following-sibling::input')

// Near another element (experimental)
page.locator('button').near(page.getByText('Total'))
```

---

## Selector Decision Tree

Use this flowchart to choose the right selector strategy:

```
Is the element interactive (button, link, input)?
├─ YES → Does it have visible text/label?
│        ├─ YES → Use getByRole() with name
│        │        Example: getByRole('button', { name: 'Submit' })
│        └─ NO  → Does it have a label association?
│                 ├─ YES → Use getByLabel()
│                 └─ NO  → Does it have placeholder text?
│                          ├─ YES → Use getByPlaceholder()
│                          └─ NO  → Add data-testid, use getByTestId()
│
└─ NO → Is it a heading?
         ├─ YES → Use getByRole('heading', { name, level })
         └─ NO  → Does it have meaningful text?
                  ├─ YES → Use getByText()
                  └─ NO  → Is it an image?
                           ├─ YES → Use getByAltText()
                           └─ NO  → Does it have a title?
                                    ├─ YES → Use getByTitle()
                                    └─ NO  → Add data-testid, use getByTestId()
                                             Last resort: use CSS locator
```

### Priority Order

1. **`getByRole`** — Most resilient, mirrors accessibility tree
2. **`getByLabel`** — Great for form fields
3. **`getByPlaceholder`** — Fallback for unlabeled inputs
4. **`getByText`** — Good for non-interactive content
5. **`getByAltText`** — Images
6. **`getByTitle`** — Elements with title attribute
7. **`getByTestId`** — When semantic selectors aren't possible
8. **CSS/XPath** — Last resort only

---

## Best Practices

### Prefer Semantic Selectors

```typescript
// GOOD — resilient to DOM changes
page.getByRole('button', { name: 'Add to cart' })

// BAD — breaks if class name changes
page.locator('.btn-primary.add-cart-btn')

// BAD — breaks if DOM structure changes
page.locator('div > div:nth-child(3) > button')
```

### Use Exact Matching When Appropriate

```typescript
// Matches "Log in" but not "Log in with Google"
page.getByRole('button', { name: 'Log in', exact: true })

// Regex for flexible matching
page.getByRole('button', { name: /log\s*in/i })
```

### Scope Selectors to Avoid Ambiguity

```typescript
// Scope to a section when multiple similar elements exist
const loginForm = page.locator('[data-testid="login-form"]')
await loginForm.getByLabel('Email').fill('user@example.com')
await loginForm.getByRole('button', { name: 'Sign in' }).click()
```

### Handle Dynamic Content

```typescript
// Wait for element to appear
await page.getByRole('alert').waitFor()

// Wait for specific text
await page.getByText('Recipe saved!').waitFor({ state: 'visible' })

// Wait for element to disappear
await page.getByRole('progressbar').waitFor({ state: 'hidden' })
```

### Avoid Fragile Selectors

```typescript
// AVOID: positional selectors
page.locator('table tr:nth-child(5) td:nth-child(2)')

// PREFER: content-based filtering
page.getByRole('row', { name: 'Pasta Recipe' }).getByRole('cell').nth(1)

// AVOID: auto-generated class names
page.locator('.css-1a2b3c4')

// PREFER: semantic or test-id selectors
page.getByTestId('recipe-title')
```
