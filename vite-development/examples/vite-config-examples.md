# Vite Configuration Examples

Standard Vite 6 configurations for React apps with build optimization and development tooling.

## React + JSX

```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    open: false,
  },
  resolve: {
    alias: {
      '@': '/src',
    },
  },
});
```

## Code Splitting and Bundling

```javascript
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'api-utils': ['./src/api', './src/utils'],
        },
      },
    },
  },
});
```

## Development Proxy (for PHP API)

```javascript
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      },
    },
  },
});
```

## Environment Variables

```javascript
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');

  return {
    server: {
      proxy: {
        '/api': {
          target: env.VITE_API_URL,
          changeOrigin: true,
        },
      },
    },
    define: {
      __APP_ENV__: JSON.stringify(mode),
    },
  };
});
```
