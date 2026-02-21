<#
.SYNOPSIS
    Deploys a Vite/React or Next.js application to Azure Static Web Apps.

.DESCRIPTION
    Creates (or reuses) a resource group and Azure Static Web App resource,
    then deploys the built application using the SWA CLI.

.PARAMETER AppName
    Name of the Static Web App resource. Must be globally unique.

.PARAMETER ResourceGroup
    Name of the Azure resource group. Created if it does not exist.

.PARAMETER Location
    Azure region for the resource group and SWA. Default: centralus.

.PARAMETER OutputDir
    Build output directory relative to the project root (e.g., "dist" for Vite, ".next" for Next.js).

.PARAMETER AppDir
    Application source directory. Default: current directory.

.PARAMETER ApiDir
    Optional managed API directory (e.g., "api").

.PARAMETER Sku
    SWA pricing tier: Free or Standard. Default: Free.

.PARAMETER SkipBuild
    If set, skips the npm build step (expects output already present).

.EXAMPLE
    .\deploy-swa.ps1 -AppName "my-vite-app" -ResourceGroup "rg-my-app" -OutputDir "dist"

.EXAMPLE
    .\deploy-swa.ps1 -AppName "my-next-app" -ResourceGroup "rg-next" -OutputDir ".next" -Sku Standard
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidatePattern('^[a-zA-Z0-9][a-zA-Z0-9-]{1,58}[a-zA-Z0-9]$')]
    [string]$AppName,

    [Parameter(Mandatory)]
    [string]$ResourceGroup,

    [string]$Location = 'centralus',

    [Parameter(Mandatory)]
    [string]$OutputDir,

    [string]$AppDir = '.',

    [string]$ApiDir = '',

    [ValidateSet('Free', 'Standard')]
    [string]$Sku = 'Free',

    [switch]$SkipBuild
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-Step {
    param([string]$Message)
    Write-Host "`n>> $Message" -ForegroundColor Cyan
}

function Assert-Command {
    param([string]$Name, [string]$InstallHint)
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        Write-Error "$Name is not installed or not in PATH. $InstallHint"
        exit 1
    }
}

# ─── Prerequisites ───

Write-Step 'Checking prerequisites'

Assert-Command 'az' 'Install Azure CLI: https://aka.ms/install-azure-cli'
Assert-Command 'swa' 'Install SWA CLI: npm install -g @azure/static-web-apps-cli'
Assert-Command 'node' 'Install Node.js: https://nodejs.org'

# ─── Azure Login Check ───

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

$currentAccount = az account show --query '{subscription:name, tenantId:tenantId}' -o json | ConvertFrom-Json
Write-Host "  Subscription: $($currentAccount.subscription)"
Write-Host "  Tenant:       $($currentAccount.tenantId)"

# ─── Resource Group ───

Write-Step "Ensuring resource group '$ResourceGroup' exists in '$Location'"

$rgExists = az group exists --name $ResourceGroup
if ($rgExists -eq 'false') {
    Write-Host "  Creating resource group..." -ForegroundColor Yellow
    az group create --name $ResourceGroup --location $Location --output none
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create resource group '$ResourceGroup'."
        exit 1
    }
    Write-Host "  Resource group created." -ForegroundColor Green
} else {
    Write-Host "  Resource group already exists." -ForegroundColor Green
}

# ─── Static Web App Resource ───

Write-Step "Ensuring Static Web App '$AppName' exists"

$swaExists = az staticwebapp show --name $AppName --resource-group $ResourceGroup 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Creating Static Web App ($Sku tier)..." -ForegroundColor Yellow
    az staticwebapp create `
        --name $AppName `
        --resource-group $ResourceGroup `
        --location $Location `
        --sku $Sku `
        --output none

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create Static Web App '$AppName'."
        exit 1
    }
    Write-Host "  Static Web App created." -ForegroundColor Green
} else {
    Write-Host "  Static Web App already exists." -ForegroundColor Green
}

# ─── Retrieve Deployment Token ───

Write-Step 'Retrieving deployment token'

$deploymentToken = az staticwebapp secrets list `
    --name $AppName `
    --resource-group $ResourceGroup `
    --query 'properties.apiKey' -o tsv

if (-not $deploymentToken) {
    Write-Error 'Failed to retrieve SWA deployment token.'
    exit 1
}

Write-Host '  Deployment token acquired.' -ForegroundColor Green

# ─── Build Application ───

Push-Location $AppDir

try {
    if (-not $SkipBuild) {
        Write-Step 'Building application'

        $packageManager = 'npm'
        if (Test-Path 'pnpm-lock.yaml') { $packageManager = 'pnpm' }
        elseif (Test-Path 'yarn.lock') { $packageManager = 'yarn' }

        Write-Host "  Detected package manager: $packageManager"

        & $packageManager install
        if ($LASTEXITCODE -ne 0) {
            Write-Error 'Dependency installation failed.'
            exit 1
        }

        & $packageManager run build
        if ($LASTEXITCODE -ne 0) {
            Write-Error 'Build failed.'
            exit 1
        }

        Write-Host '  Build succeeded.' -ForegroundColor Green
    } else {
        Write-Host '  Skipping build (--SkipBuild).' -ForegroundColor Yellow
    }

    if (-not (Test-Path $OutputDir)) {
        Write-Error "Build output directory '$OutputDir' not found. Did the build succeed?"
        exit 1
    }

    # ─── Deploy ───

    Write-Step "Deploying to Azure Static Web Apps"

    $swaArgs = @(
        'deploy'
        '--output-location', $OutputDir
        '--deployment-token', $deploymentToken
        '--env', 'production'
    )

    if ($ApiDir -and (Test-Path $ApiDir)) {
        $swaArgs += '--api-location', $ApiDir
    }

    & swa @swaArgs

    if ($LASTEXITCODE -ne 0) {
        Write-Error 'SWA deployment failed.'
        exit 1
    }

    # ─── Summary ───

    $hostname = az staticwebapp show `
        --name $AppName `
        --resource-group $ResourceGroup `
        --query 'defaultHostname' -o tsv

    Write-Host ''
    Write-Host '==========================================' -ForegroundColor Green
    Write-Host '  Deployment Successful!' -ForegroundColor Green
    Write-Host "  URL: https://$hostname" -ForegroundColor Green
    Write-Host "  Resource Group: $ResourceGroup" -ForegroundColor Green
    Write-Host "  SWA Name: $AppName" -ForegroundColor Green
    Write-Host "  SKU: $Sku" -ForegroundColor Green
    Write-Host '==========================================' -ForegroundColor Green
}
finally {
    Pop-Location
}
