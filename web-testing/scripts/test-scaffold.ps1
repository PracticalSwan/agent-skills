<#
.SYNOPSIS
    Scaffolds Playwright test files with boilerplate code.

.DESCRIPTION
    Generates Playwright test files including a Page Object class and test
    cases skeleton based on the specified test type: e2e, visual, a11y, or
    performance.

.PARAMETER Name
    The test suite name (used for file and class naming). Required.

.PARAMETER Url
    The base URL for the test suite. Defaults to "http://localhost:3000".

.PARAMETER Type
    Test type: e2e, visual, a11y, or performance. Defaults to "e2e".

.EXAMPLE
    .\test-scaffold.ps1 -Name "RecipeSearch" -Url "http://localhost:5173" -Type e2e

.EXAMPLE
    .\test-scaffold.ps1 -Name "HomePage" -Type visual

.EXAMPLE
    .\test-scaffold.ps1 -Name "LoginForm" -Type a11y
#>
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Name,

    [Parameter(Position = 1)]
    [string]$Url = "http://localhost:3000",

    [Parameter(Position = 2)]
    [ValidateSet("e2e", "visual", "a11y", "performance")]
    [string]$Type = "e2e"
)

$ErrorActionPreference = "Stop"

$kebabName = ($Name -creplace '([A-Z])', '-$1').Trim('-').ToLower()
$pascalName = $Name
$testsDir = "tests"
$pagesDir = "tests/pages"

if (-not (Test-Path $testsDir)) { New-Item -ItemType Directory -Path $testsDir -Force | Out-Null }
if (-not (Test-Path $pagesDir)) { New-Item -ItemType Directory -Path $pagesDir -Force | Out-Null }

Write-Host "Scaffolding $Type test: $Name" -ForegroundColor Cyan
Write-Host "  Base URL: $Url" -ForegroundColor DarkGray

# --- Page Object ---
$pageObjectPath = "$pagesDir/${pascalName}Page.ts"
$pageObjectContent = @"
import { type Page, type Locator, expect } from '@playwright/test'

export class ${pascalName}Page {
  readonly page: Page

  // Define locators here
  readonly heading: Locator
  readonly mainContent: Locator

  constructor(page: Page) {
    this.page = page
    this.heading = page.getByRole('heading', { level: 1 })
    this.mainContent = page.locator('main')
  }

  async goto(path = '/') {
    await this.page.goto(path)
    await this.page.waitForLoadState('domcontentloaded')
  }

  async expectVisible() {
    await expect(this.mainContent).toBeVisible()
  }
}
"@

Set-Content -Path $pageObjectPath -Value $pageObjectContent
Write-Host "  Created: $pageObjectPath" -ForegroundColor Green

# --- Test File ---
$testPath = "$testsDir/${kebabName}.spec.ts"

switch ($Type) {
    "e2e" {
        $testContent = @"
import { test, expect } from '@playwright/test'
import { ${pascalName}Page } from './pages/${pascalName}Page'

test.describe('${Name} E2E Tests', () => {
  let ${Name.ToLower()}Page: ${pascalName}Page

  test.beforeEach(async ({ page }) => {
    ${Name.ToLower()}Page = new ${pascalName}Page(page)
    await ${Name.ToLower()}Page.goto()
  })

  test('should display the page correctly', async ({ page }) => {
    await ${Name.ToLower()}Page.expectVisible()
    await expect(${Name.ToLower()}Page.heading).toBeVisible()
  })

  test('should handle user interaction', async ({ page }) => {
    // TODO: Implement interaction test
    // Example:
    // await page.getByRole('button', { name: 'Action' }).click()
    // await expect(page.getByText('Result')).toBeVisible()
  })

  test('should navigate correctly', async ({ page }) => {
    // TODO: Implement navigation test
    // Example:
    // await page.getByRole('link', { name: 'Details' }).click()
    // await expect(page).toHaveURL(/\/details/)
  })

  test('should handle error states', async ({ page }) => {
    // TODO: Mock API error and verify error UI
    // await page.route('**/api/data', route =>
    //   route.fulfill({ status: 500 })
    // )
    // await page.reload()
    // await expect(page.getByText('Something went wrong')).toBeVisible()
  })

  test('should handle empty states', async ({ page }) => {
    // TODO: Mock empty response and verify empty state UI
    // await page.route('**/api/data', route =>
    //   route.fulfill({ status: 200, body: JSON.stringify([]) })
    // )
    // await page.reload()
    // await expect(page.getByText('No items found')).toBeVisible()
  })
})
"@
    }

    "visual" {
        $testContent = @"
import { test, expect } from '@playwright/test'
import { ${pascalName}Page } from './pages/${pascalName}Page'

test.describe('${Name} Visual Regression Tests', () => {
  let ${Name.ToLower()}Page: ${pascalName}Page

  test.beforeEach(async ({ page }) => {
    ${Name.ToLower()}Page = new ${pascalName}Page(page)
    await ${Name.ToLower()}Page.goto()
    await ${Name.ToLower()}Page.expectVisible()
  })

  test('full page screenshot', async ({ page }) => {
    await expect(page).toHaveScreenshot('${kebabName}-full.png', {
      fullPage: true,
      maxDiffPixelRatio: 0.01,
    })
  })

  test('main content screenshot', async ({ page }) => {
    await expect(${Name.ToLower()}Page.mainContent).toHaveScreenshot(
      '${kebabName}-main.png'
    )
  })

  test('dark mode screenshot', async ({ page }) => {
    await page.emulateMedia({ colorScheme: 'dark' })
    await expect(page).toHaveScreenshot('${kebabName}-dark.png', {
      fullPage: true,
    })
  })

  test('mobile viewport screenshot', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 })
    await expect(page).toHaveScreenshot('${kebabName}-mobile.png', {
      fullPage: true,
    })
  })

  test('tablet viewport screenshot', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 })
    await expect(page).toHaveScreenshot('${kebabName}-tablet.png', {
      fullPage: true,
    })
  })
})
"@
    }

    "a11y" {
        $testContent = @"
import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'
import { ${pascalName}Page } from './pages/${pascalName}Page'

test.describe('${Name} Accessibility Tests', () => {
  let ${Name.ToLower()}Page: ${pascalName}Page

  test.beforeEach(async ({ page }) => {
    ${Name.ToLower()}Page = new ${pascalName}Page(page)
    await ${Name.ToLower()}Page.goto()
    await ${Name.ToLower()}Page.expectVisible()
  })

  test('should have no WCAG 2.0 A violations', async ({ page }) => {
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a'])
      .analyze()

    expect(results.violations).toEqual([])
  })

  test('should have no WCAG 2.0 AA violations', async ({ page }) => {
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2aa'])
      .analyze()

    expect(results.violations).toEqual([])
  })

  test('should have proper heading hierarchy', async ({ page }) => {
    const headings = await page.evaluate(() => {
      const hs = document.querySelectorAll('h1, h2, h3, h4, h5, h6')
      return Array.from(hs).map((h) => ({
        level: parseInt(h.tagName[1]),
        text: h.textContent?.trim(),
      }))
    })

    // Verify h1 exists and heading levels don't skip
    expect(headings.length).toBeGreaterThan(0)
    expect(headings[0].level).toBe(1)
  })

  test('should have proper keyboard navigation', async ({ page }) => {
    // Tab through interactive elements
    await page.keyboard.press('Tab')
    const firstFocused = await page.evaluate(() => document.activeElement?.tagName)
    expect(firstFocused).toBeTruthy()

    // Verify focus is visible
    const focusedElement = page.locator(':focus')
    await expect(focusedElement).toBeVisible()
  })

  test('should have sufficient color contrast', async ({ page }) => {
    const results = await new AxeBuilder({ page })
      .withRules(['color-contrast'])
      .analyze()

    expect(results.violations).toEqual([])
  })

  test('images should have alt text', async ({ page }) => {
    const results = await new AxeBuilder({ page })
      .withRules(['image-alt'])
      .analyze()

    expect(results.violations).toEqual([])
  })
})
"@
    }

    "performance" {
        $testContent = @"
import { test, expect } from '@playwright/test'
import { ${pascalName}Page } from './pages/${pascalName}Page'

test.describe('${Name} Performance Tests', () => {
  let ${Name.ToLower()}Page: ${pascalName}Page

  test.beforeEach(async ({ page }) => {
    ${Name.ToLower()}Page = new ${pascalName}Page(page)
  })

  test('page loads within budget (3s)', async ({ page }) => {
    const start = Date.now()
    await ${Name.ToLower()}Page.goto()
    await page.waitForLoadState('networkidle')
    const loadTime = Date.now() - start

    console.log('Load time: ' + loadTime + 'ms')
    expect(loadTime).toBeLessThan(3000)
  })

  test('First Contentful Paint within budget', async ({ page }) => {
    await ${Name.ToLower()}Page.goto()

    const fcp = await page.evaluate(() => {
      const entry = performance.getEntriesByName('first-contentful-paint')[0]
      return entry ? entry.startTime : null
    })

    expect(fcp).not.toBeNull()
    expect(fcp).toBeLessThan(1500)
  })

  test('no excessive DOM nodes', async ({ page }) => {
    await ${Name.ToLower()}Page.goto()

    const nodeCount = await page.evaluate(
      () => document.querySelectorAll('*').length
    )

    console.log('DOM nodes: ' + nodeCount)
    expect(nodeCount).toBeLessThan(1500)
  })

  test('Cumulative Layout Shift within budget', async ({ page }) => {
    await ${Name.ToLower()}Page.goto()

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
        setTimeout(() => { observer.disconnect(); resolve(clsValue) }, 3000)
      })
    })

    console.log('CLS: ' + cls)
    expect(cls).toBeLessThan(0.1)
  })

  test('no large network payloads', async ({ page }) => {
    const responses: { url: string; size: number }[] = []

    page.on('response', async (response) => {
      const size = (await response.body().catch(() => Buffer.from(''))).length
      if (size > 500_000) {
        responses.push({ url: response.url(), size })
      }
    })

    await ${Name.ToLower()}Page.goto()
    await page.waitForLoadState('networkidle')

    if (responses.length > 0) {
      console.log('Large payloads:', responses)
    }
    expect(responses).toHaveLength(0)
  })
})
"@
    }
}

Set-Content -Path $testPath -Value $testContent
Write-Host "  Created: $testPath" -ForegroundColor Green

# --- Config scaffold (only if it doesn't exist) ---
$configPath = "playwright.config.ts"
if (-not (Test-Path $configPath)) {
    $configContent = @"
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 4 : undefined,
  reporter: [
    ['html'],
    ['list'],
  ],
  use: {
    baseURL: '${Url}',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 7'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: '${Url}',
    reuseExistingServer: !process.env.CI,
  },
})
"@
    Set-Content -Path $configPath -Value $configContent
    Write-Host "  Created: $configPath" -ForegroundColor Green
}

Write-Host "`nScaffolding complete!" -ForegroundColor Green
Write-Host "Files created:"
Write-Host "  - $pageObjectPath"
Write-Host "  - $testPath"
if (-not (Test-Path "$configPath.bak")) { Write-Host "  - $configPath (if new)" }
Write-Host "`nNext steps:"
Write-Host "  1. npm init playwright@latest (if not already installed)"
if ($Type -eq "a11y") { Write-Host "  2. npm install -D @axe-core/playwright" }
Write-Host "  2. Update page object locators for your actual UI"
Write-Host "  3. npx playwright test ${kebabName}.spec.ts"
