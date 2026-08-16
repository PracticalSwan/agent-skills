[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$SourceRoot = "",
    [string]$CodexRoot = "C:\Users\LOQ\.codex\skills",
    [string]$SharedRoot = "C:\Users\LOQ\.agents\skills",
    [string]$ClaudeRoot = "C:\Users\LOQ\.claude\skills",
    [switch]$SkipCodex,
    [switch]$SkipShared,
    [switch]$SkipClaude
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Downstream sync is locked to these three personal-global targets. Any other
# skill folder path (including workspace-local roots such as .agent\skills,
# .agents\skills, or .claude\skills under a project tree) is an upstream
# promotion source only, never a downstream sync destination.
$script:allowedDownstreamRoots = @(
    'C:\Users\LOQ\.agents\skills',
    'C:\Users\LOQ\.codex\skills',
    'C:\Users\LOQ\.claude\skills'
)

# These exact maintained-skill names were retired by the 2026-08-02 frontend
# consolidation. Prune only these known catalog-owned copies; preserve unknown
# personal skills and all host-managed folders.
$script:retiredCatalogSkills = @(
    'frontend-skill',
    'premium-frontend-ui'
)

function Get-NormalizedPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    return [System.IO.Path]::GetFullPath($Path)
}

function Assert-ApprovedDownstreamRoot {
    param(
        [Parameter(Mandatory = $true)]
        [string]$TargetRoot
    )

    $normalizedTarget = (Get-NormalizedPath $TargetRoot).TrimEnd("\")

    foreach ($allowedRoot in $script:allowedDownstreamRoots) {
        $normalizedAllowed = (Get-NormalizedPath $allowedRoot).TrimEnd("\")
        if ($normalizedTarget -eq $normalizedAllowed -or
            $normalizedTarget.StartsWith("$normalizedAllowed\", [System.StringComparison]::OrdinalIgnoreCase)) {
            return
        }
    }

    throw "Refusing to sync to '$TargetRoot' because it is not inside any of the approved downstream targets: $([string]::Join(', ', $script:allowedDownstreamRoots))."
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
        [string]$RootPath,
        [Parameter(Mandatory = $true)]
        [string[]]$CopiedOfficialNames
    )

    $skillDirs = Get-ChildItem -LiteralPath $RootPath -Directory | Where-Object {
        Test-Path (Join-Path $_.FullName "SKILL.md")
    }

    return [pscustomobject]@{
        Maintained = @($skillDirs | Where-Object { $CopiedOfficialNames -notcontains $_.Name } | Sort-Object Name)
        CopiedOfficial = @($skillDirs | Where-Object { $CopiedOfficialNames -contains $_.Name } | Sort-Object Name)
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

    Assert-ApprovedDownstreamRoot -TargetRoot $TargetRoot

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

function Remove-RetiredRouteCopies {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$SkillNames,
        [Parameter(Mandatory = $true)]
        [string]$TargetRoot,
        [Parameter(Mandatory = $true)]
        [string]$Label
    )

    Assert-ApprovedDownstreamRoot -TargetRoot $TargetRoot
    $removed = New-Object System.Collections.Generic.List[string]

    foreach ($skillName in @($SkillNames | Sort-Object -Unique)) {
        if ($skillName -notmatch '^[a-z0-9]+(?:-[a-z0-9]+)*$') {
            throw "Refusing to prune invalid skill folder name '$skillName'."
        }
        $targetSkillPath = Join-Path $TargetRoot $skillName
        Assert-WithinRoot -CandidatePath $targetSkillPath -RootPath $TargetRoot
        if (Test-Path -LiteralPath $targetSkillPath) {
            if ($PSCmdlet.ShouldProcess($targetSkillPath, "Remove stale $Label skill copy")) {
                Remove-Item -LiteralPath $targetSkillPath -Recurse -Force
            }
            $removed.Add($skillName) | Out-Null
        }
    }

    return $removed
}

$defaultSourceRoot = Join-Path (Split-Path -Parent $PSCommandPath) ".."
if ([string]::IsNullOrWhiteSpace($SourceRoot)) {
    $SourceRoot = $defaultSourceRoot
}

$workspaceRoot = Get-NormalizedPath $SourceRoot
$codexRootPath = Get-NormalizedPath $CodexRoot
$sharedRootPath = Get-NormalizedPath $SharedRoot
$claudeRootPath = Get-NormalizedPath $ClaudeRoot
$sharedSuperpowersRoot = Join-Path $sharedRootPath "superpowers"

if (-not (Test-Path -LiteralPath $workspaceRoot)) {
    throw "Source root '$workspaceRoot' does not exist."
}

# The shared superpowers folder is a subfolder of the approved .agents\skills
# root, so it inherits that approval rather than being its own downstream target.
if (-not (Test-Path -LiteralPath $sharedSuperpowersRoot)) {
    throw "Shared superpowers root '$sharedSuperpowersRoot' does not exist."
}

$registryPath = Join-Path $workspaceRoot "scripts\skill-registry.json"
if (-not (Test-Path -LiteralPath $registryPath)) {
    throw "Skill registry '$registryPath' does not exist."
}

$registry = Get-Content -LiteralPath $registryPath -Raw | ConvertFrom-Json
$copiedOfficialNames = @($registry.copied_official_superpowers)
$codexSystemManagedNames = @($registry.codex_system_managed_skills)
$codexLocalOnlyNames = @($registry.codex_local_only_skill_names)
if ($copiedOfficialNames.Count -eq 0) {
    throw "Skill registry '$registryPath' does not define copied_official_superpowers."
}

$skillSet = Get-SkillSet -RootPath $workspaceRoot -CopiedOfficialNames $copiedOfficialNames
$codexLocalOnlyConflicts = @(
    $skillSet.Maintained |
        Where-Object { $codexLocalOnlyNames -contains $_.Name } |
        Select-Object -ExpandProperty Name
)
if ($codexLocalOnlyConflicts.Count -gt 0) {
    throw "Codex-local-only skills must not exist in the parent catalog: $($codexLocalOnlyConflicts -join ', ')"
}
$codexMaintained = @(
    $skillSet.Maintained |
        Where-Object { $codexSystemManagedNames -notcontains $_.Name } |
        Sort-Object Name
)

$summary = [ordered]@{
    source = [ordered]@{
        root = $workspaceRoot
        maintained_count = $skillSet.Maintained.Count
        copied_official_count = $skillSet.CopiedOfficial.Count
    }
    codex = [ordered]@{
        root = $codexRootPath
        synced_maintained = @()
        skipped_system_managed = @(
            $skillSet.Maintained |
                Where-Object { $codexSystemManagedNames -contains $_.Name } |
                Select-Object -ExpandProperty Name
        )
        pruned_stale_system_mirrors = @()
        pruned_stale_superpowers = @()
        pruned_retired_skills = @()
    }
    shared = [ordered]@{
        root = $sharedRootPath
        synced_maintained = @()
        synced_superpowers = @()
        pruned_top_level_superpowers = @()
        pruned_retired_skills = @()
    }
    claude = [ordered]@{
        root = $claudeRootPath
        synced_maintained = @()
        skipped_superpowers = @($skillSet.CopiedOfficial | Select-Object -ExpandProperty Name)
        pruned_top_level_superpowers = @()
        pruned_retired_skills = @()
    }
}

if (-not $SkipCodex) {
    $summary.codex.pruned_stale_system_mirrors = @(
        Remove-RetiredRouteCopies `
            -SkillNames $codexSystemManagedNames `
            -TargetRoot $codexRootPath `
            -Label "top-level Codex system-shadow"
    )
    $summary.codex.pruned_stale_superpowers = @(
        Remove-RetiredRouteCopies `
            -SkillNames $copiedOfficialNames `
            -TargetRoot $codexRootPath `
            -Label "top-level Codex Superpower"
    )
    $summary.codex.pruned_retired_skills = @(
        Remove-RetiredRouteCopies `
            -SkillNames $script:retiredCatalogSkills `
            -TargetRoot $codexRootPath `
            -Label "retired frontend catalog"
    )
    $summary.codex.synced_maintained = @(
        Sync-SkillFolders -SkillDirs $codexMaintained -TargetRoot $codexRootPath -Label "Codex maintained"
    )
}

if (-not $SkipShared) {
    $summary.shared.pruned_top_level_superpowers = @(
        Remove-RetiredRouteCopies `
            -SkillNames $copiedOfficialNames `
            -TargetRoot $sharedRootPath `
            -Label "top-level shared Superpower"
    )
    $summary.shared.pruned_retired_skills = @(
        Remove-RetiredRouteCopies `
            -SkillNames $script:retiredCatalogSkills `
            -TargetRoot $sharedRootPath `
            -Label "retired frontend catalog"
    )
    $summary.shared.synced_maintained = @(
        Sync-SkillFolders -SkillDirs $skillSet.Maintained -TargetRoot $sharedRootPath -Label "Shared maintained"
    )
    $summary.shared.synced_superpowers = @(
        Sync-SkillFolders -SkillDirs $skillSet.CopiedOfficial -TargetRoot $sharedSuperpowersRoot -Label "Shared superpower"
    )
}

if (-not $SkipClaude) {
    $summary.claude.pruned_top_level_superpowers = @(
        Remove-RetiredRouteCopies `
            -SkillNames $copiedOfficialNames `
            -TargetRoot $claudeRootPath `
            -Label "top-level Claude Superpower"
    )
    $summary.claude.pruned_retired_skills = @(
        Remove-RetiredRouteCopies `
            -SkillNames $script:retiredCatalogSkills `
            -TargetRoot $claudeRootPath `
            -Label "retired frontend catalog"
    )
    $summary.claude.synced_maintained = @(
        Sync-SkillFolders -SkillDirs $skillSet.Maintained -TargetRoot $claudeRootPath -Label "Claude maintained"
    )
}

$summary | ConvertTo-Json -Depth 5
