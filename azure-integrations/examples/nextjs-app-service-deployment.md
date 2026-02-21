# End-to-End: Deploy a Next.js App to Azure App Service

Complete walkthrough from zero to production with CI/CD, Key Vault integration, Application Insights, and Azure Storage for file uploads.

---

## Prerequisites

- [Node.js 20+](https://nodejs.org) and npm/pnpm
- [Azure CLI](https://aka.ms/install-azure-cli) installed and logged in (`az login`)
- A GitHub repository with your Next.js project
- An Azure subscription (free tier works)

---

## 1. Project Structure

```
my-nextjs-app/
├── public/
│   └── favicon.svg
├── src/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── middleware.js
├── .github/
│   └── workflows/
│       └── deploy-appservice.yml    ← CI/CD workflow
├── infra/
│   └── main.bicep                 ← Infrastructure as code
├── appsettings.local.json            ← Local environment variables
├── package.json
├── next.config.js
└── next-env.d.ts
```

---

## 2. Azure Resource Setup

### Option A: Azure CLI (Step-by-Step)

```bash
# Variables
RG_NAME="rg-recipe-app"
LOCATION="eastus"
APP_NAME="kitchen-odyssey"
APP_SERVICE_PLAN="${APP_NAME}-plan"
STORAGE_ACCOUNT="${APP_NAME}stg"
KEY_VAULT="${APP_NAME}-kv"
COSMOS_DB="${APP_NAME}-db"

# 1. Create resource group
az group create --name $RG_NAME --location $LOCATION

# 2. Create App Service Plan (Linux, B1 tier)
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RG_NAME \
  --location $LOCATION \
  --is-linux \
  --sku B1

# 3. Create Web App (Node.js 20)
az webapp create \
  --name $APP_NAME \
  --resource-group $RG_NAME \
  --plan $APP_SERVICE_PLAN \
  --runtime "NODE|20-lts"

# 4. Enable Application Insights
APPINSIGHTS_NAME="${APP_NAME}-ai"
az monitor app-insights component create \
  --app $APPINSIGHTS_NAME \
  --location $LOCATION \
  --resource-group $RG_NAME \
  --application-type web
APPINSIGHTS_KEY=$(az monitor app-insights component show \
  --app $APPINSIGHTS_NAME \
  --resource-group $RG_NAME \
  --query instrumentationKey -o tsv)

# 5. Create Storage Account for file uploads
az storage account create \
  --name $STORAGE_ACCOUNT \
  --resource-group $RG_NAME \
  --location $LOCATION \
  --sku Standard_LRS \
  --kind StorageV2

# 6. Create container for recipe images
az storage container create \
  --name recipe-images \
  --account-name $STORAGE_ACCOUNT \
  --auth-mode login

# 7. Create Key Vault for secrets
az keyvault create \
  --name $KEY_VAULT \
  --resource-group $RG_NAME \
  --location $LOCATION

# 8. Create Cosmos DB (MongoDB API)
az cosmosdb create \
  --name $COSMOS_DB \
  --resource-group $RG_NAME \
  --location $LOCATION \
  --kind MongoDB

# 9. Get connection strings
MONGODB_URI=$(az cosmosdb keys list \
  --name $COSMOS_DB \
  --resource-group $RG_NAME \
  --query connectionStrings[0].connectionString -o tsv)

STORAGE_CONNECTION=$(az storage account show-connection-string \
  --name $STORAGE_ACCOUNT \
  --resource-group $RG_NAME \
  --query connectionString -o tsv)

# 10. Store secrets in Key Vault (you'll upload MongoDB password securely)
az keyvault secret set \
  --vault-name $KEY_VAULT \
  --name "MongoDB-Uri" \
  --value "$MONGODB_URI"

az keyvault secret set \
  --vault-name $KEY_VAULT \
  --name "AppInsights-InstrumentationKey" \
  --value "$APPINSIGHTS_KEY"

az keyvault secret set \
  --vault-name $KEY_VAULT \
  --name "Storage-ConnectionString" \
  --value "$STORAGE_CONNECTION"

# 11. Generate NEXTAUTH_SECRET
NEXTAUTH_SECRET=$(openssl rand -base64 32)
az keyvault secret set \
  --vault-name $KEY_VAULT \
  --name "NextAuth-Secret" \
  --value "$NEXTAUTH_SECRET"

# 12. Enable Managed Identity for Web App
az webapp identity assign \
  --name $APP_NAME \
  --resource-group $RG_NAME

# 13. Get Managed Identity Principal ID
PRINCIPAL_ID=$(az webapp identity show \
  --name $APP_NAME \
  --resource-group $RG_NAME \
  --query principalId -o tsv)

# 14. Grant Managed Identity access to Key Vault
az keyvault set-policy \
  --name $KEY_VAULT \
  --resource-group $RG_NAME \
  --object-id $PRINCIPAL_ID \
  --secret-permissions get list

# 15. Grant Managed Identity access to Storage
STORAGE_ID=$(az storage account show \
  --name $STORAGE_ACCOUNT \
  --resource-group $RG_NAME \
  --query id -o tsv)
az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role "Storage Blob Data Contributor" \
  --scope $STORAGE_ID

echo "Deployment complete! Your app URL: https://$APP_NAME.azurewebsites.net"
```

### Option B: Bicep Template

Create `infra/main.bicep`:

```bicep
@description('Name of the application')
param appName string

@description('Location for all resources')
param location string = resourceGroup().location

@description('App Service Plan SKU')
@allowed(['B1', 'B2', 'B3', 'S1', 'S2', 'S3', 'P1V3', 'P2V3'])
param sku string = 'B1'

@description('MongoDB Atlas connection string (will be stored in Key Vault)')
@secure()
param mongoDbConnectionString string

var appServicePlanName = '${appName}-plan'
var storageAccountName = toLower('${appName}${uniqueString(resourceGroup().id)}stg')
var keyVaultName = '${appName}${uniqueString(resourceGroup().id)}kv'
var cosmosDbName = '${appName}db'
var appInsightsName = '${appName}ai'

// App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: sku
    size: sku
    tier: sku[0] == 'P' ? 'Premium' : (sku[0] == 'S' ? 'Standard' : 'Basic')
  }
  properties: {
    reserved: true
  }
  kind: 'linux'
}

// Web App
resource webApp 'Microsoft.Web/sites@2023-01-01' = {
  name: appName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'NODE|20-lts'
      alwaysOn: sku[0] == 'S' || sku[0] == 'P'
      appSettings: [
        { name: 'AZURE_KEYVAULT_RESOURCEENDPOINT', value: keyVault.properties.vaultUri }
        { name: 'AZURE_CLIENTID', value: managedIdentity.properties.clientId }
        { name: 'NEXTAUTH_URL', value: 'https://${appName}.azurewebsites.net' }
        { name: 'NODE_ENV', value: 'production' }
        { name: 'APPLICATIONINSIGHTS_CONNECTION_STRING', value: 'InstrumentationKey=${appInsights.properties.InstrumentationKey}' }
      ]
    }
  }
}

// Managed Identity
resource managedIdentity 'Microsoft.Web/sites/config@2023-01-01' = {
  name: '${appName}/web'
  resourceGroup: resourceGroup()
  properties: {
    managedServiceIdentityId: webApp.identity.principalId
  }
}

// Application Insights
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    Flow_Type: 'Bluefield'
    IngestionMode: 'ApplicationInsights'
  }
}

// Storage Account for file uploads
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  properties: {
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
  }
}

// Container for recipe images
resource imagesContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  parent: storageAccount
  name: 'default/recipe-images'
  properties: {
    publicAccess: 'None'
  }
}

// Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  properties: {
    sku: { family: 'A', name: 'standard' }
    tenantId: subscription().tenantId
    enablePurgeProtection: true
    enableSoftDelete: true
    enabledForDeployment: true
    enabledForTemplateDeployment: true
    enabledForDiskEncryption: true
  }
}

// Cosmos DB (MongoDB API)
resource cosmosDb 'Microsoft.DocumentDB/databaseAccounts@2023-04-15' = {
  name: cosmosDbName
  location: location
  kind: 'MongoDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    capabilities: [{ name: 'EnableMongo' }]
    locations: [{ locationName: location, failoverPriority: 0 }]
  }
}

// Store MongoDB URI in Key Vault
resource mongoDbSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  name: '${keyVaultName}/MongoDB-Uri'
  properties: {
    value: mongoDbConnectionString
  }
}

// Store App Insights Key in Key Vault
resource appInsightsSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  name: '${keyVaultName}/AppInsights-InstrumentationKey'
  properties: {
    value: appInsights.properties.InstrumentationKey
  }
}

// Store Storage Connection String in Key Vault
resource storageSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  name: '${keyVaultName}/Storage-ConnectionString'
  properties: {
    value: listKeys(storageAccount.id, storageAccount.apiVersion).keys[0].value
  }
}

// Grant Managed Identity access to Key Vault
resource keyVaultAccess 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(webApp.identity.principalId, keyVault.id, 'kv-access')
  scope: keyVault
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '4633458b-17de-408a-b874-0445c86b69e6'
    ) // Key Vault Secrets User
    principalId: webApp.identity.principalId
  }
}

// Grant Managed Identity access to Storage
resource storageAccess 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(webApp.identity.principalId, storageAccount.id, 'storage-access')
  scope: storageAccount
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
    ) // Storage Blob Data Contributor
    principalId: webApp.identity.principalId
  }
}

output appUrl string = 'https://${webApp.properties.defaultHostName}'
output keyVaultUri string = keyVault.properties.vaultUri
```

Deploy:

```bash
# Get MongoDB connection string (you'll provide this)
MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/kitchenodyssey"

az deployment group create \
  --name deploy-recipe-app \
  --resource-group rg-recipe-app \
  --template-file infra/main.bicep \
  --parameters \
    appName=kitchen-odyssey \
    location=eastus \
    sku=B1 \
    mongoDbConnectionString=$MONGODB_URI
```

---

## 3. Next.js Configuration

### next.config.js (Production)

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.azurewebsites.net',
        port: '',
        pathname: '/api/image/**',
      },
      {
        protocol: 'https',
        hostname: '**.blob.core.windows.net',
        port: '',
        pathname: '/recipe-images/**',
      },
    ],
  },
  env: {
    NEXTAUTH_URL: process.env.NEXTAUTH_URL || 'https://localhost:3000',
  },
  headers() {
    return [
      {
        source: '/:path*',
        headers: [
          { key: 'X-Frame-Options', value: 'DENY' },
          { key: 'X-Content-Type-Options', value: 'nosniff' },
          { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
```

### Key Vault Integration (lib/azure-keyvault.js)

```javascript
// Install: npm install @azure/identity @azure/keyvault-secrets
import { DefaultAzureCredential } from '@azure/identity';
import { SecretClient } from '@azure/keyvault-secrets';

const credential = new DefaultAzureCredential();
const keyVaultName = process.env.AZURE_KEYVAULT_NAME || 'kitchen-odysseykv';
const keyVaultUrl = `https://${keyVaultName}.vault.azure.net`;

const client = new SecretClient(keyVaultUrl, credential);

export async function getSecret(secretName) {
  try {
    const secret = await client.getSecret(secretName);
    return secret.value;
  } catch (error) {
    console.error(`Error retrieving secret ${secretName}:`, error);
    throw error;
  }
}

// Preload secrets at startup
export async function loadAzureSecrets() {
  try {
    const [
      mongoUri,
      storageConn,
      nextAuthSecret,
      appInsightsKey,
    ] = await Promise.all([
      getSecret('MongoDB-Uri'),
      getSecret('Storage-ConnectionString'),
      getSecret('NextAuth-Secret'),
      getSecret('AppInsights-InstrumentationKey'),
    ]);

    return {
      MONGODB_URI: mongoUri,
      AZURE_STORAGE_CONNECTION_STRING: storageConn,
      NEXTAUTH_SECRET: nextAuthSecret,
      APPLICATIONINSIGHTS_CONNECTION_STRING: `InstrumentationKey=${appInsightsKey}`,
    };
  } catch (error) {
    console.error('Failed to load Azure secrets:', error);
    throw error;
  }
}
```

### lib/mongodb.js (with Key Vault)

```javascript
import mongoose from 'mongoose';
import { loadAzureSecrets } from './azure-keyvault';

let isConnected = false;

export async function connectToDatabase() {
  if (isConnected) {
    return mongoose;
  }

  // Load MongoDB URI from Key Vault in production
  const secrets = process.env.NODE_ENV === 'production'
    ? await loadAzureSecrets()
    : {
        MONGODB_URI: process.env.MONGODB_URI,
      };

  await mongoose.connect(secrets.MONGODB_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  });

  isConnected = true;
  console.log('Connected to MongoDB');
  return mongoose;
}
```

---

## 4. GitHub Actions CI/CD Pipeline

### Set Repository Secrets

Go to **GitHub > Repository > Settings > Secrets and variables > Actions** and add:

| Secret Name | Value |
|-------------|-------|
| `AZURE_SUBSCRIPTION_ID` | Your Azure subscription ID |
| `AZURE_TENANT_ID` | Your Azure AD tenant ID |
| `AZURE_CLIENT_ID` | Service Principal client ID (for OIDC) |

### Create Workflow

Create `.github/workflows/deploy-appservice.yml`:

```yaml
name: Deploy Next.js to Azure App Service

on:
  push:
    branches: [main, staging]
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches: [main]

permissions:
  id-token: write   # Required for OIDC
  contents: read

env:
  NODE_VERSION: '20'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - run: npm ci
      - run: npm run lint --if-present
      - run: npm run test --if-present

  deploy-staging:
    needs: test
    if: github.ref == 'refs/heads/staging'
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: ${{ steps.deploy.outputs.webapp-url }}

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - run: npm ci
      - run: npm run build

      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Deploy to Staging
        id: deploy
        uses: azure/webapps-deploy@v3
        with:
          app-name: kitchen-odyssey-staging
          package: .

      - name: Monitor deployment
        run: |
          echo "Staging URL: https://kitchen-odyssey-staging.azurewebsites.net"

  deploy-production:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: ${{ steps.deploy.outputs.webapp-url }}

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - run: npm ci
      - run: npm run build

      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Deploy to Production
        id: deploy
        uses: azure/webapps-deploy@v3
        with:
          app-name: kitchen-odyssey
          package: .

      - name: Health check
        run: |
          sleep 30
          curl -f https://kitchen-odyssey.azurewebsites.net/api/health || exit 1

      - name: Rollback on failure
        if: failure()
        uses: azure/webapps-deploy-action@v2
        with:
          app-name: kitchen-odyssey
          slot-name: staging
```

---

## 5. Deployment Slots (Optional for Blue-Green)

Enable deployment slots for zero-downtime deployments:

```bash
# Enable deployment slots on App Service
az webapp deployment slot create \
  --name kitchen-odyssey \
  --resource-group rg-recipe-app \
  --slot staging

# Configure staging slot settings
az webapp config appsettings set \
  --name kitchen-odyssey-slots-staging \
  --resource-group rg-recipe-app \
  --settings \
    NODE_ENV=staging \
    NEXTAUTH_URL=https://kitchen-odyssey-staging.azurewebsites.net
```

Updated workflow for slot deployment:

```yaml
- name: Deploy to Staging Slot
  uses: azure/webapps-deploy@v3
  with:
    app-name: kitchen-odyssey
    slot-name: staging
    package: .

- name: Swap with Production
  if: github.ref == 'refs/heads/main'
  run: |
    az webapp deployment slot swap \
      --name kitchen-odyssey \
      --resource-group rg-recipe-app \
      --slot staging \
      --target-slot production
```

---

## 6. Monitoring with Application Insights

### Install SDK

```bash
npm install @azure/monitor-opentelemetry
```

### Initialize Telemetry (lib/appinsights.js)

```javascript
import { useAzureAppInsights } from '@azure/monitor-opentelemetry';

useAzureAppInsights({
  connectionString: process.env.APPLICATIONINSIGHTS_CONNECTION_STRING,
});

export default {
  trackEvent: (name, properties) => {
    // Application Insights auto-tracks events
  },
  trackException: (error) => {
    // Application Insights auto-tracks exceptions
  },
  trackDependency: (name, data) => {
    // Application Insights auto-tracks dependencies
  },
};
```

### Custom Metrics

```javascript
// Track recipe views
import telemetry from './appinsights';

export async function recordRecipeView(recipeId, userId) {
  telemetry.trackEvent('RecipeViewed', {
    recipeId,
    userId,
    timestamp: new Date().toISOString(),
  });
}

// Track user registration
export async function recordUserRegistration(userId, role) {
  telemetry.trackEvent('UserRegistered', {
    userId,
    role,
    timestamp: new Date().toISOString(),
  });
}
```

---

## 7. Azure Storage Integration for File Uploads

### Upload Helper (lib/azure-storage.js)

```javascript
// npm install @azure/storage-blob
import { BlobServiceClient } from '@azure/storage-blob';
import { getSecret } from './azure-keyvault';

let blobServiceClient;

async function getBlobServiceClient() {
  if (!blobServiceClient) {
    const connectionString = await getSecret('Storage-ConnectionString');
    blobServiceClient = BlobServiceClient.fromConnectionString(connectionString);
  }
  return blobServiceClient;
}

export async function uploadRecipeImage(fileBuffer, fileName, contentType) {
  const blobServiceClient = await getBlobServiceClient();
  const containerClient = blobServiceClient.getContainerClient('recipe-images');

  await containerClient.createIfNotExists({ access: 'blob' });

  const blockBlobClient = containerClient.getBlockBlobClient(`${Date.now()}-${fileName}`);
  await blockBlobClient.uploadData(fileBuffer, {
    blobHTTPHeaders: { blobContentType: contentType },
    metadata: {
      uploadedAt: new Date().toISOString(),
    },
  });

  return blockBlobClient.url;
}

export async function deleteRecipeImage(blobName) {
  const blobServiceClient = await getBlobServiceClient();
  const containerClient = blobServiceClient.getContainerClient('recipe-images');
  const blockBlobClient = containerClient.getBlockBlobClient(blobName);

  await blockBlobClient.deleteIfExists();
}

export async function generateImageUrl(blobName, expiresInMinutes = 60) {
  const blobServiceClient = await getBlobServiceClient();
  const containerClient = blobServiceClient.getContainerClient('recipe-images');
  const blobClient = containerClient.getBlobClient(blobName);

  const sasUrl = await blobClient.generateSasUrl({
    permissions: { read: true },
    expiresOn: new Date(Date.now() + expiresInMinutes * 60 * 1000),
  });

  return sasUrl;
}
```

### API Route for Image Upload (app/api/upload/route.js)

```javascript
import { NextResponse } from 'next/server';
import { uploadRecipeImage } from '@/lib/azure-storage';

export async function POST(request) {
  try {
    const formData = await request.formData();
    const file = formData.get('image');

    if (!file) {
      return NextResponse.json({ error: 'No file provided' }, { status: 400 });
    }

    const buffer = Buffer.from(await file.arrayBuffer());
    const fileName = file.name;
    const contentType = file.type;

    const imageUrl = await uploadRecipeImage(buffer, fileName, contentType);

    return NextResponse.json({ imageUrl }, { status: 201 });
  } catch (error) {
    console.error('Upload error:', error);
    return NextResponse.json({ error: 'Upload failed' }, { status: 500 });
  }
}
```

---

## 8. Troubleshooting

### Common Issues

#### Issue: "Error: Cannot find module './azure-keyvault'"
**Cause:** Missing Azure SDK packages
**Solution:**
```bash
npm install @azure/identity @azure/keyvault-secrets
```

#### Issue: Managed Identity cannot access Key Vault
**Cause:** Missing role assignment or firewall blocking
**Solution:**
```bash
# Check role assignments
az role assignment list \
  --assignee <PRINCIPAL_ID> \
  --scope /subscriptions/<SUB_ID>/resourceGroups/<RG> \
  --query [].[roleDefinitionName,principalId]

# Ensure Key Vault network allows trusted Microsoft services
az keyvault update \
  --name $KEY_VAULT \
  --resource-group $RG \
  --default-action Allow
```

#### Issue: Cold start latency (20-30 seconds)
**Cause:** App Service sleeping on free/basic tier
**Solution:**
```bash
# Upgrade to Standard plan with Always On enabled
az appservice plan update \
  --name $APP_SERVICE_PLAN \
  --resource-group $RG \
  --sku S1
```

#### Issue: Image uploads failing with CORS error
**Cause:** CORS not configured on Storage Account
**Solution:**
```bash
az storage cors clear \
  --account-name $STORAGE_ACCOUNT \
  --account-key <ACCOUNT_KEY>

az storage cors add \
  --account-name $STORAGE_ACCOUNT \
  --account-key <ACCOUNT_KEY> \
  --services b \
  --methods PUT GET DELETE OPTIONS \
  --origins "https://kitchen-odyssey.azurewebsites.net" \
  --allowed-headers "*" \
  --exposed-headers "*"
```

#### Issue: Environment variables not loading in App Service
**Cause:** App Settings not configured or Key Vault Reference error
**Solution:**
```bash
# Check current app settings
az webapp config appsettings list \
  --name kitchen-odyssey \
  --resource-group rg-recipe-app \
  --query [].[name,value]

# Verify Managed Identity is enabled
az webapp identity show \
  --name kitchen-odyssey \
  --resource-group rg-recipe-app

# Test Key Vault access locally (requires Azure CLI login)
az keyvault secret show \
  --name MongoDB-Uri \
  --vault-name kitchen-odysseykv
```

#### Issue: Application Insights not receiving telemetry
**Cause:** Missing connection string or SDK not initialized
**Solution:**
```javascript
// Verify connection string is set
console.log('App Insights Connection:', process.env.APPLICATIONINSIGHTS_CONNECTION_STRING?.substring(0, 20) + '...');

// Check telemetry in Azure Portal
# Navigate to: Application Insights > Logs
# Run query: traces | where timestamp > ago(1h) | project timestamp, message
```

---

## 9. Best Practices

### Security
- ✅ Always use Managed Identity (never store connection strings in app settings)
- ✅ Enable HTTPS Only on App Service
- ✅ Use Key Vault for all secrets and sensitive data
- ✅ Regularly rotate MongoDB Atlas credentials
- ✅ Enable App Service authentication (Azure AD, GitHub OAuth)
- ✅ Set up IP restrictions and VNet integration for production

### Performance
- ✅ Use Always On for consistent response times (Standard+ tier)
- ✅ Configure scaling rules based on CPU/memory metrics
- ✅ Use CDN for serving static assets
- ✅ Optimize images before upload to reduce storage costs

### Monitoring
- ✅ Set up alerts in Application Insights (response time, error rate, failed requests)
- ✅ Enable App Service diagnostic logs
- ✅ Configure log archiving to Azure Storage
- ✅ Create dashboards in Azure Monitor

### Cost Optimization
- ✅ Use App Service Plan cost calculator for right-sizing
- ✅ Enable auto-scaling to manage peak vs. off-peak traffic
- ✅ Clean up old resources in non-production environments
- ✅ Use lifecycle policies for Storage Account cleanup

---

## 10. Deployment Checklist

Before deploying to production:

- [ ] All CI/CD tests passing
- [ ] Environment variables configured in Key Vault
- [ ] Managed Identity has correct role assignments
- [ ] Application Insights configured and receiving telemetry
- [ ] Storage Account CORS rules set up
- [ ] Custom domain configured (if applicable)
- [ ] SSL certificate installed for custom domain
- [ ] Deployment slots enabled for zero-downtime updates
- [ ] Backup strategy configured
- [ ] Monitoring alerts created
- [ ] Security best practices reviewed

---

## Reference Documentation

- [Azure App Service Documentation](https://learn.microsoft.com/azure/app-service/)
- [Azure Key Vault Documentation](https://learn.microsoft.com/azure/key-vault/)
- [Azure Storage Documentation](https://learn.microsoft.com/azure/storage/)
- [Application Insights Documentation](https://learn.microsoft.com/azure/azure-monitor/app/app-insights-overview)
- [Bicep Language Reference](https://learn.microsoft.com/azure/azure-resource-manager/bicep/)
