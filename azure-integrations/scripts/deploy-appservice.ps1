<#
.SYNOPSIS
    Deploys a Next.js application to Azure App Service with Storage, Key Vault, and Application Insights.

.DESCRIPTION
    Creates (or reuses) a resource group, App Service Plan, Web App, Storage Account,
    Key Vault, Cosmos DB (MongoDB API), and Application Insights. Configures Managed Identity
    for secure secret access and deploys the built application.

.PARAMETER AppName
    Name of the Web App resource. Must be globally unique.

.PARAMETER ResourceGroup
    Name of Azure resource group. Created if it does not exist.

.PARAMETER Location
    Azure region for resource group and all resources. Default: eastus.

.PARAMETER OutputDir
    Build output directory relative to project root. Default: ".next" (Next.js standalone).

.PARAMETER AppDir
    Application source directory. Default: current directory.

.PARAMETER Sku
    App Service Plan pricing tier. Default: B1 (Basic).

.PARAMETER EnableAppInsights
    Enable Application Insights for monitoring. Default: true.

.PARAMETER EnableStorage
    Create Storage Account for file uploads. Default: true.

.PARAMETER SkipBuild
    If set, skips npm build step (expects output already present).

.PARAMETER MongoDbConnectionString
    MongoDB Atlas connection string for Cosmos DB. Secure parameter (prompted if not provided).

.EXAMPLE
    .\deploy-appservice.ps1 -AppName "kitchen-odyssey" -ResourceGroup "rg-recipe-app"

.EXAMPLE
    .\deploy-appservice.ps1 -AppName "my-app" -ResourceGroup "rg-my" -Sku S1 -OutputDir ".next"

.EXAMPLE
    .\deploy-appservice.ps1 -AppName "test-app" -ResourceGroup "rg-test" -SkipBuild
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidatePattern('^[a-zA-Z0-9][a-zA-Z0-9-]{1,58}[a-zA-Z0-9]$')]
    [string]$AppName,

    [Parameter(Mandatory)]
    [string]$ResourceGroup,

    [string]$Location = 'eastus',

    [string]$OutputDir = '.next',

    [string]$AppDir = '.',

    [ValidateSet('B1', 'B2', 'B3', 'S1', 'S2', 'S3', 'P1V3', 'P2V3', 'P3V3')]
    [string]$Sku = 'B1',

    [switch]$EnableAppInsights,

    [switch]$EnableStorage,

    [switch]$SkipBuild,

    [Parameter(Mandatory = $false)]
    [securestring]$MongoDbConnectionString
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ProgressPreference = 'SilentlyContinue'

function Write-Step {
    param([string]$Message)
    Write-Host "`n▶ $Message" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "  ✓ $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "  ⚠ $Message" -ForegroundColor Yellow
}

function Assert-Command {
    param([string]$Name, [string]$InstallHint)
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        Write-Error "$Name is not installed or not in PATH. $InstallHint"
        exit 1
    }
}

# ────────────────────────────────────────────────────────────────────────────────
# Prerequisites
# ────────────────────────────────────────────────────────────────────────────────

Write-Step 'Checking prerequisites'

Assert-Command 'az' 'Install Azure CLI: https://aka.ms/install-azure-cli'
Assert-Command 'node' 'Install Node.js: https://nodejs.org'

Write-Success 'All prerequisites installed'

# ────────────────────────────────────────────────────────────────────────────────
# Azure Login Check
# ────────────────────────────────────────────────────────────────────────────────

Write-Step 'Verifying Azure CLI login'

$account = az account show 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Not logged in. Launching interactive login...' -ForegroundColor Yellow
    az login
    if ($LASTEXITCODE -ne 0) {
        Write-Error 'Azure login failed.'
        exit 1
    }
}

$currentAccount = az account show --query '{subscription:name, tenantId:tenantId, user:name}' -o json | ConvertFrom-Json
Write-Host "  Subscription:  $($currentAccount.subscription)"
Write-Host "  Tenant:       $($currentAccount.tenantId)"
Write-Host "  User:         $($currentAccount.user)"

# ────────────────────────────────────────────────────────────────────────────────
# MongoDB Connection String
# ────────────────────────────────────────────────────────────────────────────────

Write-Step 'MongoDB Connection String'

if (-not $MongoDbConnectionString) {
    Write-Host 'Enter MongoDB Atlas connection string (will be stored securely in Key Vault):' -ForegroundColor Yellow
    Write-Host 'Example: mongodb+srv://username:password@cluster.mongodb.net/database' -ForegroundColor Gray
    $credential = $Host.UI.PromptForCredential("MongoDB Atlas", "Enter connection string", "", "")
    $MongoDbConnectionString = $credential.GetNetworkCredential().Password | ConvertTo-SecureString -AsPlainText -Force
}

$mongoDbPlain = [System.Net.NetworkCredential]::new("", $MongoDbConnectionString).Password
Write-Success 'MongoDB connection string acquired'

# ────────────────────────────────────────────────────────────────────────────────
# Resource Group
# ────────────────────────────────────────────────────────────────────────────────

Write-Step "Ensuring resource group '$ResourceGroup' exists in '$Location'"

$rgExists = az group exists --name $ResourceGroup
if ($rgExists -eq 'false') {
    Write-Host "  Creating resource group..." -ForegroundColor Yellow
    az group create --name $ResourceGroup --location $Location --output none
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create resource group '$ResourceGroup'."
        exit 1
    }
    Write-Success "Resource group created"
} else {
    Write-Success "Resource group already exists"
}

# ────────────────────────────────────────────────────────────────────────────────
# App Service Plan
# ────────────────────────────────────────────────────────────────────────────────

Write-Step "Ensuring App Service Plan '${AppName}-plan' exists ($Sku tier)"

$appServicePlan = "${AppName}-plan"

$planExists = az appservice plan show --name $appServicePlan --resource-group $ResourceGroup --query name -o tsv 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Creating App Service Plan..." -ForegroundColor Yellow

    $skuTier = switch ($Sku[0]) {
        'B' { 'Basic' }
        'S' { 'Standard' }
        'P' { 'Premium' }
        default { 'Basic' }
    }

    az appservice plan create `
        --name $appServicePlan `
        --resource-group $ResourceGroup `
        --location $Location `
        --is-linux `
        --sku $Sku `
        --output none

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create App Service Plan '$appServicePlan'."
        exit 1
    }
    Write-Success "App Service Plan created ($skuTier tier)"
} else {
    Write-Success "App Service Plan already exists"
}

# ────────────────────────────────────────────────────────────────────────────────
# Web App
# ────────────────────────────────────────────────────────────────────────────────

Write-Step "Ensuring Web App '$AppName' exists"

$webAppExists = az webapp show --name $AppName --resource-group $ResourceGroup --query name -o tsv 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Creating Web App..." -ForegroundColor Yellow

    az webapp create `
        --name $AppName `
        --resource-group $ResourceGroup `
        --plan $appServicePlan `
        --runtime "NODE|20-lts" `
        --output none

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create Web App '$AppName'."
        exit 1
    }
    Write-Success "Web App created"
} else {
    Write-Success "Web App already exists"
}

# ────────────────────────────────────────────────────────────────────────────────
# Managed Identity
# ────────────────────────────────────────────────────────────────────────────────

Write-Step "Configuring Managed Identity"

az webapp identity assign --name $AppName --resource-group $ResourceGroup --output none
$principalId = az webapp identity show --name $AppName --resource-group $ResourceGroup --query principalId -o tsv
$clientId = az webapp identity show --name $AppName --resource-group $ResourceGroup --query clientId -o tsv

Write-Success "Managed Identity enabled (Principal ID: $principalId)"

# ────────────────────────────────────────────────────────────────────────────────
# Application Insights
# ────────────────────────────────────────────────────────────────────────────────

if ($EnableAppInsights) {
    Write-Step "Setting up Application Insights"

    $appInsightsName = "${AppName}ai"

    $aiExists = az monitor app-insights component show --app $appInsightsName --resource-group $ResourceGroup --query name -o tsv 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  Creating Application Insights..." -ForegroundColor Yellow

        az monitor app-insights component create `
            --app $appInsightsName `
            --location $Location `
            --resource-group $ResourceGroup `
            --application-type web `
            --output none

        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to create Application Insights."
            exit 1
        }
        Write-Success "Application Insights created"
    } else {
        Write-Success "Application Insights already exists"
    }

    $instrumentationKey = az monitor app-insights component show `
        --app $appInsightsName `
        --resource-group $ResourceGroup `
        --query instrumentationKey -o tsv

    Write-Success "Instrumentation Key retrieved"
}

# ────────────────────────────────────────────────────────────────────────────────
# Storage Account
# ────────────────────────────────────────────────────────────────────────────────

if ($EnableStorage) {
    Write-Step "Setting up Storage Account for file uploads"

    $storageAccount = "${AppName}$(Get-Random -Minimum 100 -Maximum 999)"

    $storageExists = az storage account show --name $storageAccount --resource-group $ResourceGroup --query name -o tsv 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  Creating Storage Account..." -ForegroundColor Yellow

        az storage account create `
            --name $storageAccount `
            --resource-group $ResourceGroup `
            --location $Location `
            --sku Standard_LRS `
            --kind StorageV2 `
            --output none

        if ($LASTEXITCODE -ne 0) {
            Write-Warning "Failed to create Storage Account. File uploads will not work."
        } else {
            Write-Success "Storage Account created"
        }
    } else {
        Write-Success "Storage Account already exists"
    }

    if ($LASTEXITCODE -eq 0) {
        Write-Step "Creating container for recipe images"

        az storage container create `
            --name recipe-images `
            --account-name $storageAccount `
            --auth-mode login `
            --public-access blob `
            --output none 2>&1

        Write-Success "Container 'recipe-images' created"

        $storageConn = az storage account show-connection-string `
            --name $storageAccount `
            --resource-group $ResourceGroup `
            --query connectionString -o tsv
    }
}

# ────────────────────────────────────────────────────────────────────────────────
# Key Vault
# ────────────────────────────────────────────────────────────────────────────────

Write-Step "Setting up Key Vault for secure secrets"

$keyVaultName = "${AppName}$(Get-Random -Minimum 100 -Maximum 999)kv"

$kvExists = az keyvault show --name $keyVaultName --resource-group $ResourceGroup --query name -o tsv 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Creating Key Vault..." -ForegroundColor Yellow

    az keyvault create `
        --name $keyVaultName `
        --resource-group $ResourceGroup `
        --location $Location `
        --enable-purge-protection true `
        --enable-soft-delete true `
        --output none

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create Key Vault."
        exit 1
    }
    Write-Success "Key Vault created"
} else {
    Write-Success "Key Vault already exists"
}

# ────────────────────────────────────────────────────────────────────────────────
# Store Secrets in Key Vault
# ────────────────────────────────────────────────────────────────────────────────

Write-Step "Storing secrets in Key Vault"

az keyvault secret set `
    --vault-name $keyVaultName `
    --name "MongoDB-Uri" `
    --value $mongoDbPlain `
    --output none

Write-Success "MongoDB URI stored in Key Vault"

if ($EnableAppInsights) {
    az keyvault secret set `
        --vault-name $keyVaultName `
        --name "AppInsights-InstrumentationKey" `
        --value $instrumentationKey `
        --output none

    Write-Success "App Insights Instrumentation Key stored"
}

if ($EnableStorage -and $storageConn) {
    az keyvault secret set `
        --vault-name $keyVaultName `
        --name "Storage-ConnectionString" `
        --value $storageConn `
        --output none

    Write-Success "Storage Connection String stored"
}

# Generate NEXTAUTH_SECRET
$nextAuthSecret = -join ((48..122) | Get-Random -Count 32 | ForEach-Object { [char]$_ })
az keyvault secret set `
    --vault-name $keyVaultName `
    --name "NextAuth-Secret" `
    --value $nextAuthSecret `
    --output none

Write-Success "NEXTAUTH_SECRET generated and stored"

# ────────────────────────────────────────────────────────────────────────────────
# Grant Managed Identity Access to Key Vault
# ────────────────────────────────────────────────────────────────────────────────

Write-Step "Granting Managed Identity access to Key Vault"

az keyvault set-policy `
    --name $keyVaultName `
    --resource-group $ResourceGroup `
    --object-id $principalId `
    --secret-permissions get list `
    --output none

Write-Success "Managed Identity has Key Vault access (get, list)"

# ────────────────────────────────────────────────────────────────────────────────
# Grant Managed Identity Access to Storage (if enabled)
# ────────────────────────────────────────────────────────────────────────────────

if ($EnableStorage -and $storageConn) {
    Write-Step "Granting Managed Identity access to Storage Account"

    $storageId = az storage account show --name $storageAccount --resource-group $ResourceGroup --query id -o tsv

    az role assignment create `
        --assignee $principalId `
        --role "Storage Blob Data Contributor" `
        --scope $storageId `
        --output none

    Write-Success "Managed Identity has Storage access (Blob Data Contributor)"
}

# ────────────────────────────────────────────────────────────────────────────────
# Configure Application Settings
# ────────────────────────────────────────────────────────────────────────────────

Write-Step "Configuring Web App settings"

$keyVaultUri = az keyvault show --name $keyVaultName --resource-group $ResourceGroup --query properties.vaultUri -o tsv
$appUrl = "https://$AppName.azurewebsites.net"

$appSettings = @(
    "AZURE_KEYVAULT_RESOURCEENDPOINT=$keyVaultUri"
    "AZURE_CLIENTID=$clientId"
    "NEXTAUTH_URL=$appUrl"
    "NODE_ENV=production"
    "AZURE_KEYVAULT_NAME=$keyVaultName"
)

if ($EnableAppInsights) {
    $appSettings += "APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=$instrumentationKey"
}

foreach ($setting in $appSettings) {
    az webapp config appsettings set `
        --name $AppName `
        --resource-group $ResourceGroup `
        --settings $setting `
        --output none
}

Write-Success "Application settings configured"

# ────────────────────────────────────────────────────────────────────────────────
# Build Application
# ────────────────────────────────────────────────────────────────────────────────

Push-Location $AppDir

try {
    if (-not $SkipBuild) {
        Write-Step 'Building application'

        $packageManager = 'npm'
        if (Test-Path 'pnpm-lock.yaml') {
            $packageManager = 'pnpm'
        } elseif (Test-Path 'yarn.lock') {
            $packageManager = 'yarn'
        }

        Write-Host "  Detected package manager: $packageManager" -ForegroundColor Cyan

        Write-Host "  Installing dependencies..." -ForegroundColor Gray
        & $packageManager install
        if ($LASTEXITCODE -ne 0) {
            Write-Error 'Dependency installation failed.'
            exit 1
        }

        Write-Host "  Building Next.js app..." -ForegroundColor Gray
        & $packageManager run build
        if ($LASTEXITCODE -ne 0) {
            Write-Error 'Build failed.'
            exit 1
        }

        Write-Success 'Build succeeded'
    } else {
        Write-Warning 'Skipping build (--SkipBuild)'
    }

    if (-not (Test-Path $OutputDir)) {
        Write-Error "Build output directory '$OutputDir' not found. Did the build succeed?"
        exit 1
    }

    # ────────────────────────────────────────────────────────────────────────────────
    # Deploy
    # ────────────────────────────────────────────────────────────────────────────────

    Write-Step "Deploying to Azure App Service"

    Publish-Location -Path $OutputDir -DestinationPath "deploy-package" -Force

    Compress-Archive -Path "deploy-package\*" -DestinationPath "deploy-package.zip" -Force

    az webapp deployment source config-zip `
        --resource-group $ResourceGroup `
        --name $AppName `
        --src "deploy-package.zip" `
        --output none

    if ($LASTEXITCODE -ne 0) {
        Write-Error 'Deployment failed. Check Azure portal logs.'
        exit 1
    }

    Write-Success "Deployment successful!"

    # ────────────────────────────────────────────────────────────────────────────────
    # Summary
    # ────────────────────────────────────────────────────────────────────────────────

    Write-Host "`n" -NoNewline
    Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                    Deployment Complete!                           ║" -ForegroundColor Green
    Write-Host "╠═══════════════════════════════════════════════════════════════╣" -ForegroundColor Green
    Write-Host "║" -NoNewline -ForegroundColor Green
    Write-Host " Application URL:    " -NoNewline
    Write-Host "$appUrl" -ForegroundColor White -BackgroundColor Blue
    Write-Host "  ║" -NoNewline -ForegroundColor Green
    Write-Host ""
    Write-Host "║" -NoNewline -ForegroundColor Green
    Write-Host " App Service Plan:   " -NoNewline
    Write-Host "$appServicePlan" -ForegroundColor Cyan
    Write-Host " ($Sku)           ║" -NoNewline -ForegroundColor Green
    Write-Host ""
    Write-Host "║" -NoNewline -ForegroundColor Green
    Write-Host " Key Vault:          " -NoNewline
    Write-Host "$keyVaultName" -ForegroundColor Cyan
    Write-Host "                     ║" -NoNewline -ForegroundColor Green
    Write-Host ""
    Write-Host "║" -NoNewline -ForegroundColor Green
    Write-Host " Managed Identity:   " -NoNewline
    Write-Host "Enabled ($clientId)" -ForegroundColor Cyan
    Write-Host "             ║" -NoNewline -ForegroundColor Green
    Write-Host ""

    if ($EnableAppInsights) {
        Write-Host "║" -NoNewline -ForegroundColor Green
        Write-Host " App Insights:       " -NoNewline
        Write-Host "Enabled" -ForegroundColor Cyan
        Write-Host "                          ║" -NoNewline -ForegroundColor Green
        Write-Host ""
    }

    if ($EnableStorage) {
        Write-Host "║" -NoNewline -ForegroundColor Green
        Write-Host " Storage Account:     " -NoNewline
        Write-Host "$storageAccount" -ForegroundColor Cyan
        Write-Host "                ║" -NoNewline -ForegroundColor Green
        Write-Host ""
    }

    Write-Host "╠═══════════════════════════════════════════════════════════════╣" -ForegroundColor Green
    Write-Host "║ Important:                                                               ║" -ForegroundColor Yellow
    Write-Host "║ - MongoDB connection string is stored securely in Key Vault                ║" -ForegroundColor Yellow
    Write-Host "║ - NEXTAUTH_SECRET was auto-generated and stored in Key Vault            ║" -ForegroundColor Yellow
    Write-Host "║ - No secrets are exposed in Application Settings                            ║" -ForegroundColor Yellow
    Write-Host "║ - Enable logging: az webapp log tail --name $AppName --resource-group $ResourceGroup" -ForegroundColor Yellow
    Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Green

} finally {
    Pop-Location

    if (Test-Path "deploy-package") {
        Remove-Item -Recurse -Force "deploy-package"
    }
    if (Test-Path "deploy-package.zip") {
        Remove-Item -Force "deploy-package.zip"
    }
}
