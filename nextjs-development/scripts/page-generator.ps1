# Next.js App Router Page Generator
# Scaffolds page, loading, and error files for a given route segment.
# Usage: .\page-generator.ps1 -Route "blog/[slug]"
#        .\page-generator.ps1 -Route "dashboard/settings" -AppDir "src/app"

param(
    [Parameter(Mandatory = $true)]
    [string]$Route,

    [string]$AppDir = "app"
)

# Resolve the target directory relative to current working directory
$targetDir = Join-Path (Get-Location) $AppDir $Route

# Create the directory if it doesn't exist
if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    Write-Host "Created directory: $targetDir" -ForegroundColor Green
}

# Derive a PascalCase component name from the route (strip dynamic segments for naming)
$componentBase = ($Route -split '/')[-1]
$componentBase = $componentBase -replace '[\[\]\.]+', ''
$componentName = (Get-Culture).TextInfo.ToTitleCase($componentBase) -replace '\s', ''
if (-not $componentName) { $componentName = "Page" }

# --- page.tsx ---
$pageFile = Join-Path $targetDir "page.tsx"
if (-not (Test-Path $pageFile)) {
    # Detect if the route has dynamic segments
    $hasDynamicSegment = $Route -match '\[.+?\]'

    if ($hasDynamicSegment) {
        # Extract param names from brackets
        $paramMatches = [regex]::Matches($Route, '\[(?:\.{3})?(\w+)\]')
        $paramNames = $paramMatches | ForEach-Object { $_.Groups[1].Value }
        $paramsType = ($paramNames | ForEach-Object { "  $($_): string" }) -join "`n"
        $paramsDestructure = ($paramNames | ForEach-Object { $_ }) -join ", "

        $pageContent = @"
interface Props {
  params: Promise<{
$paramsType
  }>
}

export default async function ${componentName}Page({ params }: Props) {
  const { $paramsDestructure } = await params

  return (
    <main>
      <h1>${componentName}</h1>
    </main>
  )
}
"@
    } else {
        $pageContent = @"
export default async function ${componentName}Page() {
  return (
    <main>
      <h1>${componentName}</h1>
    </main>
  )
}
"@
    }

    Set-Content -Path $pageFile -Value $pageContent -Encoding UTF8
    Write-Host "Created: $pageFile" -ForegroundColor Cyan
} else {
    Write-Host "Skipped (exists): $pageFile" -ForegroundColor Yellow
}

# --- loading.tsx ---
$loadingFile = Join-Path $targetDir "loading.tsx"
if (-not (Test-Path $loadingFile)) {
    $loadingContent = @"
export default function ${componentName}Loading() {
  return (
    <div role="status" aria-label="Loading...">
      <span>Loading…</span>
    </div>
  )
}
"@
    Set-Content -Path $loadingFile -Value $loadingContent -Encoding UTF8
    Write-Host "Created: $loadingFile" -ForegroundColor Cyan
} else {
    Write-Host "Skipped (exists): $loadingFile" -ForegroundColor Yellow
}

# --- error.tsx ---
$errorFile = Join-Path $targetDir "error.tsx"
if (-not (Test-Path $errorFile)) {
    $errorContent = @"
'use client'

import { useEffect } from 'react'

interface Props {
  error: Error & { digest?: string }
  reset: () => void
}

export default function ${componentName}Error({ error, reset }: Props) {
  useEffect(() => {
    console.error(error)
  }, [error])

  return (
    <div role="alert">
      <h2>Something went wrong</h2>
      <button onClick={reset}>Try again</button>
    </div>
  )
}
"@
    Set-Content -Path $errorFile -Value $errorContent -Encoding UTF8
    Write-Host "Created: $errorFile" -ForegroundColor Cyan
} else {
    Write-Host "Skipped (exists): $errorFile" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Done. Route segment scaffolded at: $targetDir" -ForegroundColor Green
