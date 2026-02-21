# Web Testing Patterns

Patterns and best practices for Playwright-based web testing.

---

## Page Object Model (POM)

Encapsulate page interactions in reusable classes.

```typescript
// pages/LoginPage.ts
import { type Page, type Locator } from '@playwright/test'

export class LoginPage {
  readonly page: Page
  readonly emailInput: Locator
  readonly passwordInput: Locator
  readonly submitButton: Locator
  readonly errorMessage: Locator

  constructor(page: Page) {
    this.page = page
    this.emailInput = page.getByLabel('Email')
    this.passwordInput = page.getByLabel('Password')
    this.submitButton = page.getByRole('button', { name: 'Sign in' })
    this.errorMessage = page.getByRole('alert')
  }

  async goto() {
    await this.page.goto('/login')
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email)
    await this.passwordInput.fill(password)
    await this.submitButton.click()
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toContainText(message)
  }
}
```

```typescript
// Usage in tests
import { LoginPage } from './pages/LoginPage'

test('successful login', async ({ page }) => {
  const loginPage = new LoginPage(page)
  await loginPage.goto()
  await loginPage.login('user@test.com', 'password123')
  await expect(page).toHaveURL('/dashboard')
})
```

---

## Fixtures and Test Setup

### Custom Fixtures

```typescript
// fixtures.ts
import { test as base } from '@playwright/test'
import { LoginPage } from './pages/LoginPage'
import { RecipePage } from './pages/RecipePage'

type Fixtures = {
  loginPage: LoginPage
  recipePage: RecipePage
}

export const test = base.extend<Fixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page)
    await use(loginPage)
  },
  recipePage: async ({ page }, use) => {
    const recipePage = new RecipePage(page)
    await use(recipePage)
  },
})

export { expect } from '@playwright/test'
```

### Before/After Hooks

```typescript
test.describe('Recipe Management', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/recipes')
    await page.waitForLoadState('networkidle')
  })

  test.afterEach(async ({ page }) => {
    // Cleanup: delete test data via API
    await page.request.delete('/api/test/cleanup')
  })

  test('creates a recipe', async ({ page }) => {
    // test implementation
  })
})
```

---

## Authentication State Reuse

Avoid logging in for every test by saving and reusing auth state.

### Global Setup

```typescript
// global-setup.ts
import { chromium, type FullConfig } from '@playwright/test'

async function globalSetup(config: FullConfig) {
  const browser = await chromium.launch()
  const page = await browser.newPage()

  await page.goto('http://localhost:3000/login')
  await page.getByLabel('Email').fill('admin@test.com')
  await page.getByLabel('Password').fill('password123')
  await page.getByRole('button', { name: 'Sign in' }).click()
  await page.waitForURL('/dashboard')

  await page.context().storageState({ path: '.auth/admin.json' })
  await browser.close()
}

export default globalSetup
```

### Use in Config

```typescript
// playwright.config.ts
export default defineConfig({
  globalSetup: require.resolve('./global-setup'),
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'authenticated',
      use: { storageState: '.auth/admin.json' },
      dependencies: ['setup'],
    },
    {
      name: 'unauthenticated',
      testMatch: /.*\.unauth\.spec\.ts/,
      // No storageState — fresh context
    },
  ],
})
```

---

## API Mocking with Route Interception

### Mock API Responses

```typescript
test('displays recipes from API', async ({ page }) => {
  await page.route('**/api/recipes', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { id: 1, title: 'Mock Pasta', time: 30 },
        { id: 2, title: 'Mock Salad', time: 15 },
      ]),
    })
  })

  await page.goto('/recipes')
  await expect(page.getByText('Mock Pasta')).toBeVisible()
  await expect(page.getByText('Mock Salad')).toBeVisible()
})
```

### Simulate Error States

```typescript
test('shows error when API fails', async ({ page }) => {
  await page.route('**/api/recipes', (route) =>
    route.fulfill({ status: 500, body: 'Internal Server Error' })
  )

  await page.goto('/recipes')
  await expect(page.getByText('Failed to load recipes')).toBeVisible()
})
```

### Modify Real Responses

```typescript
test('augments real API data', async ({ page }) => {
  await page.route('**/api/recipes', async (route) => {
    const response = await route.fetch()
    const json = await response.json()
    json.push({ id: 999, title: 'Injected Recipe', time: 5 })
    await route.fulfill({ response, json })
  })

  await page.goto('/recipes')
  await expect(page.getByText('Injected Recipe')).toBeVisible()
})
```

---

## Visual Regression Testing

### Screenshot Comparisons

```typescript
test('home page visual', async ({ page }) => {
  await page.goto('/')
  await expect(page).toHaveScreenshot('home-page.png', {
    maxDiffPixelRatio: 0.01,
  })
})

test('recipe card visual', async ({ page }) => {
  await page.goto('/recipes')
  const card = page.locator('.recipe-card').first()
  await expect(card).toHaveScreenshot('recipe-card.png')
})
```

### Update Snapshots

```bash
# Generate or update baseline screenshots
npx playwright test --update-snapshots
```

---

## Accessibility Testing with axe-core

```typescript
import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

test('home page has no a11y violations', async ({ page }) => {
  await page.goto('/')

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze()

  expect(results.violations).toEqual([])
})

test('form has no a11y violations', async ({ page }) => {
  await page.goto('/recipes/new')

  const results = await new AxeBuilder({ page })
    .include('form')
    .exclude('.third-party-widget')
    .analyze()

  expect(results.violations).toEqual([])
})
```

---

## Mobile Viewport Testing

```typescript
// In playwright.config.ts
import { devices } from '@playwright/test'

export default defineConfig({
  projects: [
    { name: 'Desktop Chrome', use: { ...devices['Desktop Chrome'] } },
    { name: 'Mobile Safari', use: { ...devices['iPhone 14'] } },
    { name: 'Mobile Chrome', use: { ...devices['Pixel 7'] } },
    { name: 'Tablet', use: { ...devices['iPad Pro 11'] } },
  ],
})
```

```typescript
// In tests
test('mobile menu opens on hamburger click', async ({ page, isMobile }) => {
  await page.goto('/')

  if (isMobile) {
    await page.getByRole('button', { name: 'Menu' }).click()
    await expect(page.getByRole('navigation')).toBeVisible()
  } else {
    await expect(page.getByRole('navigation')).toBeVisible()
  }
})
```

---

## Performance Assertions

```typescript
test('page loads within performance budget', async ({ page }) => {
  const startTime = Date.now()
  await page.goto('/')
  await page.waitForLoadState('networkidle')
  const loadTime = Date.now() - startTime

  expect(loadTime).toBeLessThan(3000) // 3s budget
})

test('no large layout shifts', async ({ page }) => {
  await page.goto('/')

  const cls = await page.evaluate(() => {
    return new Promise<number>((resolve) => {
      let clsValue = 0
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (!(entry as any).hadRecentInput) {
            clsValue += (entry as any).value
          }
        }
      })
      observer.observe({ type: 'layout-shift', buffered: true })
      setTimeout(() => {
        observer.disconnect()
        resolve(clsValue)
      }, 3000)
    })
  })

  expect(cls).toBeLessThan(0.1)
})
```

---

## Retry Strategies

```typescript
// playwright.config.ts
export default defineConfig({
  retries: process.env.CI ? 2 : 0,
  expect: {
    timeout: 5000,
  },
  use: {
    actionTimeout: 10000,
    navigationTimeout: 30000,
  },
})
```

```typescript
// Soft assertions — continue test after failure
test('multiple checks', async ({ page }) => {
  await page.goto('/recipes')

  await expect.soft(page.getByText('Pasta')).toBeVisible()
  await expect.soft(page.getByText('Salad')).toBeVisible()
  await expect.soft(page.getByText('Soup')).toBeVisible()
  // Test reports all failures, not just the first
})
```

---

## Parallel Test Execution

```typescript
// playwright.config.ts
export default defineConfig({
  fullyParallel: true,
  workers: process.env.CI ? 4 : undefined,
})
```

```typescript
// Serial execution when tests share state
test.describe.serial('Order flow', () => {
  test('add item to cart', async ({ page }) => { /* ... */ })
  test('proceed to checkout', async ({ page }) => { /* ... */ })
  test('confirm payment', async ({ page }) => { /* ... */ })
})
```

---

## Test Data Management

```typescript
// test-data/recipes.ts
export const testRecipes = {
  pasta: {
    title: 'Test Pasta Recipe',
    description: 'A test recipe for E2E testing',
    ingredients: ['pasta', 'sauce', 'cheese'],
    time: 30,
  },
  salad: {
    title: 'Test Salad Recipe',
    description: 'Fresh test salad',
    ingredients: ['lettuce', 'tomato', 'dressing'],
    time: 10,
  },
}

// Generate unique test data
export function uniqueRecipe(base = testRecipes.pasta) {
  return {
    ...base,
    title: `${base.title} ${Date.now()}`,
  }
}
```

```typescript
// Seed via API before tests
test.beforeEach(async ({ request }) => {
  await request.post('/api/test/seed', {
    data: { recipes: [testRecipes.pasta, testRecipes.salad] },
  })
})
```

---

## CI Integration Patterns

### GitHub Actions

```yaml
name: Playwright Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

### Sharding for Large Test Suites

```yaml
jobs:
  test:
    strategy:
      matrix:
        shard: [1/4, 2/4, 3/4, 4/4]
    steps:
      - run: npx playwright test --shard=${{ matrix.shard }}
```

### Running Against Preview Deployments

```yaml
jobs:
  test:
    steps:
      - run: npx playwright test
        env:
          BASE_URL: ${{ github.event.deployment_status.target_url }}
```
