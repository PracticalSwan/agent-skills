# Vite Excerpts from Official Docs

Excerpted from official Vite 6 documentation at https://vite.dev/.

## server.hmr Configuration

Configure Hot Module Replacement (HMR) connection settings.

```js
export default defineConfig({
  server: {
    hmr: {
      protocol: 'wss',
      host: 'example.com',
      port: 443,
      overlay: false,
    },
  },
});
```

## Client-side HMR event handling

Register a handler for custom HMR events in the client.

```js
if (import.meta.hot) {
  import.meta.hot.on('special-update', (data) => {
    // perform custom update
  })
}
```

## Server-side custom HMR event

Send custom HMR events from a plugin to the client.

```js
handleHotUpdate({ server }) {
  server.ws.send({
    type: 'custom',
    event: 'special-update',
    data: {}
  })
  return []
}
```

## Guard HMR API usage for tree-shaking

Ensure HMR-specific code is excluded from production builds.

```js
if (import.meta.hot) {
  // HMR code
}
```

## Filter HMR modules

Filter modules affected by an HMR update.

```js
hotUpdate({ modules }) {
  return modules.filter(condition)
}
```

## Plugin communication via HMR

Bilateral communication between plugin and application using `environment.hot`.

```js
configureServer(server) {
  server.environments.ssr.hot.on('my:greetings', (data, client) => {
    client.send('my:foo:reply', `Hello from server! You said: ${data}`)
  })
}
```

## Source

- Vite Docs: https://vite.dev/
- HMR API: https://vite.dev/guide/api-hmr.html
- Plugin API: https://vite.dev/guide/api-plugin.html
