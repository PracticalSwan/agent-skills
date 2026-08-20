[CmdletBinding()]
param(
    [switch]$SkipFetch
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$registryPath = Join-Path $PSScriptRoot "skill-registry.json"
$registry = Get-Content -LiteralPath $registryPath -Raw | ConvertFrom-Json
$config = $registry.codex_local_only_skill_sets.blender_skills

$checkout = [System.IO.Path]::GetFullPath($config.checkout)
$sourceRoot = Join-Path $checkout $config.source_subdir
$installRoot = [System.IO.Path]::GetFullPath($config.install_root)
$manifestPath = [System.IO.Path]::GetFullPath($config.manifest)
$sharedReferencesName = $config.shared_references
$extraProtectedSkillNames = @($config.extra_protected_skill_names)
foreach ($name in $extraProtectedSkillNames) {
    if ($name -notmatch '^[a-z0-9]+(?:-[a-z0-9]+)*$') { throw "Invalid protected Blender overlay skill name: $name" }
}

$expectedCheckout = "C:\Users\LOQ\.codex\vendor\blender-skills"
$expectedInstallRoot = "C:\Users\LOQ\.codex\skills"
if ($checkout.TrimEnd("\") -ne $expectedCheckout) {
    throw "Refusing unexpected Blender checkout path: $checkout"
}
if ($installRoot.TrimEnd("\") -ne $expectedInstallRoot) {
    throw "Refusing unexpected Blender install root: $installRoot"
}
if ($config.scope -ne "codex-only" -or
    -not $config.never_promote_to_parent -or
    -not $config.never_sync_to_shared -or
    -not $config.never_sync_to_claude) {
    throw "Codex-local-only Blender policy flags are missing or disabled."
}

if (-not (Test-Path -LiteralPath $checkout)) {
    New-Item -ItemType Directory -Force (Split-Path -Parent $checkout) | Out-Null
    git clone $config.repo $checkout
}
$checkoutStatus = @(git -C $checkout status --porcelain)
if ($checkoutStatus.Count -ne 0) {
    throw "Blender skills checkout is dirty; refusing to update or overwrite it."
}
if (-not $SkipFetch) {
    git -C $checkout fetch origin $config.branch
    git -C $checkout checkout $config.branch
    git -C $checkout merge --ff-only "origin/$($config.branch)"
}

if (-not (Test-Path -LiteralPath $sourceRoot)) {
    throw "Blender skill source root does not exist: $sourceRoot"
}
if (-not (Test-Path -LiteralPath $installRoot)) {
    throw "Codex skill root does not exist: $installRoot"
}

$skillDirs = @(
    Get-ChildItem -LiteralPath $sourceRoot -Directory |
        Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md") } |
        Sort-Object Name
)
$skillNames = @($skillDirs | Select-Object -ExpandProperty Name)
if ($skillNames.Count -eq 0) {
    throw "No Blender SKILL.md directories were discovered."
}
$previousOwned = @()
$previousOwnsReferences = $false
if (Test-Path -LiteralPath $manifestPath) {
    $previousManifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    $previousOwned = @($previousManifest.skill_names)
    $previousOwnsReferences = [bool]$previousManifest.owns_shared_references
}

$collisions = @(
    $skillNames | Where-Object {
        (Test-Path -LiteralPath (Join-Path $installRoot $_)) -and
        ($previousOwned -notcontains $_)
    }
)
if ($collisions.Count -gt 0) {
    throw "Refusing to overwrite non-owned Codex skills: $($collisions -join ', ')"
}

$sharedSource = Join-Path $sourceRoot $sharedReferencesName
$sharedDestination = Join-Path $installRoot $sharedReferencesName
if ((Test-Path -LiteralPath $sharedDestination) -and -not $previousOwnsReferences) {
    throw "Refusing to overwrite non-owned shared references: $sharedDestination"
}
$staleOwned = @($previousOwned | Where-Object { $skillNames -notcontains $_ })
foreach ($name in $staleOwned) {
    if ($name -notmatch '^[a-z0-9]+(?:-[a-z0-9]+)*$') {
        throw "Invalid previously owned Blender skill name: $name"
    }
    $destination = Join-Path $installRoot $name
    if (Test-Path -LiteralPath $destination) {
        Remove-Item -LiteralPath $destination -Recurse -Force
    }
}

foreach ($skillDir in $skillDirs) {
    $destination = Join-Path $installRoot $skillDir.Name
    if (Test-Path -LiteralPath $destination) {
        Remove-Item -LiteralPath $destination -Recurse -Force
    }
    Copy-Item -LiteralPath $skillDir.FullName -Destination $installRoot -Recurse -Force
}

if (-not (Test-Path -LiteralPath $sharedSource)) {
    throw "Upstream shared references folder is missing: $sharedSource"
}
if (Test-Path -LiteralPath $sharedDestination) {
    Remove-Item -LiteralPath $sharedDestination -Recurse -Force
}
Copy-Item -LiteralPath $sharedSource -Destination $installRoot -Recurse -Force

function Get-TreeDigest {
    param([Parameter(Mandatory = $true)][string]$Root)
    $normalizedRoot = [System.IO.Path]::GetFullPath($Root).TrimEnd("\")
    $lines = @(
        Get-ChildItem -LiteralPath $normalizedRoot -File -Recurse |
            Sort-Object FullName |
            ForEach-Object {
                $relative = $_.FullName.Substring($normalizedRoot.Length).TrimStart("\").Replace("\", "/")
                $hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
                "$relative|$hash"
            }
    )
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [System.Text.Encoding]::UTF8.GetBytes(($lines -join "`n"))
        return ([System.BitConverter]::ToString($sha.ComputeHash($bytes))).Replace("-", "").ToLowerInvariant()
    } finally {
        $sha.Dispose()
    }
}
foreach ($skillDir in $skillDirs) {
    $sourceDigest = Get-TreeDigest -Root $skillDir.FullName
    $destination = Join-Path $installRoot $skillDir.Name
    $destinationDigest = Get-TreeDigest -Root $destination
    if ($sourceDigest -ne $destinationDigest) {
        throw "Installed Blender skill differs from upstream: $($skillDir.Name)"
    }
}
if ((Get-TreeDigest -Root $sharedSource) -ne (Get-TreeDigest -Root $sharedDestination)) {
    throw "Installed Blender shared references differ from upstream."
}

$protectedSkillNames = @($skillNames + $extraProtectedSkillNames | Sort-Object -Unique)
foreach ($name in $extraProtectedSkillNames) {
    if (-not (Test-Path -LiteralPath (Join-Path (Join-Path $installRoot $name) "SKILL.md"))) {
        throw "Protected Codex-local Blender overlay is missing: $installRoot\$name"
    }
}
$forbiddenRoots = @(
    $repoRoot,
    "C:\Users\LOQ\.agents\skills",
    "C:\Users\LOQ\.claude\skills"
)
foreach ($root in $forbiddenRoots) {
    foreach ($name in $protectedSkillNames) {
        if (Test-Path -LiteralPath (Join-Path (Join-Path $root $name) "SKILL.md")) {
            throw "Codex-local-only Blender skill escaped into forbidden root: $root\$name"
        }
    }
}
$commit = (git -C $checkout rev-parse HEAD).Trim()
$manifest = [ordered]@{
    name = "arjun988/blender-skills"
    repo = $config.repo
    branch = $config.branch
    upstream_commit = $commit
    checkout = $checkout
    source_subdir = $config.source_subdir
    install_root = $installRoot
    scope = "codex-only"
    never_promote_to_parent = $true
    never_sync_to_shared = $true
    never_sync_to_claude = $true
    owns_shared_references = $true
    skill_count = $skillNames.Count
    skill_names = $skillNames
    updated_at = (Get-Date).ToUniversalTime().ToString("o")
}
$manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

python (Join-Path $PSScriptRoot "update-codex-local-blender-registry.py")
if ($LASTEXITCODE -ne 0) {
    throw "Failed to update Blender local-only registry metadata."
}
[ordered]@{
    status = "ok"
    scope = "codex-only"
    upstream_commit = $commit
    skill_count = $skillNames.Count
    installed_root = $installRoot
    removed_upstream_skills = $staleOwned
    shared_references = $sharedDestination
    manifest = $manifestPath
} | ConvertTo-Json -Depth 5
