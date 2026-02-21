<#
.SYNOPSIS
    Backs up Serena project memories to a timestamped local directory.

.DESCRIPTION
    Reads the .serena/ directory in a project, copies all memory files to a
    timestamped backup folder, and generates an index of all memories with
    dates, sizes, and a summary table.

.PARAMETER ProjectDir
    Path to the project root containing the .serena/ directory.
    Defaults to the current directory.

.PARAMETER BackupDir
    Path where backups will be stored.
    Defaults to .serena-backups/ inside the project directory.

.EXAMPLE
    .\serena-memory-backup.ps1 -ProjectDir "C:\Projects\MyApp"

.EXAMPLE
    .\serena-memory-backup.ps1 -ProjectDir "." -BackupDir "D:\Backups\serena"
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$ProjectDir = ".",

    [Parameter(Position = 1)]
    [string]$BackupDir
)

$ErrorActionPreference = "Stop"

$ProjectDir = Resolve-Path -Path $ProjectDir
$serenaDir = Join-Path $ProjectDir ".serena"

if (-not (Test-Path $serenaDir)) {
    Write-Error "No .serena/ directory found in '$ProjectDir'. Nothing to back up."
    exit 1
}

if (-not $BackupDir) {
    $BackupDir = Join-Path $ProjectDir ".serena-backups"
}

$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$targetDir = Join-Path $BackupDir $timestamp

Write-Host "Serena Memory Backup" -ForegroundColor Cyan
Write-Host "  Source:  $serenaDir"
Write-Host "  Target:  $targetDir"
Write-Host ""

New-Item -ItemType Directory -Path $targetDir -Force | Out-Null

$memoryFiles = Get-ChildItem -Path $serenaDir -File -Recurse
if ($memoryFiles.Count -eq 0) {
    Write-Warning "No memory files found in .serena/ directory."
    exit 0
}

$indexEntries = @()

foreach ($file in $memoryFiles) {
    $relativePath = $file.FullName.Substring($serenaDir.Length + 1)
    $destPath = Join-Path $targetDir $relativePath
    $destDir = Split-Path $destPath -Parent

    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }

    Copy-Item -Path $file.FullName -Destination $destPath -Force

    $sizeKB = [math]::Round($file.Length / 1024, 2)
    $indexEntries += [PSCustomObject]@{
        Name         = $relativePath
        Size         = "$sizeKB KB"
        LastModified = $file.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
        Lines        = (Get-Content -Path $file.FullName | Measure-Object -Line).Lines
    }
}

$indexContent = @"
# Serena Memory Backup Index

**Backup Date:** $($timestamp -replace '_', ' ')
**Source Project:** $ProjectDir
**Total Memories:** $($memoryFiles.Count)
**Total Size:** $([math]::Round(($memoryFiles | Measure-Object -Property Length -Sum).Sum / 1024, 2)) KB

## Memory Files

| File | Size | Lines | Last Modified |
|------|------|-------|---------------|
"@

foreach ($entry in $indexEntries | Sort-Object Name) {
    $indexContent += "`n| $($entry.Name) | $($entry.Size) | $($entry.Lines) | $($entry.LastModified) |"
}

$indexPath = Join-Path $targetDir "BACKUP_INDEX.md"
Set-Content -Path $indexPath -Value $indexContent -Encoding UTF8

Write-Host "Backup complete." -ForegroundColor Green
Write-Host "  Files copied: $($memoryFiles.Count)"
Write-Host "  Index:        $indexPath"
Write-Host ""

$indexEntries | Sort-Object Name | Format-Table -AutoSize
