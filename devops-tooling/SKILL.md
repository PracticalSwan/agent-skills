---
name: devops-tooling
version: "2.0"
last_updated: 2026-07-29
tags: [devops, tooling, workflow, quality, planning]
description: "Git operations, shell scripting, CI/CD pipelines, and terminal automation. Use for conventional commits, PowerShell/Bash scripting, configuring GitHub Actions, or automating development tooling workflows."
---
# Devops Tooling

Comprehensive toolkit for Git workflows, shell scripting, and development automation.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## When to Use This Skill

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- Creating conventional commits and managing Git workflows
- Writing Bash, Zsh, or PowerShell automation scripts
- Configuring CI/CD pipelines (GitHub Actions, Azure DevOps)
- Automating development, testing, or deployment tasks
- Troubleshooting Git conflicts and repository hygiene issues

## Part 1: Git Workflows

### Conventional Commits

The conventional commit specification provides an easy-to-extend set of rules for creating an explicit commit history.

#### Commit Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### Types

| Type | Purpose | Example |
|-------|---------|---------|
| `feat` | New feature | `feat(auth): add OAuth2 support` |
| `fix` | Bug fix | `fix(api): resolve null reference` |
| `docs` | Documentation only | `docs(readme): update setup guide` |
| `style` | Formatting/style (no logic) | `style(ui): fix indentation` |
| `refactor` | Refactor production code | `refactor(svc): extract helpers` |
| `perf` | Performance improvement | `perf(db): add index on email` |
| `test` | Adding tests | `test(auth): add unit tests` |
| `build` | Build system or deps | `build(ci): upgrade Node to v20` |
| `ci` | CI configuration changes | `ci(github): add workflow for PRs` |
| `chore` | Maintenance tasks | `chore(deps): update packages` |
| `revert` | Revert previous commit | `revert: feat(login)` |

#### Breaking Changes

Breaking changes must be indicated by `!` after the type/scope, or via `BREAKING CHANGE` in footer:

```bash


feat(api)!: remove deprecated v1 endpoint


feat(api): remove deprecated v1 endpoint

BREAKING CHANGE: v1 endpoints are no longer supported. Use v2.
```

#### Good Examples

```bash


feat(auth): implement JWT refresh tokens


fix(ui): resolve mobile navigation overlap issue


docs(api): add authentication examples


refactor(user): extract validation logic to separate module


perf(images): implement lazy loading


feat(core)!: change data structure from array to object
```

### Git Operations

#### Branch Management

```bash


git checkout -b feature/PROJ-123/user-auth


git checkout develop


git branch -d feature/PROJ-123/user-auth


git push origin --delete feature/PROJ-123/user-auth


git branch -m new-name


git branch -a
```

#### Commit Workflow

```bash


git add .


git add file1.ts file2.ts


git add -i


git commit -m "feat(auth): add OAuth2 support"


git commit --amend


git log --oneline --graph --all


git show <commit-hash>
```

#### Merge & Rebase

```bash


git merge feature/new-feature


git rebase develop


git rebase -i HEAD~3


git rebase --abort
git merge --abort


git rebase --continue
git merge --continue
```

#### Handling Conflicts

```bash


git status


vim conflicting-file.ts


git add conflicting-file.ts


git commit  # for merges
git rebase --continue  # for rebases
```

#### Stashing

```bash


git stash push -m "Work in progress"


git stash pop


git stash apply stash@{2}


git stash list


git stash drop stash@{2}


git stash clear
```

#### Tagging

```bash


git tag -a v1.0.0 -m "Release v1.0.0"


git tag v1.0.0


git tag


git push origin --tags


git push origin v1.0.0


git tag -d v1.0.0


git push origin --delete v1.0.0
```

#### Git Diff

```bash


git diff


git diff --staged


git diff src/app.ts


git diff HEAD~2 HEAD


git log --oneline v1.0.0..v2.0.0


git diff --stat
```

#### Git Configuration

```bash


git config --global user.name "Your Name"
git config --global user.email "your@email.com"


git config --global init.defaultBranch main


git config --global commit.gpgsign true


git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status


git config --unset user.name


git config --list
```

---

## Part 2: Shell Scripting (bash/zsh)

### General Principles

- Generate clean, simple, and concise code
- Ensure scripts are easily readable and understandable
- Add comments where needed for understanding
- Generate concise echo outputs for execution status
- Avoid unnecessary output and excessive logging

### Error Handling & Safety

#### Enable Strict Mode

Always enable strict mode at the top of scripts:

```bash
#!/bin/bash
set -euo pipefail
```

- `-e`: Exit on first error
- `-u`: Treat unset variables as errors
- `-o pipefail`: Surface pipeline failures

#### Cleanup with Traps

```bash
cleanup() {
    # Remove temporary files
    if [[ -n "${TEMP_DIR:-}" && -d "$TEMP_DIR" ]]; then
        rm -rf "$TEMP_DIR"
    fi

    # Close connections
    if [[ -n "${CONNECTION:-}" ]]; then
        echo "Closing connection..."
        # connection close logic
    fi
}

trap cleanup EXIT


trap 'echo "Interrupted"; cleanup; exit 1' INT TERM
```

#### Validate Requirements

```bash
validate_requirements() {
    local errors=0

    # Check required variables
    if [[ -z "${RESOURCE_GROUP:-}" ]]; then
        echo "Error: RESOURCE_GROUP environment variable not set" >&2
        ((errors++))
    fi

    # Check required commands
    for cmd in curl jq az; do
        if ! command -v "$cmd" &> /dev/null; then
            echo "Error: $cmd is not installed" >&2
            ((errors++))
        fi
    done

    # Return appropriate exit code
    return $errors
}


if ! validate_requirements; then
    exit 1
fi
```

### Working with Variables

```bash


echo "Config: ${CONFIG_FILE:-./config.default.yaml}"


name="World"
echo "Hello, ${name}!"


apps=("app1" "app2" "app3")
for app in "${apps[@]}"; do
    echo "Processing: $app"
done


declare -A config
config[host]="localhost"
config[port]="8080"
echo "Connecting to ${config[host]}:${config[port]}"
```

### Control Flow

```bash


if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Linux detected"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS detected"
else
    echo "Unknown OS"
fi


case "$1" in
    start)
        echo "Starting service..."
        ;;
    stop)
        echo "Stopping service..."
        ;;
    *)
        echo "Usage: $0 {start|stop}"
        exit 1
        ;;
esac


for i in {1..5}; do
    echo "Iteration $i"
done


timeout=30
elapsed=0
while [[ $elapsed -lt $timeout ]]; do
    if check_ready; then
        echo "Service ready"
        break
    fi
    sleep 1
    ((elapsed++))
done
```

### Parsing JSON with jq

```bash


result=$(curl -s "https://api.example.com/data")
name=$(echo "$result" | jq -r '.name')
count=$(echo "$result" | jq '.items | length')
first_item=$(echo "$result" | jq -r '.items[0]')


active_users=$(echo "$result" | jq '.users[] | select(.status == "active")')


read -r first_name last_name email <<<$(echo "$result" | jq -r '"\(.firstName) \(.lastName) \(.email)"')


echo "$result" | jq '.count += 1' > updated.json


jq -n \
  --arg name "John" \
  --arg age "30" \
  '{name: $name, age: ($age | tonumber)}'
```

### Parsing Arguments

```bash
#!/bin/bash


verbose=0
output_file="output.txt"
config="./config.yaml"


while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            verbose=1
            shift
            ;;
        -o|--output)
            output_file="$2"
            shift 2
            ;;
        -c|--config)
            config="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

echo "Config: $config"
echo "Output: $output_file"
echo "Verbose: $verbose"
```

### File Operations

```bash


if [[ -f "$FILE_PATH" ]]; then
    echo "File exists"
fi


if [[ ! -d "$DIR_PATH" ]]; then
    mkdir -p "$DIR_PATH"
fi


mkdir -p ./dir1/dir2


cp -r source_dir/ dest_dir/


rm -f file.txt          # Force delete file
rm -rf directory/       # Recursive delete directory


find . -name "*.py"           # All Python files
find . -type f -name "*.js"   # All JS files (regular files only)
find . -mtime -7              # Modified in last 7 days


temp_file=$(mktemp)
echo "data" > "$temp_file"


rm -f "$temp_file"


temp_dir=$(mktemp -d)


rm -rf "$temp_dir"
```

### Process Management

```bash


if pgrep -x "nginx" > /dev/null; then
    echo "Nginx is running"
else
    echo "Nginx is not running"
fi


while pgrep -x "script-name" > /dev/null; do
    sleep 1
done


timeout 30s ./long-running-script.sh || echo "Timed out after 30s"


./script.sh &
job_pid=$!


trap "kill $job_pid 2>/dev/null" EXIT
```

### Logging

```bash
#!/bin/bash


LOG_INFO() {
    echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') $*"
}

LOG_WARN() {
    echo "[WARN] $(date '+%Y-%m-%d %H:%M:%S') $*" >&2
}

LOG_ERROR() {
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') $*" >&2
}

LOG_DEBUG() {
    if [[ "${DEBUG:-}" == "1" ]]; then
        echo "[DEBUG] $(date '+%Y-%m-%d %H:%M:%S') $*"
    fi
}


LOG_INFO "Starting deployment"
LOG_WARN "This is a warning"
LOG_ERROR "Deployment failed"
LOG_DEBUG "Detailed debugging info"
```

---

## Part 3: PowerShell Scripting

### General Practices

- Use proper cmdlet names instead of aliases (e.g., `Get-ChildItem`, not `dir`)
- Quote paths with spaces: `"C:\Path With Spaces\file.txt"`
- Use `ShouldProcess` for destructive operations
- Implement proper error handling with try-catch
- Parameterize scripts for reusability

### Error Handling

```powershell


Set-StrictMode -Version Latest


$ErrorActionPreference = "Stop"


try {
    $result = Invoke-RestMethod -Uri "https://api.example.com/data" -Method Get
}
catch [System.Net.WebException] {
    Write-Error "Network error occurred: $($_.Exception.Message)"
    exit 1
}
catch {
    Write-Error "Unexpected error: $($_.Exception.Message)"
    exit 1
}
finally {
    # Cleanup code always runs
    Write-Output "Execution completed"
}


trap {
    Write-Error "Script failed: $_"
    # Cleanup code
    Remove-Variable -Name tempVar -ErrorAction SilentlyContinue
    exit 1
}
```

### Parameter Handling

```powershell
param(
    [Parameter(Mandatory=$true)]
    [string]$Name,

    [Parameter(Mandatory=$false)]
    [string]$Path = ".",

    [Parameter(Mandatory=$false)]
    [switch]$Verbose,

    [ValidateSet("dev", "staging", "prod")]
    [string]$Environment = "dev"
)

Write-Output "Name: $Name"
Write-Output "Path: $Path"
Write-Output "Environment: $Environment"
Write-Output "Verbose: $Verbose"
```

### Working with Objects

```powershell


$user = [PSCustomObject]@{
    Name = "John"
    Age = 30
    Email = "john@example.com",
    Address = "123 Main St"
}


Write-Output $user.Name


$user | Add-Member -MemberType NoteProperty -Name "City" -Value "Anytown"


$users | Where-Object { $_.Age -gt 25 }


$users | Select-Object Name, Email


$users | Sort-Object Name


$users | Group-Object City
```

### Working with JSON

```powershell


$json = '{"name": "John", "age": 30}'
$obj = $json | ConvertFrom-Json

Write-Output $obj.name


$data = @{ name = "John"; age = 30 }
$json = $data | ConvertTo-Json -Depth 10
Write-Output $json


$config = Get-Content "config.json" | ConvertFrom-Json


$config | ConvertTo-Json -Depth 10 | Set-Content "config.json"
```

### Working with Arrays and Hashtables

```powershell


$files = @("file1.txt", "file2.txt", "file3.txt")


$files += "file4.txt"


$filtered = $files | Where-Object { $_ -like "*.txt" }


$config = @{
    host = "localhost"
    port = 8080
    tls = $true
}


Write-Output $config.host


$key = "port"
Write-Output $config[$key]


foreach ($item in $config.GetEnumerator()) {
    Write-Output "$($item.Name) = $($item.Value)"
}
```

### File Operations

```powershell


if (Test-Path "C:\path\to\file.txt") {
    Write-Output "File exists"
}


New-Item -ItemType Directory -Path "C:\new\dir" -Force


Remove-Item "C:\path\to\file.txt" -Force
Remove-Item "C:\path\to\directory" -Recurse -Force


Copy-Item "source.txt" "destination.txt" -Force
Copy-Item "dir\" "backup\" -Recurse


Move-Item "old_name.txt" "new_name.txt"


$content = Get-Content "file.txt"
$content = Get-Content "file.txt" -Raw  # As single string


$content | Set-Content "file.txt"


"more content" | Add-Content "file.txt"
```

### String Operations

```powershell


$name = "John"
Write-Output "Hello, $name!"


Write-Output ("Hello, {0}! Your score is {1:N2}" -f $name, 95.5)


$string = "  Hello World  "


$trimmed = $string.Trim()


$replaced = $string.Replace("World", "PowerShell")


if ($string -like "*World*") {
    Write-Output "Contains 'World'"
}


if ($string -match "^Hello") {
    Write-Output "Starts with 'Hello'"
}


$parts = "a,b,c".Split(",")
```

---

## Part 4: CI/CD Configuration

### GitHub Actions

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  workflow_dispatch: # Allow manual trigger

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16.x, 18.x, 20.x]

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run tests
        run: npm test

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build
          path: dist/

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Download artifacts
        uses: actions/download-artifact@v3
        with:
          name: build

      - name: Deploy to Azure
        run: az webapp up --name myapp --resource-group myrg
```

### Azure Pipelines

```yaml
trigger:
- main
- develop

pool:
  vmImage: 'ubuntu-latest'

variables:
  buildConfiguration: 'Release'
  packageFolder: '$(build.artifactStagingDirectory)/package'

stages:
- stage: Build
  displayName: 'Build stage'
  jobs:
  - job: Build
    displayName: 'Build job'
    steps:
    - task: NodeTool@0
      inputs:
        versionSpec: '18.x'
      displayName: 'Install Node.js'

    - script: |
        npm ci
      displayName: 'Install dependencies'

    - script: |
        npm run build
      displayName: 'Build application'

    - task: ArchiveFiles@2
      inputs:
        rootFolderOrFile: 'dist'
        includeRootFolder: false
        archiveType: 'zip'
        archiveFile: $(Build.ArtifactStagingDirectory)/$(Build.BuildId).zip
      displayName: 'Archive build artifacts'

    - publish: $(Build.ArtifactStagingDirectory)/$(Build.BuildId).zip
      artifact: drop

- stage: Deploy
  displayName: 'Deploy stage'
  dependsOn: Build
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
  jobs:
  - deployment: Deploy
    displayName: 'Deploy job'
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureWebApp@1
            inputs:
              azureSubscription: 'your_subscription_id'
              appName: 'your_webapp_name'
              package: $(Pipeline.Workspace)/drop/$(Build.BuildId).zip
```

---

## DevOps Best Practices

### Git
- [ ] Use conventional commits
- [ ] Keep commits small and focused
- [ ] Write clear, descriptive messages
- [ ] Keep feature branches short-lived
- [ ] Rebase feature branches before merging
- [ ] Sign commits for security-critical projects

### Shell Scripting
- [ ] Always use strict mode (`set -euo pipefail`)
- [ ] Quote variables properly
- [ ] Handle errors gracefully with traps
- [ ] Validate inputs and parameters
- [ ] Use functions for reusability
- [ ] Add proper error messages to stderr

### PowerShell
- [ ] Use strict mode for security
- [ ] Use proper cmdlet names (no aliases)
- [ ] Implement error handling with try-catch
- [ ] Test scripts thoroughly
- [ ] Use parameter validation
- [ ] Handle pipeline errors properly

### CI/CD
- [ ] Use secure variable management for secrets
- [ ] Cache dependencies to speed up builds
- [ ] Run tests on multiple environments
- [ ] Use matrix builds for different configurations
- [ ] Implement proper artifact management
- [ ] Add deployment gates and approvals
- [ ] Provide clear build status

---

## Anti-Patterns

- Starting work before the plan or gate is clear: Execution drifts when success criteria are implied instead of explicit.
- Treating verification as optional cleanup: The last mile is where regressions and missing updates are usually hiding.
- Mixing planning, implementation, and release work in one jump: You lose the causal chain that explains why a change is safe.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Devops Tooling workflow starts from explicit success criteria, constraints, and stop conditions.
2. Pass/fail: Required evidence is collected before any completion, approval, or readiness claim.
3. Pass/fail: The next action follows the documented gate order without skipping review or verification steps.
4. Pressure-test scenario: Apply the workflow under time pressure with one failing check and one tempting shortcut.
5. Success metric: Zero rationalizations; blocked, failed, or unverified work is reported as such.

## References & Resources

### Documentation
- [CI/CD Patterns](./references/ci-cd-patterns.md) — GitHub Actions patterns, caching, security scanning, and deployment strategies
- [Shell Scripting Patterns](./references/shell-scripting-patterns.md) — PowerShell and Bash patterns side-by-side for automation

### Scripts
- [Setup Git Hooks](./scripts/setup-git-hooks.ps1) — PowerShell script to install pre-commit, commit-msg, and pre-push hooks

### Examples
- [GitHub Actions Templates](./examples/github-actions-templates.md) — 8 production-ready workflow templates for Node.js, Python, Docker, Terraform


---

<!-- MCP:START -->

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/devops-tooling` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: GitHub MCP

- Fallback prompt: "Use the Devops Tooling skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- Use standard local tools such as `git`, `gh`, CI logs, and shell automation scripts for repository and pipeline work.
- Prefer the bundled repo scripts or direct YAML edits when the MCP host does not expose GitHub operations.

<!-- MCP:END -->

## Related Skills

- [development-workflow](../development-workflow/SKILL.md): Use it when the workflow also needs planning, quality gates, and delivery tracking.
- [code-quality](../code-quality/SKILL.md): Use it when the workflow also needs two-stage review (spec compliance first, then code quality), maintainability, and refactoring guidance.
- [systematic-debugging](../systematic-debugging/SKILL.md): Use it when the workflow also needs root-cause debugging before proposing fixes.
- [test-driven-development](../test-driven-development/SKILL.md): Use it when the workflow also needs test-first implementation and regression safety.
