<#
.SYNOPSIS
    Build and deploy a Node or Next.js app to Azure App Service with zip deployment.

.DESCRIPTION
    Creates the resource group, Linux App Service plan, and web app if they do not exist.
    Builds the app unless -SkipBuild is provided, zips the chosen output directory, and deploys it.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$AppName,

    [Parameter(Mandatory = $true)]
    [string]$ResourceGroup,

    [string]$Location = "eastus",

    [string]$PlanName,

    [string]$Runtime = "NODE|20-lts",

    [string]$AppDir = ".",

    [string]$OutputDir = "dist",

    [switch]$SkipBuild
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Assert-Command {
    param([string]$Name)
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found in PATH."
    }
}

function Ensure-AzureLogin {
    az account show *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Azure CLI is not logged in. Launching 'az login'..." -ForegroundColor Yellow
        az login | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw "Azure login failed."
        }
    }
}

function Ensure-ResourceGroup {
    $exists = az group exists --name $ResourceGroup
    if ($exists -eq "false") {
        Write-Host "Creating resource group '$ResourceGroup' in '$Location'..." -ForegroundColor Cyan
        az group create --name $ResourceGroup --location $Location --output none
    }
}

function Ensure-Plan {
    param([string]$ResolvedPlanName)
    az appservice plan show --name $ResolvedPlanName --resource-group $ResourceGroup *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Creating App Service plan '$ResolvedPlanName'..." -ForegroundColor Cyan
        az appservice plan create `
            --name $ResolvedPlanName `
            --resource-group $ResourceGroup `
            --location $Location `
            --is-linux `
            --sku B1 `
            --output none
    }
}

function Ensure-WebApp {
    param([string]$ResolvedPlanName)
    az webapp show --name $AppName --resource-group $ResourceGroup *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Creating web app '$AppName'..." -ForegroundColor Cyan
        az webapp create `
            --name $AppName `
            --resource-group $ResourceGroup `
            --plan $ResolvedPlanName `
            --runtime $Runtime `
            --output none
    }
}

function Invoke-Build {
    Push-Location $AppDir
    try {
        if ($SkipBuild) {
            return
        }
        Assert-Command node
        $pm = if (Test-Path "pnpm-lock.yaml") { "pnpm" } elseif (Test-Path "yarn.lock") { "yarn" } else { "npm" }
        Write-Host "Installing dependencies with $pm..." -ForegroundColor Cyan
        & $pm install
        if ($LASTEXITCODE -ne 0) {
            throw "Dependency installation failed."
        }
        Write-Host "Building application..." -ForegroundColor Cyan
        & $pm run build
        if ($LASTEXITCODE -ne 0) {
            throw "Build failed."
        }
    }
    finally {
        Pop-Location
    }
}

function Publish-ZipDeployment {
    Push-Location $AppDir
    try {
        if (-not (Test-Path $OutputDir)) {
            throw "Output directory '$OutputDir' was not found."
        }

        $zipPath = Join-Path ([System.IO.Path]::GetTempPath()) "$AppName-deploy.zip"
        if (Test-Path $zipPath) {
            Remove-Item -Force $zipPath
        }
        Compress-Archive -Path (Join-Path $OutputDir "*") -DestinationPath $zipPath -Force
        Write-Host "Deploying archive to Azure App Service..." -ForegroundColor Cyan
        az webapp deployment source config-zip `
            --name $AppName `
            --resource-group $ResourceGroup `
            --src $zipPath `
            --output none
        Remove-Item -Force $zipPath
    }
    finally {
        Pop-Location
    }
}

Assert-Command az
Ensure-AzureLogin

$resolvedPlan = if ($PlanName) { $PlanName } else { "$AppName-plan" }

Ensure-ResourceGroup
Ensure-Plan -ResolvedPlanName $resolvedPlan
Ensure-WebApp -ResolvedPlanName $resolvedPlan
Invoke-Build
Publish-ZipDeployment

Write-Host ""
Write-Host "Deployment complete." -ForegroundColor Green
Write-Host "App URL: https://$AppName.azurewebsites.net" -ForegroundColor Green
