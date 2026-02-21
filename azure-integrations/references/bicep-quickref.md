# Bicep Template Quick Reference

Comprehensive reference for Azure Bicep — the declarative DSL for deploying Azure resources.

---

## Fundamentals

### Target Scope

```bicep
targetScope = 'resourceGroup' // default
// Also: 'subscription', 'managementGroup', 'tenant'
```

### Parameters

```bicep
@description('Name of the application')
@minLength(3)
@maxLength(24)
param appName string

@description('Deployment environment')
@allowed(['dev', 'staging', 'prod'])
param environment string = 'dev'

@secure()
param adminPassword string

param tags object = {
  environment: environment
  managedBy: 'bicep'
}

param allowedIPs array = []

param enableMonitoring bool = true

param instanceCount int = 1
```

### Variables

```bicep
var resourcePrefix = '${appName}-${environment}'
var location = resourceGroup().location
var uniqueSuffix = uniqueString(resourceGroup().id)
var storageName = toLower('st${replace(resourcePrefix, '-', '')}${uniqueSuffix}')
```

### Outputs

```bicep
output appUrl string = 'https://${webApp.properties.defaultHostName}'
output resourceId string = webApp.id
output storageEndpoint string = storageAccount.properties.primaryEndpoints.blob

// Typed object output
output connectionInfo object = {
  host: webApp.properties.defaultHostName
  resourceGroup: resourceGroup().name
}
```

---

## Resource Declarations

### Basic Pattern

```bicep
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageName
  location: location
  tags: tags
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
  }
}
```

### Existing Keyword (Reference Pre-existing Resources)

```bicep
resource existingVnet 'Microsoft.Network/virtualNetworks@2023-11-01' existing = {
  name: 'my-existing-vnet'
  scope: resourceGroup('networking-rg')
}

resource existingKeyVault 'Microsoft.KeyVault/vaults@2023-07-01' existing = {
  name: keyVaultName
}
```

### Child Resources

```bicep
// Inline child
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageName
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  properties: {}

  resource blobService 'blobServices' = {
    name: 'default'

    resource container 'containers' = {
      name: 'app-data'
      properties: {
        publicAccess: 'None'
      }
    }
  }
}

// Separate declaration with parent
resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
  parent: storageAccount
  name: 'default'
}
```

---

## Conditional Deployments

```bicep
param deployRedis bool = false
param environment string

resource redisCache 'Microsoft.Cache/redis@2023-08-01' = if (deployRedis) {
  name: '${resourcePrefix}-redis'
  location: location
  properties: {
    sku: {
      name: environment == 'prod' ? 'Premium' : 'Basic'
      family: environment == 'prod' ? 'P' : 'C'
      capacity: environment == 'prod' ? 1 : 0
    }
    enableNonSslPort: false
    minimumTlsVersion: '1.2'
  }
}

// Conditional output
output redisHostName string = deployRedis ? redisCache.properties.hostName : ''
```

---

## Loop Deployments

### Array Loop

```bicep
param storageNames array = ['logs', 'data', 'backups']

resource storageAccounts 'Microsoft.Storage/storageAccounts@2023-05-01' = [
  for name in storageNames: {
    name: 'st${name}${uniqueSuffix}'
    location: location
    sku: { name: 'Standard_LRS' }
    kind: 'StorageV2'
    properties: {}
  }
]
```

### Index Loop

```bicep
param appCount int = 3

resource webApps 'Microsoft.Web/sites@2023-12-01' = [
  for i in range(0, appCount): {
    name: '${resourcePrefix}-app-${i}'
    location: location
    properties: {
      serverFarmId: appServicePlan.id
    }
  }
]
```

### Object Array Loop

```bicep
param containers array = [
  { name: 'images', publicAccess: 'Blob' }
  { name: 'documents', publicAccess: 'None' }
  { name: 'logs', publicAccess: 'None' }
]

resource blobContainers 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = [
  for container in containers: {
    parent: blobService
    name: container.name
    properties: {
      publicAccess: container.publicAccess
    }
  }
]
```

### Filtered Loop

```bicep
param roleAssignments array = [
  { principalId: 'aaa', role: 'Reader' }
  { principalId: 'bbb', role: 'Contributor' }
  { principalId: 'ccc', role: 'Reader' }
]

resource readerAssignments 'Microsoft.Authorization/roleAssignments@2022-04-01' = [
  for assignment in filter(roleAssignments, r => r.role == 'Reader'): {
    name: guid(resourceGroup().id, assignment.principalId, 'Reader')
    properties: {
      roleDefinitionId: subscriptionResourceId(
        'Microsoft.Authorization/roleDefinitions',
        'acdd72a7-3385-48ef-bd42-f606fba81ae7'
      )
      principalId: assignment.principalId
    }
  }
]
```

---

## Modules

### Local Module

```bicep
// main.bicep
module webAppModule './modules/webapp.bicep' = {
  name: 'webAppDeployment'
  params: {
    appName: appName
    location: location
    appServicePlanId: appServicePlan.id
    appSettings: {
      NODE_ENV: 'production'
      API_URL: apiUrl
    }
  }
}

output webAppUrl string = webAppModule.outputs.defaultHostName
```

```bicep
// modules/webapp.bicep
param appName string
param location string
param appServicePlanId string
param appSettings object = {}

var settingsArray = [
  for item in items(appSettings): {
    name: item.key
    value: item.value
  }
]

resource webApp 'Microsoft.Web/sites@2023-12-01' = {
  name: appName
  location: location
  properties: {
    serverFarmId: appServicePlanId
    siteConfig: {
      appSettings: settingsArray
      linuxFxVersion: 'NODE|20-lts'
      alwaysOn: true
    }
    httpsOnly: true
  }
}

output defaultHostName string = webApp.properties.defaultHostName
output resourceId string = webApp.id
```

### Module with Condition and Loop

```bicep
param regions array = ['eastus', 'westeurope']
param deployMultiRegion bool = false

module regionalApps './modules/webapp.bicep' = [
  for (region, i) in regions: if (deployMultiRegion || i == 0) {
    name: 'deploy-${region}'
    params: {
      appName: '${appName}-${region}'
      location: region
      appServicePlanId: plans[i].outputs.planId
    }
  }
]
```

### Cross-Resource-Group Module

```bicep
module sharedResources './modules/shared.bicep' = {
  name: 'sharedResourcesDeploy'
  scope: resourceGroup('shared-resources-rg')
  params: {
    keyVaultName: 'kv-${appName}'
  }
}
```

---

## Common Resource Patterns

### App Service Plan + Web App (Linux, Node.js)

```bicep
param appName string
param location string = resourceGroup().location
param skuName string = 'B1'

resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: '${appName}-plan'
  location: location
  kind: 'linux'
  sku: {
    name: skuName
  }
  properties: {
    reserved: true // required for Linux
  }
}

resource webApp 'Microsoft.Web/sites@2023-12-01' = {
  name: appName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'NODE|20-lts'
      alwaysOn: skuName != 'F1'
      ftpsState: 'Disabled'
      minTlsVersion: '1.2'
      http20Enabled: true
      appSettings: [
        { name: 'WEBSITE_NODE_DEFAULT_VERSION', value: '~20' }
        { name: 'SCM_DO_BUILD_DURING_DEPLOYMENT', value: 'true' }
      ]
    }
  }
}

// Deployment slot for staging
resource stagingSlot 'Microsoft.Web/sites/slots@2023-12-01' = {
  parent: webApp
  name: 'staging'
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'NODE|20-lts'
      autoSwapSlotName: 'production'
    }
  }
}
```

### Storage Account with Blob Containers

```bicep
param storageName string
param location string = resourceGroup().location
param containerNames array = ['uploads', 'static', 'backups']

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageName
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  properties: {
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    networkAcls: {
      defaultAction: 'Deny'
      bypass: 'AzureServices'
    }
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
  parent: storageAccount
  name: 'default'
  properties: {
    deleteRetentionPolicy: {
      enabled: true
      days: 7
    }
  }
}

resource containers 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = [
  for name in containerNames: {
    parent: blobService
    name: name
    properties: {
      publicAccess: 'None'
    }
  }
]

output storageId string = storageAccount.id
output blobEndpoint string = storageAccount.properties.primaryEndpoints.blob
output connectionString string = 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value}'
```

### Azure Static Web Apps

```bicep
param appName string
param location string = 'centralus'
param sku string = 'Free' // 'Free' or 'Standard'
param repositoryUrl string = ''
param branch string = 'main'
param appLocation string = '/'
param outputLocation string = 'dist'
param apiLocation string = ''

resource staticWebApp 'Microsoft.Web/staticSites@2023-12-01' = {
  name: appName
  location: location
  sku: {
    name: sku
    tier: sku
  }
  properties: {
    repositoryUrl: !empty(repositoryUrl) ? repositoryUrl : null
    branch: !empty(repositoryUrl) ? branch : null
    buildProperties: {
      appLocation: appLocation
      outputLocation: outputLocation
      apiLocation: !empty(apiLocation) ? apiLocation : null
    }
  }
}

// App settings
resource swaAppSettings 'Microsoft.Web/staticSites/config@2023-12-01' = {
  parent: staticWebApp
  name: 'appsettings'
  properties: {
    API_URL: 'https://api.example.com'
    ENVIRONMENT: 'production'
  }
}

output swaUrl string = 'https://${staticWebApp.properties.defaultHostname}'
output swaId string = staticWebApp.id
output deploymentToken string = staticWebApp.listSecrets().properties.apiKey
```

### Cosmos DB (NoSQL API)

```bicep
param accountName string
param location string = resourceGroup().location
param databaseName string = 'appdb'
param containerConfigs array = [
  { name: 'users', partitionKey: '/userId', throughput: 400 }
  { name: 'recipes', partitionKey: '/category', throughput: 400 }
]

resource cosmosAccount 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' = {
  name: accountName
  location: location
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
    }
    locations: [
      {
        locationName: location
        failoverPriority: 0
        isZoneRedundant: false
      }
    ]
    capabilities: [
      { name: 'EnableServerless' }
    ]
    backupPolicy: {
      type: 'Continuous'
      continuousModeProperties: {
        tier: 'Continuous7Days'
      }
    }
  }
}

resource database 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-05-15' = {
  parent: cosmosAccount
  name: databaseName
  properties: {
    resource: {
      id: databaseName
    }
  }
}

resource containers 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-05-15' = [
  for config in containerConfigs: {
    parent: database
    name: config.name
    properties: {
      resource: {
        id: config.name
        partitionKey: {
          paths: [config.partitionKey]
          kind: 'Hash'
        }
        indexingPolicy: {
          automatic: true
          indexingMode: 'consistent'
        }
      }
    }
  }
]

output cosmosEndpoint string = cosmosAccount.properties.documentEndpoint
output cosmosAccountName string = cosmosAccount.name
```

---

## User-Defined Types (Bicep v0.21+)

```bicep
@description('Configuration for an application environment')
type environmentConfig = {
  @description('Environment name')
  name: 'dev' | 'staging' | 'prod'

  @description('SKU tier')
  sku: string

  @description('Number of instances')
  instanceCount: int

  @description('Custom domain (optional)')
  customDomain: string?
}

param envConfig environmentConfig = {
  name: 'dev'
  sku: 'B1'
  instanceCount: 1
}
```

---

## Decorators Reference

| Decorator | Applies To | Purpose |
|-----------|-----------|---------|
| `@description()` | param, output, type | Describes the element |
| `@secure()` | param | Marks as sensitive (no logging) |
| `@allowed([])` | param | Restricts to listed values |
| `@minLength()` / `@maxLength()` | param (string/array) | Length constraints |
| `@minValue()` / `@maxValue()` | param (int) | Numeric range |
| `@metadata({})` | param | Arbitrary metadata |
| `@sealed()` | type, param | Prevents additional properties |
| `@discriminator()` | type | Tagged union discriminator |

---

## Useful Built-in Functions

| Function | Example | Returns |
|----------|---------|---------|
| `resourceGroup().location` | — | Resource group's region |
| `uniqueString(seed)` | `uniqueString(resourceGroup().id)` | 13-char deterministic hash |
| `subscription().subscriptionId` | — | Current subscription ID |
| `tenant().tenantId` | — | Current tenant ID |
| `environment().suffixes.storage` | — | Storage endpoint suffix |
| `toLower()` / `toUpper()` | `toLower('ABC')` | `abc` |
| `replace()` | `replace('a-b', '-', '')` | `ab` |
| `guid()` | `guid(resourceGroup().id, 'reader')` | Deterministic GUID |
| `loadTextContent()` | `loadTextContent('./script.sh')` | File contents as string |
| `loadJsonContent()` | `loadJsonContent('./config.json')` | Parsed JSON object |

---

## CLI Commands

```bash
# Validate template
az bicep build --file main.bicep

# Deploy to resource group
az deployment group create \
  --resource-group myRg \
  --template-file main.bicep \
  --parameters environment='prod' appName='myapp'

# Deploy with parameter file
az deployment group create \
  --resource-group myRg \
  --template-file main.bicep \
  --parameters @parameters.prod.json

# What-if (preview changes)
az deployment group what-if \
  --resource-group myRg \
  --template-file main.bicep \
  --parameters @parameters.prod.json

# Subscription-level deployment
az deployment sub create \
  --location eastus \
  --template-file main.bicep
```
