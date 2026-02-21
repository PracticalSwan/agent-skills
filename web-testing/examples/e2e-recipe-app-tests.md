# E2E Test Suite Example: Kitchen Odyssey Recipe App

Complete Playwright test suite for a recipe application with authentication, CRUD operations, search, and admin features.

---

## Project Structure

```
tests/
  pages/
    LoginPage.ts
    HomePage.ts
    RecipeCreatePage.ts
    RecipeDetailPage.ts
    SearchPage.ts
    ProfilePage.ts
    AdminPage.ts
  fixtures/
    auth.ts
    test-data.ts
  auth.setup.ts
  login.spec.ts
  recipe-create.spec.ts
  recipe-search.spec.ts
  recipe-detail.spec.ts
  profile.spec.ts
  admin.spec.ts
playwright.config.ts
.github/workflows/playwright.yml
```

---

## Page Object Classes

### LoginPage.ts

```typescript
import { type Page, type Locator, expect } from '@playwright/test'

export class LoginPage {
  readonly page: Page
  readonly emailInput: Locator
  readonly passwordInput: Locator
  readonly signInButton: Locator
  readonly signUpLink: Locator
  readonly errorAlert: Locator
  readonly guestButton: Locator

  constructor(page: Page) {
    this.page = page
    this.emailInput = page.getByLabel('Email')
    this.passwordInput = page.getByLabel('Password')
    this.signInButton = page.getByRole('button', { name: 'Sign In' })
    this.signUpLink = page.getByRole('link', { name: 'Sign Up' })
    this.errorAlert = page.getByRole('alert')
    this.guestButton = page.getByRole('button', { name: /guest/i })
  }

  async goto() {
    await this.page.goto('/login')
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email)
    await this.passwordInput.fill(password)
    await this.signInButton.click()
  }

  async expectError(message: string) {
    await expect(this.errorAlert).toContainText(message)
  }

  async expectRedirectToDashboard() {
    await expect(this.page).toHaveURL('/')
  }
}
```

### HomePage.ts

```typescript
import { type Page, type Locator, expect } from '@playwright/test'

export class HomePage {
  readonly page: Page
  readonly heading: Locator
  readonly recipeCards: Locator
  readonly searchInput: Locator
  readonly createButton: Locator
  readonly categoryTabs: Locator

  constructor(page: Page) {
    this.page = page
    this.heading = page.getByRole('heading', { level: 1 })
    this.recipeCards = page.locator('[data-testid="recipe-card"]')
    this.searchInput = page.getByPlaceholder(/search/i)
    this.createButton = page.getByRole('link', { name: /create/i })
    this.categoryTabs = page.getByRole('tablist')
  }

  async goto() {
    await this.page.goto('/')
  }

  async expectRecipeCount(count: number) {
    await expect(this.recipeCards).toHaveCount(count)
  }

  async clickRecipe(title: string) {
    await this.recipeCards.filter({ hasText: title }).click()
  }

  async searchRecipes(query: string) {
    await this.searchInput.fill(query)
    await this.searchInput.press('Enter')
  }
}
```

### RecipeCreatePage.ts

```typescript
import { type Page, type Locator, expect } from '@playwright/test'

export class RecipeCreatePage {
  readonly page: Page
  readonly titleInput: Locator
  readonly descriptionInput: Locator
  readonly ingredientsInput: Locator
  readonly instructionsInput: Locator
  readonly timeInput: Locator
  readonly difficultySelect: Locator
  readonly submitButton: Locator
  readonly successMessage: Locator

  constructor(page: Page) {
    this.page = page
    this.titleInput = page.getByLabel('Title')
    this.descriptionInput = page.getByLabel('Description')
    this.ingredientsInput = page.getByLabel('Ingredients')
    this.instructionsInput = page.getByLabel('Instructions')
    this.timeInput = page.getByLabel(/time|duration/i)
    this.difficultySelect = page.getByLabel('Difficulty')
    this.submitButton = page.getByRole('button', { name: /create|submit|save/i })
    this.successMessage = page.getByText(/created|saved/i)
  }

  async goto() {
    await this.page.goto('/recipes/create')
  }

  async fillRecipe(recipe: {
    title: string
    description: string
    ingredients: string
    instructions: string
    time?: string
    difficulty?: string
  }) {
    await this.titleInput.fill(recipe.title)
    await this.descriptionInput.fill(recipe.description)
    await this.ingredientsInput.fill(recipe.ingredients)
    await this.instructionsInput.fill(recipe.instructions)
    if (recipe.time) await this.timeInput.fill(recipe.time)
    if (recipe.difficulty) {
      await this.difficultySelect.selectOption(recipe.difficulty)
    }
  }

  async submit() {
    await this.submitButton.click()
  }

  async expectSuccess() {
    await expect(this.successMessage).toBeVisible()
  }
}
```

### RecipeDetailPage.ts

```typescript
import { type Page, type Locator, expect } from '@playwright/test'

export class RecipeDetailPage {
  readonly page: Page
  readonly title: Locator
  readonly description: Locator
  readonly ingredients: Locator
  readonly instructions: Locator
  readonly authorName: Locator
  readonly editButton: Locator
  readonly deleteButton: Locator
  readonly backButton: Locator

  constructor(page: Page) {
    this.page = page
    this.title = page.getByRole('heading', { level: 1 })
    this.description = page.locator('[data-testid="recipe-description"]')
    this.ingredients = page.locator('[data-testid="ingredients"]')
    this.instructions = page.locator('[data-testid="instructions"]')
    this.authorName = page.locator('[data-testid="author"]')
    this.editButton = page.getByRole('button', { name: /edit/i })
    this.deleteButton = page.getByRole('button', { name: /delete/i })
    this.backButton = page.getByRole('link', { name: /back/i })
  }

  async goto(recipeId: string) {
    await this.page.goto(`/recipes/${recipeId}`)
  }

  async expectTitle(title: string) {
    await expect(this.title).toHaveText(title)
  }

  async deleteRecipe() {
    await this.deleteButton.click()
    const confirmDialog = this.page.getByRole('dialog')
    await confirmDialog.getByRole('button', { name: /confirm|yes|delete/i }).click()
  }
}
```

### SearchPage.ts

```typescript
import { type Page, type Locator, expect } from '@playwright/test'

export class SearchPage {
  readonly page: Page
  readonly searchInput: Locator
  readonly results: Locator
  readonly resultCount: Locator
  readonly noResults: Locator
  readonly filters: Locator

  constructor(page: Page) {
    this.page = page
    this.searchInput = page.getByRole('searchbox')
    this.results = page.locator('[data-testid="search-result"]')
    this.resultCount = page.locator('[data-testid="result-count"]')
    this.noResults = page.getByText(/no results|no recipes found/i)
    this.filters = page.locator('[data-testid="search-filters"]')
  }

  async goto() {
    await this.page.goto('/search')
  }

  async search(query: string) {
    await this.searchInput.fill(query)
    await this.searchInput.press('Enter')
    await this.page.waitForLoadState('networkidle')
  }

  async expectResultCount(count: number) {
    await expect(this.results).toHaveCount(count)
  }

  async expectNoResults() {
    await expect(this.noResults).toBeVisible()
  }
}
```

### ProfilePage.ts

```typescript
import { type Page, type Locator, expect } from '@playwright/test'

export class ProfilePage {
  readonly page: Page
  readonly displayName: Locator
  readonly email: Locator
  readonly recipeCount: Locator
  readonly userRecipes: Locator
  readonly editProfileButton: Locator

  constructor(page: Page) {
    this.page = page
    this.displayName = page.getByRole('heading', { level: 1 })
    this.email = page.locator('[data-testid="user-email"]')
    this.recipeCount = page.locator('[data-testid="recipe-count"]')
    this.userRecipes = page.locator('[data-testid="user-recipe"]')
    this.editProfileButton = page.getByRole('button', { name: /edit profile/i })
  }

  async goto() {
    await this.page.goto('/profile')
  }

  async expectDisplayName(name: string) {
    await expect(this.displayName).toContainText(name)
  }
}
```

### AdminPage.ts

```typescript
import { type Page, type Locator, expect } from '@playwright/test'

export class AdminPage {
  readonly page: Page
  readonly userTable: Locator
  readonly recipeTable: Locator
  readonly statsCards: Locator
  readonly tabs: Locator

  constructor(page: Page) {
    this.page = page
    this.userTable = page.locator('[data-testid="user-table"]')
    this.recipeTable = page.locator('[data-testid="recipe-table"]')
    this.statsCards = page.locator('[data-testid="stat-card"]')
    this.tabs = page.getByRole('tablist')
  }

  async goto() {
    await this.page.goto('/admin')
  }

  async switchTab(name: string) {
    await this.tabs.getByRole('tab', { name }).click()
  }

  async expectStatCount(min: number) {
    const count = await this.statsCards.count()
    expect(count).toBeGreaterThanOrEqual(min)
  }
}
```

---

## Shared Fixtures

### fixtures/auth.ts

```typescript
import { test as base } from '@playwright/test'
import { LoginPage } from '../pages/LoginPage'
import { HomePage } from '../pages/HomePage'
import { RecipeCreatePage } from '../pages/RecipeCreatePage'
import { RecipeDetailPage } from '../pages/RecipeDetailPage'
import { SearchPage } from '../pages/SearchPage'
import { ProfilePage } from '../pages/ProfilePage'
import { AdminPage } from '../pages/AdminPage'

type Pages = {
  loginPage: LoginPage
  homePage: HomePage
  recipeCreatePage: RecipeCreatePage
  recipeDetailPage: RecipeDetailPage
  searchPage: SearchPage
  profilePage: ProfilePage
  adminPage: AdminPage
}

export const test = base.extend<Pages>({
  loginPage: async ({ page }, use) => use(new LoginPage(page)),
  homePage: async ({ page }, use) => use(new HomePage(page)),
  recipeCreatePage: async ({ page }, use) => use(new RecipeCreatePage(page)),
  recipeDetailPage: async ({ page }, use) => use(new RecipeDetailPage(page)),
  searchPage: async ({ page }, use) => use(new SearchPage(page)),
  profilePage: async ({ page }, use) => use(new ProfilePage(page)),
  adminPage: async ({ page }, use) => use(new AdminPage(page)),
})

export { expect } from '@playwright/test'
```

### fixtures/test-data.ts

```typescript
export const users = {
  regular: {
    email: 'testuser@kitchen-odyssey.com',
    password: 'TestPass123!',
    name: 'Test User',
  },
  admin: {
    email: 'admin@kitchen-odyssey.com',
    password: 'AdminPass123!',
    name: 'Admin User',
  },
}

export const recipes = {
  pasta: {
    title: `Test Pasta ${Date.now()}`,
    description: 'Creamy garlic pasta for E2E testing',
    ingredients: '200g pasta\n2 cloves garlic\n100ml cream\nParmesan',
    instructions: '1. Boil pasta\n2. Saute garlic\n3. Add cream\n4. Toss and serve',
    time: '25',
    difficulty: 'Easy',
  },
  salad: {
    title: `Test Salad ${Date.now()}`,
    description: 'Fresh garden salad for E2E testing',
    ingredients: 'Lettuce\nTomatoes\nCucumber\nOlive oil',
    instructions: '1. Wash vegetables\n2. Chop\n3. Toss with oil\n4. Season and serve',
    time: '10',
    difficulty: 'Easy',
  },
}

export function uniqueRecipe(base = recipes.pasta) {
  return { ...base, title: `${base.title.split(' ').slice(0, 2).join(' ')} ${Date.now()}` }
}
```

---

## Authentication Setup

### auth.setup.ts

```typescript
import { test as setup, expect } from '@playwright/test'
import { users } from './fixtures/test-data'

setup('authenticate as regular user', async ({ page }) => {
  await page.goto('/login')
  await page.getByLabel('Email').fill(users.regular.email)
  await page.getByLabel('Password').fill(users.regular.password)
  await page.getByRole('button', { name: 'Sign In' }).click()
  await expect(page).toHaveURL('/')

  await page.context().storageState({ path: '.auth/user.json' })
})

setup('authenticate as admin', async ({ page }) => {
  await page.goto('/login')
  await page.getByLabel('Email').fill(users.admin.email)
  await page.getByLabel('Password').fill(users.admin.password)
  await page.getByRole('button', { name: 'Sign In' }).click()
  await expect(page).toHaveURL('/')

  await page.context().storageState({ path: '.auth/admin.json' })
})
```

---

## Test Suites

### login.spec.ts

```typescript
import { test, expect } from './fixtures/auth'
import { users } from './fixtures/test-data'

test.describe('Login Flow', () => {
  test('successful login redirects to home', async ({ loginPage }) => {
    await loginPage.goto()
    await loginPage.login(users.regular.email, users.regular.password)
    await loginPage.expectRedirectToDashboard()
  })

  test('invalid credentials show error', async ({ loginPage }) => {
    await loginPage.goto()
    await loginPage.login('wrong@email.com', 'wrongpassword')
    await loginPage.expectError('Invalid')
  })

  test('empty form shows validation errors', async ({ loginPage }) => {
    await loginPage.goto()
    await loginPage.signInButton.click()
    await expect(loginPage.page.getByText(/required|email/i)).toBeVisible()
  })

  test('sign up link navigates to registration', async ({ loginPage }) => {
    await loginPage.goto()
    await loginPage.signUpLink.click()
    await expect(loginPage.page).toHaveURL('/signup')
  })

  test('guest mode allows browsing without login', async ({ loginPage }) => {
    await loginPage.goto()
    await loginPage.guestButton.click()
    await expect(loginPage.page).toHaveURL('/')
  })
})
```

### recipe-create.spec.ts

```typescript
import { test, expect } from './fixtures/auth'
import { uniqueRecipe } from './fixtures/test-data'

test.use({ storageState: '.auth/user.json' })

test.describe('Recipe Creation', () => {
  test('creates a new recipe successfully', async ({ recipeCreatePage }) => {
    const recipe = uniqueRecipe()
    await recipeCreatePage.goto()
    await recipeCreatePage.fillRecipe(recipe)
    await recipeCreatePage.submit()
    await recipeCreatePage.expectSuccess()
  })

  test('validates required fields', async ({ recipeCreatePage }) => {
    await recipeCreatePage.goto()
    await recipeCreatePage.submit()
    await expect(recipeCreatePage.page.getByText(/required/i).first()).toBeVisible()
  })

  test('preserves form data on validation error', async ({ recipeCreatePage }) => {
    await recipeCreatePage.goto()
    await recipeCreatePage.titleInput.fill('Partial Recipe')
    await recipeCreatePage.submit()

    await expect(recipeCreatePage.titleInput).toHaveValue('Partial Recipe')
  })

  test('navigates to recipe detail after creation', async ({ recipeCreatePage, page }) => {
    const recipe = uniqueRecipe()
    await recipeCreatePage.goto()
    await recipeCreatePage.fillRecipe(recipe)
    await recipeCreatePage.submit()

    await expect(page).toHaveURL(/\/recipes\//)
    await expect(page.getByRole('heading', { level: 1 })).toContainText(recipe.title)
  })
})
```

### recipe-search.spec.ts

```typescript
import { test, expect } from './fixtures/auth'

test.use({ storageState: '.auth/user.json' })

test.describe('Recipe Search', () => {
  test('search returns matching recipes', async ({ searchPage }) => {
    await searchPage.goto()
    await searchPage.search('pasta')
    const count = await searchPage.results.count()
    expect(count).toBeGreaterThan(0)
  })

  test('search with no matches shows empty state', async ({ searchPage }) => {
    await searchPage.goto()
    await searchPage.search('xyznonexistentrecipe123')
    await searchPage.expectNoResults()
  })

  test('search is case-insensitive', async ({ searchPage }) => {
    await searchPage.goto()
    await searchPage.search('PASTA')
    const count = await searchPage.results.count()
    expect(count).toBeGreaterThan(0)
  })

  test('clicking a search result navigates to detail', async ({ searchPage, page }) => {
    await searchPage.goto()
    await searchPage.search('pasta')
    await searchPage.results.first().click()
    await expect(page).toHaveURL(/\/recipes\//)
  })
})
```

### recipe-detail.spec.ts

```typescript
import { test, expect } from './fixtures/auth'

test.use({ storageState: '.auth/user.json' })

test.describe('Recipe Detail View', () => {
  test.beforeEach(async ({ homePage }) => {
    await homePage.goto()
  })

  test('displays recipe information', async ({ homePage, page }) => {
    await homePage.recipeCards.first().click()
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible()
  })

  test('shows ingredients and instructions', async ({ homePage, recipeDetailPage, page }) => {
    await homePage.recipeCards.first().click()
    await expect(recipeDetailPage.ingredients).toBeVisible()
    await expect(recipeDetailPage.instructions).toBeVisible()
  })

  test('back button returns to previous page', async ({ homePage, recipeDetailPage, page }) => {
    await homePage.recipeCards.first().click()
    await recipeDetailPage.backButton.click()
    await expect(page).toHaveURL('/')
  })
})
```

### profile.spec.ts

```typescript
import { test, expect } from './fixtures/auth'
import { users } from './fixtures/test-data'

test.use({ storageState: '.auth/user.json' })

test.describe('Profile Page', () => {
  test('displays user information', async ({ profilePage }) => {
    await profilePage.goto()
    await profilePage.expectDisplayName(users.regular.name)
  })

  test('shows user recipes', async ({ profilePage }) => {
    await profilePage.goto()
    await expect(profilePage.userRecipes.first()).toBeVisible()
  })

  test('edit profile button is accessible', async ({ profilePage }) => {
    await profilePage.goto()
    await expect(profilePage.editProfileButton).toBeVisible()
    await expect(profilePage.editProfileButton).toBeEnabled()
  })
})
```

### admin.spec.ts

```typescript
import { test, expect } from './fixtures/auth'

test.use({ storageState: '.auth/admin.json' })

test.describe('Admin Functions', () => {
  test('admin dashboard loads with stats', async ({ adminPage }) => {
    await adminPage.goto()
    await adminPage.expectStatCount(2)
  })

  test('user management tab shows user list', async ({ adminPage }) => {
    await adminPage.goto()
    await adminPage.switchTab('Users')
    await expect(adminPage.userTable).toBeVisible()
  })

  test('recipe management tab shows recipes', async ({ adminPage }) => {
    await adminPage.goto()
    await adminPage.switchTab('Recipes')
    await expect(adminPage.recipeTable).toBeVisible()
  })

  test('non-admin user cannot access admin page', async ({ page }) => {
    // Use regular user auth for this test
    test.use({ storageState: '.auth/user.json' })
    await page.goto('/admin')
    await expect(page).not.toHaveURL('/admin')
  })
})
```

---

## Configuration

### playwright.config.ts

```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 4 : undefined,
  reporter: [
    ['html', { open: 'never' }],
    ['list'],
    ...(process.env.CI ? [['github' as const]] : []),
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    // Auth setup — runs first
    { name: 'setup', testMatch: /.*\.setup\.ts/ },

    // Authenticated tests
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
      dependencies: ['setup'],
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
      dependencies: ['setup'],
    },
    {
      name: 'mobile',
      use: { ...devices['iPhone 14'] },
      dependencies: ['setup'],
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
    timeout: 30000,
  },
})
```

### .github/workflows/playwright.yml

```yaml
name: Playwright Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Run Playwright tests
        run: npx playwright test

      - name: Upload test report
        uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 14

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: test-results
          path: test-results/
          retention-days: 7
```
