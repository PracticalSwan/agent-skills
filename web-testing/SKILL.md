---
name: web-testing
version: "1.3"
last_updated: 2026-07-11
tags: [web, testing, workflow, automation, guidance]
description: "Playwright automation, Chrome DevTools debugging, and browser interaction testing. Use for E2E/unit tests, capturing screenshots, inspecting network/console logs, or validating user flows in web applications."
---
# Web Application Testing & Debugging

Comprehensive toolkit for testing and debugging web applications using Playwright automation and Chrome DevTools.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.



## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

**Playwright Testing:**
- Testing frontend functionality in a real browser
- Verifying UI behavior and interactions
- Debugging web application issues
- Capturing screenshots for documentation or debugging
- Inspecting browser console logs
- Validating form submissions and user flows
- Checking responsive design across viewports

**Chrome DevTools Debugging:**
- Interacting with web pages through automated controls
- Taking screenshots, and analyzing network traffic
- Navigating pages, clicking elements, filling forms, handling dialogs
- Emulating network conditions or devices
- Running JavaScript in page context, capturing console messages
- Performance profiling and identifying bottlenecks

## Part 1: Playwright Testing

### Core Capabilities

#### Browser Automation
```typescript
import { test, expect, Page, Browser } from '@playwright/test';

// Navigate to URLs
await page.goto('https://example.com');
await page.waitForLoadState('networkidle');

// Click buttons and links
await page.click('#submit-button');
await page.click('text=Continue');

// Fill form fields
await page.fill('#email', 'user@example.com');
await page.fill('#password', 'securepassword');

// Select dropdowns
await page.selectOption('#country', 'United States');

// Handle dialogs and alerts
page.on('dialog', async dialog => {
  await dialog.accept(); // or dialog.dismiss()
});
```

#### User Flow Testing
```typescript
test('complete checkout flow', async ({ page }) => {
  // Add to cart
  await page.goto('/products');
  await page.click('text=Add to Cart');

  // Navigate to cart
  await page.goto('/cart');

  // Verify item in cart
  await expect(page.locator('.cart-item')).toHaveCount(1);

  // Checkout
  await page.click('text=Checkout');
  await page.fill('#email', 'test@example.com');
  await page.fill('#shipping-address', '123 Main St');
  await page.click('text=Place Order');

  // Verify success
  await expect(page.locator('.success-message')).toBeVisible();
});
```

#### Form Validation Testing
```typescript
test('form validation', async ({ page }) => {
  await page.goto('/register');

  // Submit empty form - should show errors
  await page.click('text=Submit');

  // Check error messages
  await expect(page.locator('.error-email')).toBeVisible();
  await expect(page.locator('.error-password')).toBeVisible();

  // Fill valid data
  await page.fill('#email', 'valid@example.com');
  await page.fill('#password', 'securePass123!');
  await page.click('text=Submit');

  // Verify no errors and success
  await expect(page.locator('.error-email')).not.toBeVisible();
  await expect(page.locator('.success-message')).toBeVisible();
});
```

### Responsive Testing

```typescript
test.describe('Responsive Design', () => {
  const viewports = [
    { name: 'Mobile', width: 375, height: 667 },
    { name: 'Tablet', width: 768, height: 1024 },
    { name: 'Desktop', width: 1280, height: 720 },
  ];

  viewports.forEach(({ name, width, height }) => {
    test(`layout on ${name} (${width}x${height})`, async ({ page }) => {
      await page.setViewportSize({ width, height });
      await page.goto('/');

      // Check navigation is visible and accessible
      const nav = page.locator('nav');
      await expect(nav).toBeVisible();

      // On mobile, check hamburger menu is present
      if (width < 768) {
        await expect(page.locator('.mobile-menu-toggle')).toBeVisible();
      } else {
        await expect(page.locator('.mobile-menu-toggle')).not.toBeVisible();
      }

      // Screenshot for comparison
      await page.screenshot({
        path: `screenshots/${name.toLowerCase()}-layout.png`,
        fullPage: true,
      });
    });
  });
});
```

### Console & Network Inspection

```typescript
test('console errors and warnings', async ({ page, context }) => {
  const errors: string[] = [];

  // Listen for console errors
  page.on('console', msg => {
    if (msg.type() === 'error') {
      errors.push(msg.text());
    }
  });

  await page.goto('/');

  // Assertions
  expect(errors).toEqual([]);
});

test('network requests monitoring', async ({ page }) => {
  const requests: string[] = [];

  page.on('request', request => {
    requests.push(request.url());
  });

  await page.goto('/');

  // Verify API calls
  const apiRequests = requests.filter(url => url.includes('/api/'));
  expect(apiRequests.length).toBeGreaterThan(0);

  // Verify no 404s
  const failedResponses: any[] = [];
  page.on('response', response => {
    if (response.status() === 404) {
      failedResponses.push(response.url());
    }
  });

  await page.click('a[href="/about"]');
  expect(failedResponses).toEqual([]);
});
```

### Accessibility Testing

```typescript
test('basic accessibility checks', async ({ page }) => {
  // Check heading hierarchy
  const headings = await page.locator('h1, h2, h3').all();
  expect(headings[0]).toHaveText('Main Heading'); // h1 should be first

  // Check images have alt text
  const imagesWithoutAlt = await page.locator('img:not([alt])').count();
  expect(imagesWithoutAlt).toBe(0);

  // Check form labels
  const inputs = await page.locator('input, select, textarea').all();
  for (const input of inputs) {
    const hasLabel = await input.evaluate(el => {
      return el.labels.length > 0 || el.getAttribute('aria-label');
    });
    expect(hasLabel).toBeTruthy();
  }

  // Check keyboard navigation
  await page.keyboard.press('Tab');
  const focusedElement = await page.evaluate(() => document.activeElement?.tagName);
  expect(['INPUT', 'BUTTON', 'A']).toContain(focusedElement);
});
```

### Visual Regression Testing

```typescript
import { compareScreenshots } from './visual-utils';

test('visual regression - home page', async ({ page }) => {
  await page.goto('/');

  // Wait for all images and fonts to load
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1000);

  // Take screenshot
  const screenshot = await page.screenshot({
    fullPage: true,
  });

  // Compare with baseline
  const diff = await compareScreenshots(screenshot, 'baseline/home.png');
  expect(diff.pixelDifference).toBeLessThan(100); // Threshold
});
```

---

## Part 2: Chrome DevTools Integration

### Tool Categories

#### Navigation & Page Management
```javascript
// Open new page
await chrome.newPage();

// Navigate to URL
await chrome.navigatePage('https://example.com');

// Reload current page
await chrome.navigatePage({ action: 'reload' });

// Navigate history
await chrome.navigatePage({ action: 'back' });
await chrome.navigatePage({ action: 'forward' });

// List all open pages
const pages = await chrome.listPages();
await chrome.selectPage(pages[0].id);

// Close specific page
await chrome.closePage('page-id-here');

// Wait for text to appear
await chrome.waitFor('Welcome to the site');
```

#### Input & Interaction
```javascript
// Take snapshot to get element IDs
const snapshot = await chrome.takeSnapshot();

// Find element by uid
const submitButton = snapshot.elements.find(el => el.text === 'Submit');

// Click element
await chrome.click(submitButton.uid);

// Fill single field
await chrome.fill(inputUid, 'value@example.com');

// Fill multiple fields at once
await chrome.fillForm([
  { uid: emailInputUid, value: 'test@example.com' },
  { uid: passwordInputUid, value: 'password123' },
  { uid: nameInputUid, value: 'John Doe' },
]);

// Hover over element
await chrome.hover(buttonUid);

// Press keyboard shortcuts
await chrome.pressKey('Enter');
await chrome.pressKey('Control+C');

// Drag and drop
await chrome.drag(sourceUid, targetUid);

// Handle browser dialogs
await chrome.handleDialog('accept');
await chrome.handleDialog('dismiss');
```

#### Debugging & Inspection
```javascript
// Get accessibility tree (best for finding elements)
const snapshot = await chrome.takeSnapshot();

// Take visual screenshot
const screenshot = await chrome.takeScreenshot();

// List all console messages
const messages = await chrome.listConsoleMessages();

// Get messages by level
const errors = await chrome.listConsoleMessages('error');
const warnings = await chrome.listConsoleMessages('warning');

// Get specific message details
const message = await chrome.getConsoleMessage(messageId);

// Evaluate JavaScript in page context
const result = await chrome.evaluateScript('document.title');
const userInfo = await chrome.evaluateScript(`
  JSON.parse(localStorage.getItem('user'))
`);

// List network requests
const requests = await chrome.listNetworkRequests();

// Get failed requests
const failedRequests = requests.filter(req =>
  req.status >= 400 || req.status === 0
);

// Get specific request details
const requestDetails = await chrome.getNetworkRequest(requestId);
```

#### Emulation & Performance
```javascript
// Resize viewport
await chrome.resizePage({ width: 375, height: 667 }); // Mobile

// Emulate network conditions
await chrome.emulate({
  network: 'offline'    // 'slow-3g', 'fast-3g', 'online'
});

// Emulate geolocation
await chrome.emulate({
  geolocation: { lat: 40.7128, lon: -74.0060 }
});

// Start performance trace
await chrome.performanceStartTrace({ reload: true });

// Stop trace after navigation
await chrome.waitFor('Page loaded');
const trace = await chrome.performanceStopTrace();

// Get insights
const insights = await chrome.performanceAnalyzeInsight();
console.log('LCP:', insights.largestContentfulPaint);
console.log('CLS:', insights.cumulativeLayoutShift);
```

### Common Debugging Patterns

#### Pattern A: Identifying Elements (Snapshot-First)

Always prefer snapshot over screenshot for finding elements:

```javascript
// 1. Get current page structure
const snapshot = await chrome.takeSnapshot();

// 2. Find the target element by its uid
const element = snapshot.elements.find(el => el.text === 'Continue');

// 3. Use the uid for interaction
await chrome.click(element.uid);
```

#### Pattern B: Troubleshooting Errors

When a page is failing, check both console and network:

```javascript
// 1. Check console messages for JavaScript errors
const errors = await chrome.listConsoleMessages('error');
console.log('JavaScript Errors:', errors);

// 2. Check network requests for failures
const requests = await chrome.listNetworkRequests();
const failed = requests.filter(r => r.status >= 400);
console.log('Failed Requests:', failed);

// 3. Check specific values via JavaScript
const apiResponse = await chrome.evaluateScript(`
  window.lastApiResponse
`);
console.log('Last API Response:', apiResponse);
```

#### Pattern C: Performance Profiling

Identify why a page is slow:

```javascript
// 1. Start performance trace with reload
await chrome.performanceStartTrace({ reload: true, autoStop: true });

// 2. Wait for trace to complete
const timeout = 10000;
await new Promise(resolve => setTimeout(resolve, timeout));

// 3. Get performance insights
const insights = await chrome.performanceAnalyzeInsight();

console.log('Performance Issues:', insights.issues);
console.log('LCP:', insights.largestContentfulPaint);
console.log('CLS:', insights.cumulativeLayoutShift);
console.log('FID:', insights.firstInputDelay);

// 4. Identify bottlenecks
if (insights.largestContentfulPaint > 2500) {
  console.warn('LCP is slow - consider optimizing images and CSS');
}
if (insights.cumulativeLayoutShift > 0.1) {
  console.warn('CLS is high - avoid layout shifts');
}
```

## Part 3: Testing Best Practices

### Test Structure

```typescript
test.describe('User Authentication', () => {
  test.beforeEach(async ({ page }) => {
    // Setup: login fresh each test
    await page.goto('/login');
  });

  test('successful login with valid credentials', async ({ page }) => {
    await test.step('Enter credentials', async () => {
      await page.fill('#email', 'valid@example.com');
      await page.fill('#password', 'correct-password');
    });

    await test.step('Submit form', async () => {
      await page.click('text=Login');
    });

    await test.step('Verify redirected to dashboard', async () => {
      await expect(page).toHaveURL('/dashboard');
    });
  });

  test('shows error for invalid credentials', async ({ page }) => {
    await page.fill('#email', 'invalid@example.com');
    await page.fill('#password', 'wrong-password');
    await page.click('text=Login');

    await expect(page.locator('.error-message')).toBeVisible();
    await expect(page).toHaveURL('/login');
  });
});
```

### Page Object Model

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.fill('#email', email);
    await this.page.fill('#password', password);
    await this.page.click('text=Login');
  }

  async getErrorMessage() {
    return await this.page.locator('.error-message').textContent();
  }

  assertVisible() {
    expect(this.page.locator('h1')).toHaveText('Login');
  }
}

// Tests
test('login flow', async ({ page }) => {
  const loginPage = new LoginPage(page);

  loginPage.goto();
  await loginPage.login('user@example.com', 'password');

  await expect(page).toHaveURL('/dashboard');
});
```

### Parallel Testing

```typescript
// playwright.config.ts
export default defineConfig({
  workers: process.env.CI ? 2 : 4, // Parallel execution

  projects: [
    {
      name: 'chromium',
      use: { browserName: 'chromium' },
    },
    {
      name: 'firefox',
      use: { browserName: 'firefox' },
    },
    {
      name: 'webkit',
      use: { browserName: 'webkit' },
    },
  ],
});
```

---

## Part 4: Debugging Toolset

### Quick Reference

| Task | Playwright | Chrome DevTools |
|------|-----------|-----------------|
| Browser Automation | Yes | Yes |
| Page Navigation | `page.goto()` | `navigate_page()` |
| Click Elements | `page.click()` | `click(uid)` |
| Fill Forms | `page.fill()` | `fill(uid, value)` |
| Screenshots | `page.screenshot()` | `take_screenshot()` |
| Console Logs | `page.on('console')` | `list_console_messages()` |
| Network Requests | `page.on('request')` | `list_network_requests()` |
| JavaScript Eval | `page.evaluate()` | `evaluate_script()` |
| Viewport Resize | `page.setViewportSize()` | `resize_page()` |
| Performance | Trace API | `performance_*` tools |
| Device Emulation | `deviceDescriptor` | `emulate()` |

### Common Debugging Commands

```bash
# Run Playwright tests
npx playwright test

# Run tests with UI (helps debugging)
npx playwright test --ui

# Run tests in headed mode (watch browser)
npx playwright test --headed

# Debug specific test
npx playwright test tests/login.spec.ts --debug

# Generate codegen from browser actions
npx playwright codegen https://example.com
```

---

## Anti-Patterns

- Starting without a clear success condition: The skill becomes advice-shaped instead of workflow-shaped.
- Skipping the bundled references or scripts: You lose the proven path the catalog is trying to preserve.
- Claiming completion without concrete evidence: A future agent or reviewer cannot trust the result or resume the work safely.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Web Testing implementation names the target runtime, framework version, and affected files.
2. Pass/fail: Build, lint, test, or equivalent local validation is run for the changed surface.
3. Pass/fail: Edge cases for errors, dependency drift, and environment differences are addressed or explicitly out of scope.
4. Pressure-test scenario: Apply the workflow to a change that passes happy-path tests but fails one boundary condition.
5. Success metric: Zero untested success claims; every implementation claim maps to a command or artifact.

## Testing Checklist

### Functionality
- [ ] All user flows work end-to-end
- [ ] Form validation tested for success and failure cases
- [ ] Error handling verified
- [ ] Edge cases covered

### Responsive Design
- [ ] Tested on mobile (375px, 414px)
- [ ] Tested on tablet (768px, 1024px)
- [ ] Tested on desktop (1280px, 1440px)
- [ ] Navigation accessible on mobile
- [ ] No horizontal scrollbars

### Cross-Browser
- [ ] Tested in Chrome
- [ ] Tested in Firefox
- [ ] Tested in Safari/WebKit
- [ ] Tested in Edge

### Accessibility
- [ ] All interactive elements keyboard accessible
- [ ] Focus states visible
- [ ] ARIA labels on icon-only buttons
- [ ] Form fields have labels
- [ ] Images have alt text (except decorative)
- [ ] Touch targets ≥ 44x44px on mobile

### Performance
- [ ] Page load time < 3 seconds
- [ ] LCP < 2.5 seconds
- [ ] CLS < 0.1
- [ ] No layout shifts on interaction
- [ ] Images optimized (WebP, lazy load)

### Error Handling
- [ ] Console errors logged and reviewed
- [ ] Failed network requests identified
- [ ] 404s checked and fixed
- [ ] 500 errors investigated
- [ ] User-friendly error messages shown

---

## References & Resources

### Documentation
- [Playwright Selectors](./references/playwright-selectors.md) — All selector types with decision tree and priority order
- [Test Patterns](./references/test-patterns.md) — Page Object Model, fixtures, auth reuse, API mocking, and accessibility patterns

### Scripts
- [Test Scaffold](./scripts/test-scaffold.ps1) — PowerShell Playwright test file generator for e2e, visual, and accessibility tests

### Examples
- [E2E Recipe App Tests](./examples/e2e-recipe-app-tests.md) — Kitchen Odyssey test suite with Page Objects and CI configuration

---

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:web-testing` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py web-testing` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: Playwright MCP

- Fallback prompt: "Use the Web Application Testing & Debugging skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- Use Playwright CLI (`npx playwright test`, headed mode, or codegen) and browser devtools when MCP browser tools are unavailable.
- Keep screenshots, console logs, and network traces as test evidence when reproducing issues manually.

<!-- MCP:END -->

## Related Skills

- [development-workflow](../development-workflow/SKILL.md): Use it when the workflow also needs planning, quality gates, and delivery tracking.
- [documentation-quality](../documentation-quality/SKILL.md): Use it when the workflow also needs documentation review standards and quality gates.
- [verification-before-completion](../verification-before-completion/SKILL.md): Use it when the workflow also needs final evidence checks before claiming completion.
- [code-quality](../code-quality/SKILL.md): Use it when the workflow also needs two-stage review (spec compliance first, then code quality), maintainability, and refactoring guidance.
