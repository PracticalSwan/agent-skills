# Shell Scripting Patterns for Automation

> PowerShell and Bash patterns side-by-side for cross-platform automation.

---

## Script Boilerplate

### Bash

```bash
#!/usr/bin/env bash
set -euo pipefail                  # Exit on error, undefined vars, pipe failures
IFS=$'\n\t'                        # Safer field separator

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_NAME="$(basename "$0")"
```

### PowerShell

```powershell
#Requires -Version 7.0
$ErrorActionPreference = "Stop"    # Exit on terminating errors
Set-StrictMode -Version Latest     # Catch undefined variables

$ScriptDir = $PSScriptRoot
$ScriptName = $MyInvocation.MyCommand.Name
```

---

## Argument Parsing

### Bash (getopts)

```bash
usage() {
    echo "Usage: $SCRIPT_NAME -n <name> -e <env> [-v] [-h]"
    echo "  -n  Project name (required)"
    echo "  -e  Environment: dev|staging|prod (required)"
    echo "  -v  Verbose output"
    echo "  -h  Show this help"
    exit 1
}

VERBOSE=false
while getopts "n:e:vh" opt; do
    case $opt in
        n) NAME="$OPTARG" ;;
        e) ENV="$OPTARG" ;;
        v) VERBOSE=true ;;
        h) usage ;;
        *) usage ;;
    esac
done

[[ -z "${NAME:-}" || -z "${ENV:-}" ]] && usage
```

### PowerShell (param block)

```powershell
param(
    [Parameter(Mandatory = $true)]
    [string]$Name,

    [Parameter(Mandatory = $true)]
    [ValidateSet("dev", "staging", "prod")]
    [string]$Env,

    [switch]$Verbose
)
```

---

## Error Handling

### Bash (trap)

```bash
cleanup() {
    local exit_code=$?
    echo "Cleaning up temporary files..."
    rm -rf "$TEMP_DIR"
    exit $exit_code
}
trap cleanup EXIT                  # Always runs on script exit
trap 'echo "Error on line $LINENO"; exit 1' ERR  # Runs on error

TEMP_DIR=$(mktemp -d)
# ... script work ...
```

### PowerShell (try/catch/finally)

```powershell
$tempDir = Join-Path $env:TEMP "script-$(Get-Random)"
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

try {
    # ... script work ...
    throw "Something went wrong"
}
catch {
    Write-Error "Error: $_"
    exit 1
}
finally {
    if (Test-Path $tempDir) {
        Remove-Item -Recurse -Force $tempDir
    }
}
```

---

## Logging Functions

### Bash

```bash
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[0;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m'

log_info()  { echo -e "${BLUE}[INFO]${NC}  $(date '+%H:%M:%S') $*"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}    $(date '+%H:%M:%S') $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $(date '+%H:%M:%S') $*" >&2; }
log_error() { echo -e "${RED}[ERROR]${NC} $(date '+%H:%M:%S') $*" >&2; }

log_info "Starting deployment"
log_ok "Build completed"
log_warn "Cache miss — cold install"
log_error "Tests failed"
```

### PowerShell

```powershell
function Write-Log {
    param(
        [string]$Message,
        [ValidateSet("INFO", "OK", "WARN", "ERROR")]
        [string]$Level = "INFO"
    )
    $timestamp = Get-Date -Format "HH:mm:ss"
    $colors = @{ INFO = "Cyan"; OK = "Green"; WARN = "Yellow"; ERROR = "Red" }
    Write-Host "[$Level]  $timestamp $Message" -ForegroundColor $colors[$Level]
}

Write-Log "Starting deployment" -Level INFO
Write-Log "Build completed" -Level OK
Write-Log "Cache miss" -Level WARN
Write-Log "Tests failed" -Level ERROR
```

---

## File Operations

### Check existence

| Operation | Bash | PowerShell |
|-----------|------|------------|
| File exists | `[[ -f "$path" ]]` | `Test-Path $path -PathType Leaf` |
| Dir exists | `[[ -d "$path" ]]` | `Test-Path $path -PathType Container` |
| Is empty | `[[ ! -s "$path" ]]` | `(Get-Item $path).Length -eq 0` |
| Is writable | `[[ -w "$path" ]]` | `(Get-Acl $path).Access` |

### Common operations

**Bash:**
```bash
mkdir -p "$OUTPUT_DIR"
cp -r src/ "$OUTPUT_DIR/"
find . -name "*.log" -mtime +7 -delete        # Delete logs older than 7 days
find . -name "*.ts" -not -path "*/node_modules/*" | wc -l  # Count TS files
```

**PowerShell:**
```powershell
New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
Copy-Item -Path src\* -Destination $OutputDir -Recurse
Get-ChildItem -Recurse -Filter "*.log" |
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) } |
    Remove-Item
(Get-ChildItem -Recurse -Filter "*.ts" -Exclude "node_modules").Count
```

---

## JSON Processing

### Bash (jq)

```bash
# Read a field
VERSION=$(jq -r '.version' package.json)

# Update a field
jq '.version = "2.0.0"' package.json > tmp.json && mv tmp.json package.json

# Filter an array
jq '.dependencies | keys[]' package.json

# Build JSON from variables
jq -n --arg name "$NAME" --arg ver "$VERSION" \
  '{ name: $name, version: $ver }'

# Process API response
curl -s https://api.example.com/items |
  jq '.items[] | select(.status == "active") | .name'
```

### PowerShell (ConvertFrom-Json / ConvertTo-Json)

```powershell
# Read a field
$pkg = Get-Content package.json | ConvertFrom-Json
$version = $pkg.version

# Update a field
$pkg.version = "2.0.0"
$pkg | ConvertTo-Json -Depth 10 | Set-Content package.json

# Filter array
$pkg.dependencies.PSObject.Properties.Name

# Build JSON from variables
@{ name = $Name; version = $Version } | ConvertTo-Json

# Process API response
$items = Invoke-RestMethod https://api.example.com/items
$items.items | Where-Object { $_.status -eq "active" } | Select-Object name
```

---

## YAML Processing

### Bash (yq)

```bash
# Read value
yq '.services.web.image' docker-compose.yml

# Update value
yq -i '.services.web.image = "app:2.0"' docker-compose.yml

# Add an item to a list
yq -i '.services.web.environment += ["NEW_VAR=value"]' docker-compose.yml
```

### PowerShell (powershell-yaml module)

```powershell
Install-Module -Name powershell-yaml -Scope CurrentUser -Force

$yaml = Get-Content docker-compose.yml -Raw | ConvertFrom-Yaml
$yaml.services.web.image = "app:2.0"
$yaml | ConvertTo-Yaml | Set-Content docker-compose.yml
```

---

## Retry Logic

### Bash

```bash
retry() {
    local max_attempts=$1
    local delay=$2
    shift 2
    local cmd=("$@")

    for ((attempt = 1; attempt <= max_attempts; attempt++)); do
        if "${cmd[@]}"; then
            return 0
        fi
        echo "Attempt $attempt/$max_attempts failed. Retrying in ${delay}s..."
        sleep "$delay"
        delay=$((delay * 2))       # Exponential backoff
    done

    echo "All $max_attempts attempts failed."
    return 1
}

retry 3 5 curl --fail https://api.example.com/health
```

### PowerShell

```powershell
function Invoke-WithRetry {
    param(
        [scriptblock]$ScriptBlock,
        [int]$MaxAttempts = 3,
        [int]$DelaySeconds = 5
    )

    $attempt = 1
    $delay = $DelaySeconds

    while ($attempt -le $MaxAttempts) {
        try {
            return & $ScriptBlock
        }
        catch {
            Write-Warning "Attempt $attempt/$MaxAttempts failed: $_"
            if ($attempt -eq $MaxAttempts) { throw }
            Start-Sleep -Seconds $delay
            $delay *= 2             # Exponential backoff
            $attempt++
        }
    }
}

Invoke-WithRetry -MaxAttempts 3 -DelaySeconds 5 -ScriptBlock {
    Invoke-RestMethod https://api.example.com/health
}
```

---

## Parallel Execution

### Bash (xargs / GNU parallel)

```bash
# Process files in parallel (4 at a time)
find . -name "*.ts" | xargs -P 4 -I {} eslint {}

# GNU parallel
parallel -j 4 ./process.sh ::: file1.txt file2.txt file3.txt

# Background jobs
for server in web api worker; do
    deploy "$server" &
done
wait                               # Wait for all background jobs
echo "All deployments finished"
```

### PowerShell (ForEach-Object -Parallel)

```powershell
# Requires PowerShell 7+
$files = Get-ChildItem -Filter "*.ts" -Recurse
$files | ForEach-Object -Parallel {
    & eslint $_.FullName
} -ThrottleLimit 4

# Job-based
$servers = @("web", "api", "worker")
$jobs = $servers | ForEach-Object {
    Start-Job -ScriptBlock { param($s) & ./deploy.ps1 $s } -ArgumentList $_
}
$jobs | Wait-Job | Receive-Job
```

---

## Environment Variable Management

### Bash

```bash
# Load .env file
if [[ -f .env ]]; then
    set -a                         # Auto-export all variables
    source .env
    set +a
fi

# Default values
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"

# Required variables
: "${API_KEY:?ERROR: API_KEY is not set}"

# Export for child processes
export BUILD_VERSION="1.2.3"
```

### PowerShell

```powershell
# Load .env file
if (Test-Path .env) {
    Get-Content .env | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
            [Environment]::SetEnvironmentVariable($Matches[1].Trim(), $Matches[2].Trim(), "Process")
        }
    }
}

# Default values
$dbHost = if ($env:DB_HOST) { $env:DB_HOST } else { "localhost" }
$dbPort = if ($env:DB_PORT) { $env:DB_PORT } else { "5432" }

# Required variables
if (-not $env:API_KEY) {
    throw "ERROR: API_KEY is not set"
}

# Set for child processes
$env:BUILD_VERSION = "1.2.3"
```

---

## Common Automation Recipes

### 1. Health Check Script

```bash
check_health() {
    local url=$1
    local status
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    if [[ "$status" == "200" ]]; then
        log_ok "$url is healthy"
    else
        log_error "$url returned $status"
        return 1
    fi
}

check_health https://api.example.com/health
check_health https://web.example.com/health
```

### 2. Database Backup

```powershell
param(
    [string]$ConnectionString,
    [string]$BackupDir = "./backups"
)

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupFile = Join-Path $BackupDir "backup-$timestamp.sql"

New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null

& pg_dump $ConnectionString --file $backupFile --format=custom

$backups = Get-ChildItem $BackupDir -Filter "backup-*.sql" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -Skip 7
$backups | Remove-Item -Force            # Keep only 7 most recent
```

### 3. Version Bump

```bash
bump_version() {
    local part=$1                  # major, minor, patch
    local current
    current=$(jq -r '.version' package.json)

    IFS='.' read -r major minor patch <<< "$current"

    case $part in
        major) major=$((major + 1)); minor=0; patch=0 ;;
        minor) minor=$((minor + 1)); patch=0 ;;
        patch) patch=$((patch + 1)) ;;
    esac

    local new_version="$major.$minor.$patch"
    jq --arg v "$new_version" '.version = $v' package.json > tmp.json
    mv tmp.json package.json
    echo "$new_version"
}

NEW_VER=$(bump_version patch)
git commit -am "chore: bump version to $NEW_VER"
git tag "v$NEW_VER"
```

### 4. Dependency Audit

```powershell
Write-Log "Checking for outdated dependencies..." -Level INFO

$outdated = npm outdated --json 2>$null | ConvertFrom-Json
$count = ($outdated.PSObject.Properties | Measure-Object).Count

if ($count -gt 0) {
    Write-Log "$count outdated packages found:" -Level WARN
    $outdated.PSObject.Properties | ForEach-Object {
        $pkg = $_.Name
        $current = $_.Value.current
        $latest = $_.Value.latest
        Write-Host "  $pkg  $current -> $latest"
    }
} else {
    Write-Log "All packages up to date" -Level OK
}
```

### 5. Port Availability Check

```bash
wait_for_port() {
    local host=$1
    local port=$2
    local timeout=${3:-30}
    local elapsed=0

    while ! nc -z "$host" "$port" 2>/dev/null; do
        if (( elapsed >= timeout )); then
            log_error "$host:$port not available after ${timeout}s"
            return 1
        fi
        sleep 1
        elapsed=$((elapsed + 1))
    done
    log_ok "$host:$port is ready"
}

wait_for_port localhost 5432 60    # Wait for PostgreSQL
wait_for_port localhost 6379 30    # Wait for Redis
```

---

## Comparison Quick Reference

| Task | Bash | PowerShell |
|------|------|------------|
| Exit on error | `set -e` | `$ErrorActionPreference = "Stop"` |
| Strict mode | `set -u` | `Set-StrictMode -Version Latest` |
| Current dir | `$(pwd)` | `$PWD` / `Get-Location` |
| Script dir | `$( cd "$(dirname "$0")" && pwd )` | `$PSScriptRoot` |
| Env var | `$VAR` / `${VAR}` | `$env:VAR` |
| String interp | `"Hello $name"` | `"Hello $name"` |
| Null coalesce | `${VAR:-default}` | `$var ?? "default"` (PS 7+) |
| Pipe to file | `cmd > file` | `cmd \| Out-File file` |
| Redirect stderr | `2>&1` | `2>&1` |
| Process subst | `<(cmd)` | N/A (use temp variable) |
| Ternary | `[[ cond ]] && a \|\| b` | `$cond ? $a : $b` (PS 7+) |
