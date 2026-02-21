# End-to-End: Deploy a Vite + React App to Azure Static Web Apps

Complete walkthrough from zero to production with CI/CD, custom domain, and environment variables.

---

## Prerequisites

- [Node.js 20+](https://nodejs.org) and npm/pnpm
- [Azure CLI](https://aka.ms/install-azure-cli) installed and logged in (`az login`)
- [SWA CLI](https://github.com/Azure/static-web-apps-cli): `npm install -g @azure/static-web-apps-cli`
- A GitHub repository with your Vite + React project
- An Azure subscription (free tier works)

---

## 1. Project Structure

```
my-vite-app/
├── public/
│   └── favicon.svg
├── src/
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── staticwebapp.config.json    ← SWA routing/headers config
├── .github/
│   └── workflows/
│       └── deploy-swa.yml      ← CI/CD workflow
├── index.html
├── package.json
└── vite.config.js
```

---

## 2. Azure Resource Setup

### Option A: Azure CLI

```bash
# Variables
RG_NAME="rg-my-vite-app"
SWA_NAME="swa-my-vite-app"
LOCATION="centralus"

# Create resource group
az group create --name $RG_NAME --location $LOCATION

# Create Static Web App (Free tier)
az staticwebapp create \
  --name $SWA_NAME \
  --resource-group $RG_NAME \
  --location $LOCATION \
  --sku Free

# Get the deployment token (needed for GitHub Actions secret)
az staticwebapp secrets list \
  --name $SWA_NAME \
  --resource-group $RG_NAME \
  --query "properties.apiKey" -o tsv
```

Save the deployment token — you'll add it as a GitHub secret.

### Option B: Bicep Template

Create `infra/main.bicep`:

```bicep
targetScope = 'resourceGroup'

@description('Name of the Static Web App')
param appName string

@description('Azure region (SWA supports limited regions)')
@allowed(['centralus', 'eastus2', 'eastasia', 'westeurope', 'westus2'])
param location string = 'centralus'

@description('Pricing tier')
@allowed(['Free', 'Standard'])
param sku string = 'Free'

resource staticWebApp 'Microsoft.Web/staticSites@2023-12-01' = {
  name: appName
  location: location
  sku: {
    name: sku
    tier: sku
  }
  properties: {
    buildProperties: {
      appLocation: '/'
      outputLocation: 'dist'
    }
  }
}

resource appSettings 'Microsoft.Web/staticSites/config@2023-12-01' = {
  parent: staticWebApp
  name: 'appsettings'
  properties: {
    VITE_API_URL: 'https://api.example.com'
  }
}

output defaultHostname string = staticWebApp.properties.defaultHostname
output swaId string = staticWebApp.id
```

Deploy:

```bash
az deployment group create \
  --resource-group rg-my-vite-app \
  --template-file infra/main.bicep \
  --parameters appName='swa-my-vite-app'
```

---

## 3. Static Web App Configuration

Create `staticwebapp.config.json` in the project root:

```json
{
  "navigationFallback": {
    "rewrite": "/index.html",
    "exclude": ["/assets/*", "/api/*"]
  },
  "routes": [
    {
      "route": "/api/*",
      "allowedRoles": ["authenticated"]
    },
    {
      "route": "/admin/*",
      "allowedRoles": ["admin"]
    },
    {
      "route": "/login",
      "rewrite": "/.auth/login/github"
    },
    {
      "route": "/logout",
      "redirect": "/.auth/logout"
    }
  ],
  "responseOverrides": {
    "401": {
      "statusCode": 302,
      "redirect": "/login"
    },
    "404": {
      "rewrite": "/index.html",
      "statusCode": 200
    }
  },
  "globalHeaders": {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self' https://api.example.com",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()"
  },
  "mimeTypes": {
    ".json": "application/json",
    ".wasm": "application/wasm"
  },
  "platform": {
    "apiRuntime": "node:20"
  }
}
```

### Key Config Points

- **`navigationFallback`**: Required for SPAs — rewrites all unmatched routes to `index.html` so client-side routing (React Router, etc.) works.
- **`exclude`**: Paths that should NOT be rewritten (static assets, API calls).
- **`routes`**: Role-based access control, redirects, rewrites.
- **`globalHeaders`**: Security headers applied to every response.

---

## 4. GitHub Actions Workflow

### Set Repository Secret

Go to **GitHub > Repository > Settings > Secrets and variables > Actions** and add:

| Secret Name | Value |
|-------------|-------|
| `AZURE_STATIC_WEB_APPS_API_TOKEN` | The deployment token from Step 2 |

### Create Workflow

Create `.github/workflows/deploy-swa.yml`:

```yaml
name: Deploy to Azure Static Web Apps

on:
  push:
    branches: [main]
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches: [main]

jobs:
  build-and-deploy:
    if: github.event_name == 'push' || (github.event_name == 'pull_request' && github.event.action != 'closed')
    runs-on: ubuntu-latest
    name: Build and Deploy

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint --if-present

      - name: Run tests
        run: npm run test -- --run --if-present

      - name: Build
        run: npm run build
        env:
          VITE_API_URL: ${{ vars.VITE_API_URL || 'https://api.example.com' }}

      - name: Deploy to SWA
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: "upload"
          skip_app_build: true        # We already built above
          app_location: "/"
          output_location: "dist"

  close-pull-request:
    if: github.event_name == 'pull_request' && github.event.action == 'closed'
    runs-on: ubuntu-latest
    name: Close PR Staging Environment
    steps:
      - name: Close staging
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          action: "close"
```

### What This Workflow Does

| Trigger | Action |
|---------|--------|
| Push to `main` | Build + deploy to production |
| PR opened/updated | Build + deploy to a unique staging URL |
| PR closed | Tear down the staging environment |

Every pull request gets its own preview URL like `https://lively-river-0a1b2c3d4-{PR_NUMBER}.centralus.azurestaticapps.net`.

---

## 5. Environment Variables

### Build-Time Variables (Vite)

Vite exposes variables prefixed with `VITE_` to client code via `import.meta.env`.

In your React code:

```jsx
const apiUrl = import.meta.env.VITE_API_URL;
```

Set them in the workflow `env` block (see step 4) or in `.env.production`:

```
VITE_API_URL=https://api.example.com
VITE_APP_TITLE=My App
```

> **Warning**: These are embedded into the JS bundle at build time and visible to the client. Never put secrets here.

### Runtime Variables (SWA App Settings)

For backend/API environment variables (used by SWA managed functions):

```bash
az staticwebapp appsettings set \
  --name swa-my-vite-app \
  --resource-group rg-my-vite-app \
  --setting-names \
    "DATABASE_URL=mongodb+srv://..." \
    "API_KEY=sk-..."
```

These are server-side only and never exposed to the browser.

---

## 6. Custom Domain Setup

### Add a Custom Domain

```bash
# Add the custom domain
az staticwebapp hostname set \
  --name swa-my-vite-app \
  --resource-group rg-my-vite-app \
  --hostname www.example.com
```

### DNS Configuration

#### For Apex Domain (example.com)

| Type | Name | Value |
|------|------|-------|
| `ALIAS` or `ANAME` | `@` | `<your-swa>.azurestaticapps.net` |

> Not all DNS providers support ALIAS/ANAME for apex domains. If yours does not, use `www` and set up a redirect from apex.

#### For Subdomain (www.example.com)

| Type | Name | Value |
|------|------|-------|
| `CNAME` | `www` | `<your-swa>.azurestaticapps.net` |

### Verify and Enable SSL

```bash
# Check validation status (Azure provisions a free SSL certificate automatically)
az staticwebapp hostname list \
  --name swa-my-vite-app \
  --resource-group rg-my-vite-app \
  --output table
```

SSL is automatically provisioned and renewed — no manual certificate management needed.

---

## 7. Local Development with SWA CLI

Test the full SWA experience locally including auth emulation and API routing:

```bash
# Start Vite dev server + SWA emulator
swa start http://localhost:5173 --run "npm run dev"

# Or with a local API
swa start http://localhost:5173 --api-location ./api --run "npm run dev"
```

The SWA CLI emulator runs on `http://localhost:4280` and provides:
- Auth simulation (`.auth/login/github`, `.auth/me`)
- Routing rules from `staticwebapp.config.json`
- Proxy to your Vite dev server and local API

---

## 8. Complete File Reference

### package.json

```json
{
  "name": "my-vite-app",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint .",
    "swa:start": "swa start http://localhost:5173 --run \"npm run dev\"",
    "swa:deploy": "swa deploy dist --deployment-token $AZURE_STATIC_WEB_APPS_API_TOKEN"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router-dom": "^7.0.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.4.0",
    "eslint": "^9.0.0",
    "vite": "^6.0.0"
  }
}
```

### vite.config.js

```js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: false,
  },
  server: {
    port: 5173,
  },
});
```

### .env.production

```
VITE_API_URL=https://api.example.com
VITE_APP_TITLE=My Vite App
```

---

## 9. Troubleshooting

| Issue | Solution |
|-------|----------|
| 404 on page refresh | Add `navigationFallback` to `staticwebapp.config.json` (see step 3) |
| Assets not loading | Ensure `exclude` list in `navigationFallback` includes `/assets/*` |
| Custom domain not verifying | DNS propagation can take up to 48h; verify CNAME with `dig www.example.com CNAME` |
| Build fails in CI | Compare local Node version with CI — pin with `.nvmrc` or `engines` in `package.json` |
| Environment variables undefined | `VITE_` prefix is required for client access; set them in the `env:` block of the build step |
| SWA CLI deploy fails locally | Ensure token is valid: re-run `az staticwebapp secrets list` |
| PR preview not appearing | Check that the PR targets the branch configured in the workflow trigger |

---

## 10. Cost Summary

| Tier | Monthly Cost | Features |
|------|-------------|----------|
| **Free** | $0 | 2 custom domains, 0.5 GB storage, 100 GB bandwidth, built-in auth, PR preview environments |
| **Standard** | ~$9/month | 5 custom domains, 2 GB storage, 100 GB bandwidth, managed functions, SLA, private endpoints |

For most Vite + React SPAs, the **Free tier** is sufficient for production.
