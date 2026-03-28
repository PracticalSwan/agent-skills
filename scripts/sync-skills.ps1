[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$SourceRoot = "",
    [string]$CodexRoot = "C:\Users\LOQ\.agents\skills",
    [string]$ClaudeRoot = "C:\Users\LOQ\.claude\skills",
    [switch]$SkipCodex,
    [switch]$SkipClaude
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-NormalizedPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    return [System.IO.Path]::GetFullPath($Path)
}

function Assert-WithinRoot {
    param(
        [Parameter(Mandatory = $true)]
        [string]$CandidatePath,
        [Parameter(Mandatory = $true)]
        [string]$RootPath
    )

    $normalizedRoot = (Get-NormalizedPath $RootPath).TrimEnd("\")
    $normalizedCandidate = Get-NormalizedPath $CandidatePath

    if (-not $normalizedCandidate.StartsWith("$normalizedRoot\", [System.StringComparison]::OrdinalIgnoreCase) -and
        $normalizedCandidate -ne $normalizedRoot) {
        throw "Refusing to touch '$normalizedCandidate' because it is outside '$normalizedRoot'."
    }
}

function Get-SkillSet {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RootPath
    )

    $skillDirs = Get-ChildItem -LiteralPath $RootPath -Directory | Where-Object {
        Test-Path (Join-Path $_.FullName "SKILL.md")
    }

    return [pscustomobject]@{
        Maintained = @($skillDirs | Where-Object { Test-Path (Join-Path $_.FullName "CHANGELOG.md") } | Sort-Object Name)
        CopiedOfficial = @($skillDirs | Where-Object { -not (Test-Path (Join-Path $_.FullName "CHANGELOG.md")) } | Sort-Object Name)
    }
}

function Sync-SkillFolders {
    param(
        [Parameter(Mandatory = $true)]
        [System.IO.DirectoryInfo[]]$SkillDirs,
        [Parameter(Mandatory = $true)]
        [string]$TargetRoot,
        [Parameter(Mandatory = $true)]
        [string]$Label
    )

    if (-not (Test-Path -LiteralPath $TargetRoot)) {
        throw "Target root '$TargetRoot' does not exist."
    }

    $synced = New-Object System.Collections.Generic.List[string]

    foreach ($skillDir in $SkillDirs) {
        $targetSkillPath = Join-Path $TargetRoot $skillDir.Name
        Assert-WithinRoot -CandidatePath $targetSkillPath -RootPath $TargetRoot

        if (Test-Path -LiteralPath $targetSkillPath) {
            if ($PSCmdlet.ShouldProcess($targetSkillPath, "Replace existing $Label skill copy")) {
                Remove-Item -LiteralPath $targetSkillPath -Recurse -Force
            }
        }

        if ($PSCmdlet.ShouldProcess($targetSkillPath, "Copy $Label skill from workspace")) {
            Copy-Item -LiteralPath $skillDir.FullName -Destination $TargetRoot -Recurse -Force
        }

        $synced.Add($skillDir.Name) | Out-Null
    }

    return $synced
}

$defaultSourceRoot = Join-Path (Split-Path -Parent $PSCommandPath) ".."
if ([string]::IsNullOrWhiteSpace($SourceRoot)) {
    $SourceRoot = $defaultSourceRoot
}

$workspaceRoot = Get-NormalizedPath $SourceRoot
$codexRootPath = Get-NormalizedPath $CodexRoot
$claudeRootPath = Get-NormalizedPath $ClaudeRoot
$codexSuperpowersRoot = Join-Path $codexRootPath "superpowers"

if (-not (Test-Path -LiteralPath $workspaceRoot)) {
    throw "Source root '$workspaceRoot' does not exist."
}

if (-not (Test-Path -LiteralPath $codexSuperpowersRoot)) {
    throw "Codex superpowers root '$codexSuperpowersRoot' does not exist."
}

$skillSet = Get-SkillSet -RootPath $workspaceRoot

$summary = [ordered]@{
    workspace = [ordered]@{
        root = $workspaceRoot
        maintained_count = $skillSet.Maintained.Count
        copied_official_count = $skillSet.CopiedOfficial.Count
    }
    codex = [ordered]@{
        root = $codexRootPath
        synced_maintained = @()
        synced_superpowers = @()
    }
    claude = [ordered]@{
        root = $claudeRootPath
        synced_maintained = @()
        skipped_superpowers = @($skillSet.CopiedOfficial | Select-Object -ExpandProperty Name)
    }
}

if (-not $SkipCodex) {
    $summary.codex.synced_maintained = @(
        Sync-SkillFolders -SkillDirs $skillSet.Maintained -TargetRoot $codexRootPath -Label "Codex maintained"
    )
    $summary.codex.synced_superpowers = @(
        Sync-SkillFolders -SkillDirs $skillSet.CopiedOfficial -TargetRoot $codexSuperpowersRoot -Label "Codex superpower"
    )
}

if (-not $SkipClaude) {
    $summary.claude.synced_maintained = @(
        Sync-SkillFolders -SkillDirs $skillSet.Maintained -TargetRoot $claudeRootPath -Label "Claude maintained"
    )
}

$summary | ConvertTo-Json -Depth 5
