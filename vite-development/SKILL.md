---
name: vite-development
version: "2.0"
last_updated: 2026-08-14
tags: [vite, development, testing, quality, automation]
description: "Vite 8.0.10 build tooling — HMR, fast builds, plugins, and optimized production assets. Use when configuring Vite, setting up React/Vue projects with Vite, or optimizing frontend build performance."
---
# Vite Development

> Optimized for Vite 8+, React 19+, TypeScript 5.5+, Vitest 2+, and modern ESM-first frontend builds.

Expert guidance for using Vite 8.0.10 as the build tool for React and other web applications with modern frontend development patterns. Documentation grounded in the official Vite docs at https://vite.dev/.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Component Review Rubric Reference

Apply the shared [Component Review Rubric](../frontend-design/SKILL.md#component-review-rubric) before approving Vite components, then run the Vite-specific checks below.

## Anti-Patterns

- Hard-coding environment-specific URLs: Builds become fragile as soon as the app moves between local, staging, and production.
- Treating plugin order as incidental: Vite plugins often transform the same files, so ordering bugs are easy to create.
- Assuming fast HMR guarantees good production output: Bundle quality and runtime behavior still need explicit review.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Vite Development guidance is tied to a concrete route, component, screen, or design artifact.
2. Pass/fail: Component states cover loading, empty, error, success, and responsive breakpoints where applicable.
3. Pass/fail: Accessibility, visual hierarchy, and interaction behavior are reviewed against the shared component rubric.
4. Pressure-test scenario: Review the component on a narrow mobile viewport, keyboard-only path, and slow-loading state.
5. Success metric: Zero generic UI approval; every approval cites rendered behavior or source evidence.

## Before and After Example

```ts
// Before
export default {
  server: { proxy: { '/api': 'http://localhost:3000' } },
};

// After
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  return {
    server: {
      proxy: {
        '/api': {
          target: env.VITE_API_BASE_URL,
          changeOrigin: true,
        },
      },
    },
  };
});
```

Makes the proxy configuration mode-aware and driven by typed environment input instead of hard-coded URLs.

## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

**Project Setup & Configuration:**
- Initializing new Vite projects
- Configuring `vite.config.js` with plugins
- Setting up development server with custom options
- Configuring build optimization and bundling

**Performance & Optimization:**
- Optimizing bundle size and code splitting
- Configuring lazy loading and dynamic imports
- Setting up asset optimization (images, CSS)
- Enabling CSS code splitting and module resolution

**Development Experience:**
- Configuring Hot Module Replacement (HMR)
- Setting up proxy for API calls in dev
- Environment variable handling
- Source map configuration

**Plugin Ecosystem:**
- Using official Vite plugins (React, Vue)
- Community plugins for specific needs
- Writing custom Vite plugins
- Configuring plugin options and hooks

---

## Part 1: Project Configuration

### Basic Vite Config

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    open: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'api-client': ['./src/api/client'],
        },
      },
    },
  },
});
```

### Environment-Specific Config

```javascript
// vite.config.js
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd());

  return {
    base: mode === 'production' ? '/app-base-path/' : '/',
    server: {
      proxy: {
        '/api': {
          target: env.VITE_API_URL || 'http://localhost:8080',
          changeOrigin: true,
        },
      },
    },
    define: {
      __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
    },
  };
});
```

---

## Part 2: Build Optimization

### Code Splitting

```javascript
// vite.config.js
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            // React and ReactDOM
            if (id.includes('react') || id.includes('react-dom')) {
              return 'react-vendor';
            }
            // Other large libraries
            if (id.includes('axios')) {
              return 'api-lib';
            }
            return 'vendor';
          }
        },
      },
    },
  },
});
```

### Lazy Loading Routes

```javascript
// Lazy loading route components
const RecipeDetail = lazy(() => import('./pages/RecipeDetail'));
const RecipeList = lazy(() => import('./pages/RecipeList'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/recipes/:id" element={<RecipeDetail />} />
        <Route path="/recipes" element={<RecipeList />} />
      </Routes>
    </Suspense>
  );
}
```

---

## Part 3: Development Server

### Proxy Configuration

```javascript
// vite.config.js
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
      '/auth': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      },
    },
  },
});
```

### HMR Configuration

```javascript
// vite.config.js
export default defineConfig({
  server: {
    hmr: {
      overlay: true,
    },
    watch: {
      usePolling: true,
      interval: 100,
    },
  },
});
```

---

## Part 4: Assets and Plugins

### Image Optimization

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import viteImagemin from 'vite-plugin-imagemin';

export default defineConfig({
  plugins: [
    viteImagemin({
      gifsicle: { optimizationLevel: 7 },
      optipng: { optimizationLevel: 7 },
      mozjpeg: { quality: 80 },
      pngquant: { quality: [0.65, 0.9], speed: 4 },
      svgo: {
        plugins: [
          {
            name: 'removeViewBox',
            active: false,
          },
        ],
      },
    }),
  ],
});
```

---

## Vite Development Best Practices

### Configuration
- [ ] Use `defineConfig` for type-safe configuration
- [ ] Separate dev and production concerns
- [ ] Enable sourcemaps for debugging
- [ ] Configure proper base path for deployment
- [ ] Set up proxy for API during development

### Build Optimization
- [ ] Implement code splitting for vendors
- [ ] Use lazy loading for heavy routes/components
- [ ] Configure manual chunks for better caching
- [ ] Optimize assets (images, fonts)
- [ ] Enable minification for production builds

### Performance
- [ ] Monitor bundle size with Vite bundle analyzer
- [ ] Use tree-shaking to remove unused code
- [ ] Configure dynamic imports for better time-to-interactive
- [ ] Enable CSS code splitting for faster page loads
- [ ] Use compression middleware for production

### Development
- [ ] Configure HMR for faster iteration
- [ ] Set up environment variables for different environments
- [ ] Use proxy for local API development
- [ ] Enable source maps for better debugging
- [ ] Configure clear port and open options

## Common Pitfalls

- Hard-coding environment-specific URLs: Builds become fragile as soon as the app moves between local, staging, and production.
- Treating plugin order as incidental: Vite plugins can transform the same files, so ordering bugs are easy to create.
- Ignoring bundle inspection: Fast local HMR does not guarantee the production output is well-shaped.

## Modern Component and Testing Examples

### Server Components
```tsx
export async function OrdersPanel() {
  const orders = await getOrders();
  return <OrdersTable orders={orders} />;
}
```

### Error Boundaries
```tsx
import { ErrorBoundary } from 'react-error-boundary';

<ErrorBoundary fallbackRender={() => <p>Could not load dashboard.</p>}>
  <Dashboard />
</ErrorBoundary>
```

### Accessibility Testing Tools
```tsx
import { axe } from 'jest-axe';

test('dialog passes axe checks', async () => {
  const { container } = render(<AccountDialog open />);
  expect(await axe(container)).toHaveNoViolations();
});
```

## References & Resources

### Documentation
- [Vite 2026 Config Reference](./references/vite-2026-config-reference.md) — Comprehensive Vite configuration guide
- [Vite Official Excerpts - HMR Config](./references/vite-official-excerpts-hmr-config.md) — Hot Module Replacement configuration

### Examples
- [Vite Config Examples](./examples/vite-config-examples.md) — Example Vite configurations for different use cases

### Scripts
- [Vite Plugin Template](./scripts/vite-plugin-template.ts) — Template for creating custom Vite plugins

### Official Documentation
- [Vite Documentation](https://vite.dev/)
- [Vite Plugins](https://vite.dev/plugins/)
- [Rollup Options](https://vite.dev/config/build-options.html#build-rollupoptions)


---

<!-- MCP:START -->

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/vite-development` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the Vite Development skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [javascript-development](../javascript-development/SKILL.md): Use it when the workflow also needs modern JavaScript and TypeScript application code.
- [react-development](../react-development/SKILL.md): Use it when the workflow also needs React component architecture and client or server boundaries.
- [web-testing](../web-testing/SKILL.md): Use it when the workflow also needs browser and end-to-end testing evidence.
- [frontend-design](../frontend-design/SKILL.md): Use it when the workflow also needs UI composition and front-end design direction.
