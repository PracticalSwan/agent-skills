<#
.SYNOPSIS
    Checks health of Azure resources in a resource group.

.DESCRIPTION
    Verifies Azure CLI installation and login, then checks the status of
    App Services, Storage Accounts, and Cosmos DB accounts within the
    specified resource group. Outputs a colored status report.

.PARAMETER ResourceGroup
    The Azure resource group to check. Required.

.PARAMETER SubscriptionId
    The Azure subscription ID. If provided, sets active subscription before checks.

.EXAMPLE
    .\azure-health-check.ps1 -ResourceGroup "my-rg"

.EXAMPLE
    .\azure-health-check.ps1 -ResourceGroup "my-rg" -SubscriptionId "00000000-0000-0000-0000-000000000000"
#>
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$ResourceGroup,

    [Parameter(Position = 1)]
    [string]$SubscriptionId
)

$ErrorActionPreference = "Stop"

function Write-Status {
    param([string]$Name, [string]$Status, [string]$Detail = "")
    $color = switch ($Status) {
        "Healthy"   { "Green" }
        "Running"   { "Green" }
        "Available" { "Green" }
        "Warning"   { "Yellow" }
        "Stopped"   { "Yellow" }
        "Error"     { "Red" }
        "NotFound"  { "DarkGray" }
        default     { "White" }
    }
    $line = "  [{0,-12}] {1}" -f $Status, $Name
    if ($Detail) { $line += " — $Detail" }
    Write-Host $line -ForegroundColor $color
}

# ── Header ──
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Azure Resource Health Check" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Resource Group: $ResourceGroup"
if ($SubscriptionId) { Write-Host "  Subscription:   $SubscriptionId" }
Write-Host "  Timestamp:      $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss UTC' -AsUTC)"
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# ── Check 1: Azure CLI ──
Write-Host "Checking prerequisites..." -ForegroundColor Yellow
try {
    $azVersion = az version 2>&1 | ConvertFrom-Json
    $cliVersion = $azVersion.'azure-cli'
    Write-Status "Azure CLI" "Healthy" "v$cliVersion"
}
catch {
    Write-Status "Azure CLI" "Error" "Not installed. Install: https://aka.ms/installazurecli"
    exit 1
}

# ── Check 2: Login Status ──
try {
    $account = az account show 2>&1 | ConvertFrom-Json
    Write-Status "Login" "Healthy" $account.user.name
}
catch {
    Write-Status "Login" "Error" "Not logged in. Run: az login"
    exit 1
}

# ── Set Subscription ──
if ($SubscriptionId) {
    try {
        az account set --subscription $SubscriptionId 2>&1 | Out-Null
        Write-Status "Subscription" "Healthy" $SubscriptionId
    }
    catch {
        Write-Status "Subscription" "Error" "Failed to set subscription $SubscriptionId"
        exit 1
    }
}

# ── Check 3: Resource Group Exists ──
Write-Host ""
Write-Host "Checking resource group..." -ForegroundColor Yellow
try {
    $rg = az group show --name $ResourceGroup 2>&1 | ConvertFrom-Json
    Write-Status "Resource Group" "Available" "Location: $($rg.location)"
}
catch {
    Write-Status "Resource Group" "NotFound" "'$ResourceGroup' does not exist"
    exit 1
}

# ── Check 4: App Services ──
Write-Host ""
Write-Host "Checking App Services..." -ForegroundColor Yellow
try {
    $apps = az webapp list --resource-group $ResourceGroup 2>&1 | ConvertFrom-Json

    if ($apps.Count -eq 0) {
        Write-Status "App Services" "NotFound" "No App Services in this resource group"
    }
    else {
        foreach ($app in $apps) {
            $state = $app.state
            $status = if ($state -eq "Running") { "Running" } elseif ($state -eq "Stopped") { "Stopped" } else { "Warning" }
            $https = if ($app.httpsOnly) { "HTTPS" } else { "HTTP" }
            Write-Status $app.name $status "$state | $https | $($app.defaultHostName)"
        }
    }
}
catch {
    Write-Status "App Services" "Error" "Failed to query: $_"
}

# ── Check 5: Function Apps ──
Write-Host ""
Write-Host "Checking Function Apps..." -ForegroundColor Yellow
try {
    $functions = az functionapp list --resource-group $ResourceGroup 2>&1 | ConvertFrom-Json

    if ($functions.Count -eq 0) {
        Write-Status "Function Apps" "NotFound" "No Function Apps in this resource group"
    }
    else {
        foreach ($func in $functions) {
            $state = $func.state
            $status = if ($state -eq "Running") { "Running" } else { "Warning" }
            Write-Status $func.name $status "$state | $($func.defaultHostName)"
        }
    }
}
catch {
    Write-Status "Function Apps" "Error" "Failed to query: $_"
}

# ── Check 6: Storage Accounts ──
Write-Host ""
Write-Host "Checking Storage Accounts..." -ForegroundColor Yellow
try {
    $storageAccounts = az storage account list --resource-group $ResourceGroup 2>&1 | ConvertFrom-Json

    if ($storageAccounts.Count -eq 0) {
        Write-Status "Storage" "NotFound" "No Storage Accounts in this resource group"
    }
    else {
        foreach ($sa in $storageAccounts) {
            $provisioningState = $sa.provisioningState
            $status = if ($provisioningState -eq "Succeeded") { "Healthy" } else { "Warning" }
            $kind = $sa.kind
            $sku = $sa.sku.name
            $https = if ($sa.enableHttpsTrafficOnly) { "HTTPS-only" } else { "HTTP allowed" }
            Write-Status $sa.name $status "$kind | $sku | $https"

            # Connectivity check
            try {
                $keys = az storage account keys list --account-name $sa.name --resource-group $ResourceGroup 2>&1 | ConvertFrom-Json
                if ($keys.Count -gt 0) {
                    Write-Status "  Keys" "Healthy" "Access keys available"
                }
            }
            catch {
                Write-Status "  Keys" "Warning" "Could not retrieve keys"
            }
        }
    }
}
catch {
    Write-Status "Storage" "Error" "Failed to query: $_"
}

# ── Check 7: Cosmos DB ──
Write-Host ""
Write-Host "Checking Cosmos DB Accounts..." -ForegroundColor Yellow
try {
    $cosmosAccounts = az cosmosdb list --resource-group $ResourceGroup 2>&1 | ConvertFrom-Json

    if ($cosmosAccounts.Count -eq 0) {
        Write-Status "Cosmos DB" "NotFound" "No Cosmos DB accounts in this resource group"
    }
    else {
        foreach ($cosmos in $cosmosAccounts) {
            $provisioningState = $cosmos.provisioningState
            $status = if ($provisioningState -eq "Succeeded") { "Healthy" } else { "Warning" }
            $apiKind = $cosmos.kind
            $endpoint = $cosmos.documentEndpoint
            $locations = ($cosmos.readLocations | ForEach-Object { $_.locationName }) -join ", "
            Write-Status $cosmos.name $status "$apiKind | $locations"
            Write-Status "  Endpoint" "Healthy" $endpoint
        }
    }
}
catch {
    Write-Status "Cosmos DB" "Error" "Failed to query: $_"
}

# ── Check 8: SQL Databases ──
Write-Host ""
Write-Host "Checking SQL Servers..." -ForegroundColor Yellow
try {
    $sqlServers = az sql server list --resource-group $ResourceGroup 2>&1 | ConvertFrom-Json

    if ($sqlServers.Count -eq 0) {
        Write-Status "SQL Server" "NotFound" "No SQL Servers in this resource group"
    }
    else {
        foreach ($sql in $sqlServers) {
            $state = $sql.state
            $status = if ($state -eq "Ready") { "Healthy" } else { "Warning" }
            Write-Status $sql.name $status "$state | $($sql.fullyQualifiedDomainName)"

            # List databases
            try {
                $dbs = az sql db list --server $sql.name --resource-group $ResourceGroup 2>&1 | ConvertFrom-Json
                foreach ($db in $dbs) {
                    if ($db.name -ne "master") {
                        $dbStatus = if ($db.status -eq "Online") { "Healthy" } else { "Warning" }
                        Write-Status "  $($db.name)" $dbStatus "$($db.status) | $($db.sku.name) | $($db.maxSizeBytes / 1GB)GB max"
                    }
                }
            }
            catch {
                Write-Status "  Databases" "Warning" "Could not list databases"
            }
        }
    }
}
catch {
    Write-Status "SQL Server" "Error" "Failed to query: $_"
}

# ── Summary ──
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Health check complete" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
