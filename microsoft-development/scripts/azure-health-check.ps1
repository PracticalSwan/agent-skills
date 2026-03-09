<#
.SYNOPSIS
    Report the health of common Azure resources in a resource group.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ResourceGroup,

    [string]$SubscriptionId
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-State {
    param(
        [string]$Name,
        [string]$State,
        [string]$Detail = ""
    )

    $color = switch ($State) {
        "Healthy" { "Green" }
        "Warning" { "Yellow" }
        "Missing" { "DarkYellow" }
        "Error" { "Red" }
        default { "White" }
    }

    $suffix = if ($Detail) { " - $Detail" } else { "" }
    Write-Host ("[{0}] {1}{2}" -f $State, $Name, $suffix) -ForegroundColor $color
}

function Assert-Command {
    param([string]$Name)
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found in PATH."
    }
}

Assert-Command az

az account show *> $null
if ($LASTEXITCODE -ne 0) {
    throw "Azure CLI is not logged in. Run 'az login' first."
}

if ($SubscriptionId) {
    az account set --subscription $SubscriptionId | Out-Null
}

$exists = az group exists --name $ResourceGroup
if ($exists -eq "false") {
    Write-State -Name $ResourceGroup -State "Missing" -Detail "resource group does not exist"
    exit 1
}

Write-State -Name $ResourceGroup -State "Healthy" -Detail "resource group found"
Write-Host ""

$webapps = az webapp list --resource-group $ResourceGroup | ConvertFrom-Json
if (-not $webapps) {
    Write-State -Name "Web Apps" -State "Missing"
} else {
    foreach ($app in $webapps) {
        $state = if ($app.state -eq "Running") { "Healthy" } else { "Warning" }
        Write-State -Name $app.name -State $state -Detail "$($app.state) $($app.defaultHostName)"
    }
}

$functions = az functionapp list --resource-group $ResourceGroup | ConvertFrom-Json
if (-not $functions) {
    Write-State -Name "Function Apps" -State "Missing"
} else {
    foreach ($app in $functions) {
        $state = if ($app.state -eq "Running") { "Healthy" } else { "Warning" }
        Write-State -Name $app.name -State $state -Detail "$($app.state) $($app.defaultHostName)"
    }
}

$storageAccounts = az storage account list --resource-group $ResourceGroup | ConvertFrom-Json
if (-not $storageAccounts) {
    Write-State -Name "Storage Accounts" -State "Missing"
} else {
    foreach ($account in $storageAccounts) {
        $state = if ($account.provisioningState -eq "Succeeded") { "Healthy" } else { "Warning" }
        Write-State -Name $account.name -State $state -Detail "$($account.kind) $($account.sku.name)"
    }
}

$sqlServers = az sql server list --resource-group $ResourceGroup | ConvertFrom-Json
if (-not $sqlServers) {
    Write-State -Name "SQL Servers" -State "Missing"
} else {
    foreach ($server in $sqlServers) {
        Write-State -Name $server.name -State "Healthy" -Detail $server.fullyQualifiedDomainName
    }
}

$cosmosAccounts = az cosmosdb list --resource-group $ResourceGroup | ConvertFrom-Json
if (-not $cosmosAccounts) {
    Write-State -Name "Cosmos DB" -State "Missing"
} else {
    foreach ($account in $cosmosAccounts) {
        $state = if ($account.provisioningState -eq "Succeeded") { "Healthy" } else { "Warning" }
        Write-State -Name $account.name -State $state -Detail $account.kind
    }
}
