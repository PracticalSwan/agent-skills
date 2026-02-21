# GitHub Actions for Azure Deployment Patterns

Workflows, actions, and patterns for deploying to Azure services from GitHub Actions.

---

## Authentication

### OIDC Federated Credentials (Recommended)

No secrets stored in GitHub — uses short-lived tokens via Azure AD workload identity federation.

#### 1. Create Azure AD App Registration + Federated Credential

```bash
# Create app registration
az ad app create --display-name "github-deploy-myapp"
APP_ID=$(az ad app list --display-name "github-deploy-myapp" --query "[0].appId" -o tsv)
OBJECT_ID=$(az ad app list --display-name "github-deploy-myapp" --query "[0].id" -o tsv)

# Create service principal
az ad sp create --id $APP_ID
SP_OBJECT_ID=$(az ad sp list --filter "appId eq '$APP_ID'" --query "[0].id" -o tsv)

# Assign Contributor role on resource group
az role assignment create \
  --assignee $SP_OBJECT_ID \
  --role "Contributor" \
  --scope "/subscriptions/<SUB_ID>/resourceGroups/<RG_NAME>"

# Add federated credential for GitHub Actions (main branch)
az ad app federated-credential create --id $OBJECT_ID --parameters '{
  "name": "github-main",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:<OWNER>/<REPO>:ref:refs/heads/main",
  "audiences": ["api://AzureADTokenExchange"]
}'

# Add federated credential for pull requests (optional)
az ad app federated-credential create --id $OBJECT_ID --parameters '{
  "name": "github-pr",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:<OWNER>/<REPO>:pull_request",
  "audiences": ["api://AzureADTokenExchange"]
}'

# Add federated credential for an environment
az ad app federated-credential create --id $OBJECT_ID --parameters '{
  "name": "github-production",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:<OWNER>/<REPO>:environment:production",
  "audiences": ["api://AzureADTokenExchange"]
}'
```

#### 2. GitHub Repository Secrets

Set these in **Settings > Secrets and variables > Actions**:

| Secret | Value |
|--------|-------|
| `AZURE_CLIENT_ID` | App registration Application (client) ID |
| `AZURE_TENANT_ID` | Azure AD tenant ID |
| `AZURE_SUBSCRIPTION_ID` | Target subscription ID |

#### 3. Workflow Login Step (OIDC)

```yaml
permissions:
  id-token: write   # Required for OIDC
  contents: read

steps:
  - name: Azure Login (OIDC)
    uses: azure/login@v2
    with:
      client-id: ${{ secrets.AZURE_CLIENT_ID }}
      tenant-id: ${{ secrets.AZURE_TENANT_ID }}
      subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

### Service Principal with Secret (Legacy)

```yaml
steps:
  - name: Azure Login
    uses: azure/login@v2
    with:
      creds: ${{ secrets.AZURE_CREDENTIALS }}
      # AZURE_CREDENTIALS is a JSON object:
      # {
      #   "clientId": "...",
      #   "clientSecret": "...",
      #   "subscriptionId": "...",
      #   "tenantId": "..."
      # }
```

---

## Azure Static Web Apps

### Deploy with SWA CLI (Vite / React / Next.js)

```yaml
name: Deploy Static Web App

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
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install and Build
        run: |
          npm ci
          npm run build

      - name: Deploy to Azure Static Web Apps
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: "upload"
          app_location: "/"
          output_location: "dist"
          # api_location: "api"  # Uncomment if using managed API

  close-pr:
    if: github.event_name == 'pull_request' && github.event.action == 'closed'
    runs-on: ubuntu-latest
    name: Close PR Environment
    steps:
      - name: Close staging environment
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          action: "close"
```

### Deploy Next.js to Static Web Apps (Hybrid)

```yaml
name: Deploy Next.js to SWA

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - run: npm ci
      - run: npm run build

      - name: Deploy
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: "upload"
          app_location: "/"
          output_location: ".next"
          # Next.js hybrid rendering on SWA requires Standard plan
```

---

## Azure App Service (Node.js)

### Basic Deployment

```yaml
name: Deploy to App Service

on:
  push:
    branches: [main]

permissions:
  id-token: write
  contents: read

env:
  AZURE_WEBAPP_NAME: my-node-app
  NODE_VERSION: '20'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install and build
        run: |
          npm ci
          npm run build --if-present

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: node-app
          path: .
          include-hidden-files: true

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: production
      url: ${{ steps.deploy.outputs.webapp-url }}

    steps:
      - name: Download artifact
        uses: actions/download-artifact@v4
        with:
          name: node-app

      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Deploy to App Service
        id: deploy
        uses: azure/webapps-deploy@v3
        with:
          app-name: ${{ env.AZURE_WEBAPP_NAME }}
```

### Deployment Slots (Blue-Green)

```yaml
name: Deploy with Staging Slot

on:
  push:
    branches: [main]

permissions:
  id-token: write
  contents: read

env:
  AZURE_WEBAPP_NAME: my-node-app
  SLOT_NAME: staging

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci && npm run build --if-present
      - uses: actions/upload-artifact@v4
        with:
          name: app
          path: .
          include-hidden-files: true

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: ${{ steps.deploy.outputs.webapp-url }}
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: app

      - uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Deploy to staging slot
        id: deploy
        uses: azure/webapps-deploy@v3
        with:
          app-name: ${{ env.AZURE_WEBAPP_NAME }}
          slot-name: ${{ env.SLOT_NAME }}

      - name: Smoke test staging
        run: |
          STAGING_URL="https://${{ env.AZURE_WEBAPP_NAME }}-${{ env.SLOT_NAME }}.azurewebsites.net"
          STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$STAGING_URL/health")
          if [ "$STATUS" != "200" ]; then
            echo "Smoke test failed with status $STATUS"
            exit 1
          fi
          echo "Smoke test passed"

  swap-to-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment:
      name: production
    steps:
      - uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Swap staging to production
        run: |
          az webapp deployment slot swap \
            --name ${{ env.AZURE_WEBAPP_NAME }} \
            --resource-group ${{ vars.AZURE_RG }} \
            --slot ${{ env.SLOT_NAME }} \
            --target-slot production
```

---

## Azure Functions

### Deploy Node.js Function App

```yaml
name: Deploy Azure Functions

on:
  push:
    branches: [main]
    paths:
      - 'api/**'

permissions:
  id-token: write
  contents: read

env:
  FUNCTION_APP_NAME: my-functions
  NODE_VERSION: '20'
  PACKAGE_PATH: 'api'

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
          cache-dependency-path: '${{ env.PACKAGE_PATH }}/package-lock.json'

      - name: Install and build
        working-directory: ${{ env.PACKAGE_PATH }}
        run: |
          npm ci
          npm run build --if-present

      - uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Deploy to Azure Functions
        uses: Azure/functions-action@v1
        with:
          app-name: ${{ env.FUNCTION_APP_NAME }}
          package: ${{ env.PACKAGE_PATH }}
```

---

## Multi-Stage Deployment Pipeline

### Full CI/CD: Test → Build → Deploy Staging → Deploy Production

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

permissions:
  id-token: write
  contents: read
  checks: write
  pull-requests: write

env:
  NODE_VERSION: '20'
  AZURE_WEBAPP_NAME: my-app

jobs:
  # ─── Stage 1: Lint + Test ───
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - run: npm ci
      - run: npm run lint
      - run: npm run test -- --coverage

      - name: Upload coverage
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage/

  # ─── Stage 2: Build ───
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - run: npm ci
      - run: npm run build

      - uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: |
            dist/
            package.json
            package-lock.json
          retention-days: 3

  # ─── Stage 3: Deploy to Staging (develop and main) ───
  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://${{ env.AZURE_WEBAPP_NAME }}-staging.azurewebsites.net
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build-output

      - uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - uses: azure/webapps-deploy@v3
        with:
          app-name: ${{ env.AZURE_WEBAPP_NAME }}
          slot-name: staging

  # ─── Stage 4: Deploy to Production (main only) ───
  deploy-production:
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://${{ env.AZURE_WEBAPP_NAME }}.azurewebsites.net
    steps:
      - uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Swap staging → production
        run: |
          az webapp deployment slot swap \
            --name ${{ env.AZURE_WEBAPP_NAME }} \
            --resource-group ${{ vars.AZURE_RG }} \
            --slot staging \
            --target-slot production
```

---

## Infrastructure as Code Deployment

### Deploy Bicep Templates

```yaml
name: Deploy Infrastructure

on:
  push:
    branches: [main]
    paths:
      - 'infra/**'
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        default: 'dev'
        type: choice
        options: [dev, staging, prod]

permissions:
  id-token: write
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Validate Bicep
        run: az bicep build --file infra/main.bicep

      - name: What-if
        run: |
          az deployment group what-if \
            --resource-group ${{ vars.AZURE_RG }} \
            --template-file infra/main.bicep \
            --parameters infra/parameters.${{ inputs.environment || 'dev' }}.json

  deploy:
    needs: validate
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment || 'dev' }}
    steps:
      - uses: actions/checkout@v4
      - uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Deploy infrastructure
        uses: azure/arm-deploy@v2
        with:
          resourceGroupName: ${{ vars.AZURE_RG }}
          template: infra/main.bicep
          parameters: infra/parameters.${{ inputs.environment || 'dev' }}.json
          failOnStdErr: false
```

---

## Environment Secrets and Variables

### Organization-Level (Shared)

Set in **Organization Settings > Secrets and variables > Actions**:

- `AZURE_TENANT_ID` — Shared across all repos in the org
- `AZURE_SUBSCRIPTION_ID` — Shared subscription

### Repository-Level

Set in **Repository Settings > Secrets and variables > Actions**:

- `AZURE_CLIENT_ID` — Per-repo app registration
- `AZURE_STATIC_WEB_APPS_API_TOKEN` — SWA deployment token

### Environment-Level

Set in **Repository Settings > Environments > (env name) > Secrets**:

- Per-environment overrides (e.g., different `AZURE_CLIENT_ID` per environment)
- Protection rules: required reviewers, wait timer, branch restrictions

### Using Variables (Non-Sensitive)

```yaml
# Repository or environment variables (not secrets)
env:
  AZURE_RG: ${{ vars.AZURE_RG }}           # from vars, not secrets
  AZURE_LOCATION: ${{ vars.AZURE_LOCATION }}
```

---

## Reusable Workflows

### Callable Deploy Workflow

```yaml
# .github/workflows/deploy-reusable.yml
name: Reusable Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      app-name:
        required: true
        type: string
      slot-name:
        required: false
        type: string
        default: 'production'
    secrets:
      AZURE_CLIENT_ID:
        required: true
      AZURE_TENANT_ID:
        required: true
      AZURE_SUBSCRIPTION_ID:
        required: true

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: ${{ inputs.environment }}
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build-output

      - uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - uses: azure/webapps-deploy@v3
        with:
          app-name: ${{ inputs.app-name }}
          slot-name: ${{ inputs.slot-name }}
```

### Calling Reusable Workflow

```yaml
# .github/workflows/ci-cd.yml
jobs:
  build:
    # ... build steps ...

  deploy-staging:
    needs: build
    uses: ./.github/workflows/deploy-reusable.yml
    with:
      environment: staging
      app-name: my-app
      slot-name: staging
    secrets:
      AZURE_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
      AZURE_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
      AZURE_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

  deploy-production:
    needs: deploy-staging
    uses: ./.github/workflows/deploy-reusable.yml
    with:
      environment: production
      app-name: my-app
    secrets:
      AZURE_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
      AZURE_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
      AZURE_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

---

## Key GitHub Actions for Azure

| Action | Version | Purpose |
|--------|---------|---------|
| `azure/login` | `v2` | Authenticate to Azure (OIDC or SP) |
| `azure/webapps-deploy` | `v3` | Deploy to App Service |
| `azure/functions-action` | `v1` | Deploy to Azure Functions |
| `Azure/static-web-apps-deploy` | `v1` | Deploy to Static Web Apps |
| `azure/arm-deploy` | `v2` | Deploy Bicep/ARM templates |
| `azure/cli` | `v2` | Run arbitrary Azure CLI commands |
| `azure/docker-login` | `v2` | Login to ACR |
| `azure/container-apps-deploy-action` | `v1` | Deploy to Container Apps |
