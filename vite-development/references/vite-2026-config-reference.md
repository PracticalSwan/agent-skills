# Vite Configuration Reference (2026)

Vite 6 configuration options and patterns relevant to React + API apps. For details see https://vite.dev/config/.

## Core Configuration

### server

Development server options:

- port — Server port (default 5173)
- open — Open browser on start
- proxy — Proxy backend requests during dev
- hmr — Hot Module Replacement settings

```javascript
server: {
  port: 5173,
  open: true,
  proxy: {
    '/api': {
      target: 'http://localhost:8080',
      changeOrigin: true,
    },
  },
}
```

### build

Production build options:

- outDir — Output directory (default dist)
- sourcemap — Enable source maps (boolean/inline/hidden)
- rollupOptions — Rollup options for bundling
- minify — Minification (esbuild for JSX)

```javascript
build: {
  outDir: 'dist',
  sourcemap: true,
  rollupOptions: {
    output: {
      manualChunks: {
        'react-vendor': ['react', 'react-dom'],
      },
    },
  },
}
```

### plugins

Vite plugins array.

- Official plugins: @vitejs/plugin-react, @vitejs/plugin-vue
- Community: image optimization, compression, PWA, etc.

```javascript
plugins: [
  react(),
  viteImagemin(),
],
```

### resolve

Path resolution and aliases:

- alias — Import aliases
- extensions — File extensions to resolve

```javascript
resolve: {
  alias: {
    '@': '/src',
  },
}
```

### define

Global constants replaced at build time.

```javascript
define: {
  __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
}
```

## Environment Variables

`VITE_` prefix for client-side, standard names for server-side (if using SSR). Access via `import.meta.env.VITE_MY_VAR`.

## Best Practices

- Use `defineConfig` for TypeScript support (via vite/config/types).
- Proxy API calls in dev; configure base path after build.
- Enable source maps for debugging in dev; generate production maps only if needed.
- Split vendor chunks for better caching.
- Use plugins sparingly; each adds build overhead.

## References
- Vite Config Docs: https://vite.dev/config/
- Vite Plugins: https://vite.dev/plugins/
- React Plugin: https://github.com/vitejs/vite-plugin-react
