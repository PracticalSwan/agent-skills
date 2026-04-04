---
name: devops-tooling
description: Git operations, shell scripting, CI/CD pipelines, and terminal automation. Use for conventional commits, PowerShell/Bash scripting, configuring GitHub Actions, or automating development tooling workflows.
license: Complete terms in LICENSE.txt
---
## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror


Comprehensive toolkit for Git workflows, shell scripting, and development automation.

## When to Use This Skill

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


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

feat(api)!: remove deprecated v1 endpoint



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

feat(api): remove deprecated v1 endpoint

BREAKING CHANGE: v1 endpoints are no longer supported. Use v2.
```

#### Good Examples

```bash


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

feat(auth): implement JWT refresh tokens



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

fix(ui): resolve mobile navigation overlap issue



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

docs(api): add authentication examples



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

refactor(user): extract validation logic to separate module



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

perf(images): implement lazy loading



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

feat(core)!: change data structure from array to object
```

### Git Operations

#### Branch Management

```bash


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git checkout -b feature/PROJ-123/user-auth



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git checkout develop



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git branch -d feature/PROJ-123/user-auth



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git push origin --delete feature/PROJ-123/user-auth



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git branch -m new-name



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git branch -a
```

#### Commit Workflow

```bash


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git add .



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git add file1.ts file2.ts



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git add -i



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git commit -m "feat(auth): add OAuth2 support"



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git commit --amend



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git log --oneline --graph --all



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git show <commit-hash>
```

#### Merge & Rebase

```bash


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git merge feature/new-feature



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git rebase develop



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git rebase -i HEAD~3



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git rebase --abort
git merge --abort



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git rebase --continue
git merge --continue
```

#### Handling Conflicts

```bash


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git status



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

vim conflicting-file.ts



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror




## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git add conflicting-file.ts



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git commit  # for merges
git rebase --continue  # for rebases
```

#### Stashing

```bash


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git stash push -m "Work in progress"



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git stash pop



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git stash apply stash@{2}



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git stash list



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git stash drop stash@{2}



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git stash clear
```

#### Tagging

```bash


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git tag -a v1.0.0 -m "Release v1.0.0"



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git tag v1.0.0



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git tag



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git push origin --tags



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git push origin v1.0.0



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git tag -d v1.0.0



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git push origin --delete v1.0.0
```

#### Git Diff

```bash


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git diff



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git diff --staged



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git diff src/app.ts



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git diff HEAD~2 HEAD



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git log --oneline v1.0.0..v2.0.0



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git diff --stat
```

#### Git Configuration

```bash


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git config --global user.name "Your Name"
git config --global user.email "your@email.com"



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git config --global init.defaultBranch main



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git config --global commit.gpgsign true



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

git config --unset user.name



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

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



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

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



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

if ! validate_requirements; then
    exit 1
fi
```

### Working with Variables

```bash


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

echo "Config: ${CONFIG_FILE:-./config.default.yaml}"



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

name="World"
echo "Hello, ${name}!"



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

apps=("app1" "app2" "app3")
for app in "${apps[@]}"; do
    echo "Processing: $app"
done



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

declare -A config
config[host]="localhost"
config[port]="8080"
echo "Connecting to ${config[host]}:${config[port]}"
```

### Control Flow

```bash


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Linux detected"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS detected"
else
    echo "Unknown OS"
fi



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

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



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

for i in {1..5}; do
    echo "Iteration $i"
done



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

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


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

result=$(curl -s "https://api.example.com/data")
name=$(echo "$result" | jq -r '.name')
count=$(echo "$result" | jq '.items | length')
first_item=$(echo "$result" | jq -r '.items[0]')



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

active_users=$(echo "$result" | jq '.users[] | select(.status == "active")')



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

read -r first_name last_name email <<<$(echo "$result" | jq -r '"\(.firstName) \(.lastName) \(.email)"')



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

echo "$result" | jq '.count += 1' > updated.json



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

jq -n \
  --arg name "John" \
  --arg age "30" \
  '{name: $name, age: ($age | tonumber)}'
```

### Parsing Arguments

```bash
#!/bin/bash



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

verbose=0
output_file="output.txt"
config="./config.yaml"



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

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


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

if [[ -f "$FILE_PATH" ]]; then
    echo "File exists"
fi



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

if [[ ! -d "$DIR_PATH" ]]; then
    mkdir -p "$DIR_PATH"
fi



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

mkdir -p ./dir1/dir2



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

cp -r source_dir/ dest_dir/



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

rm -f file.txt          # Force delete file
rm -rf directory/       # Recursive delete directory



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

find . -name "*.py"           # All Python files
find . -type f -name "*.js"   # All JS files (regular files only)
find . -mtime -7              # Modified in last 7 days



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

temp_file=$(mktemp)
echo "data" > "$temp_file"


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

rm -f "$temp_file"



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

temp_dir=$(mktemp -d)


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

rm -rf "$temp_dir"
```

### Process Management

```bash


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

if pgrep -x "nginx" > /dev/null; then
    echo "Nginx is running"
else
    echo "Nginx is not running"
fi



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

while pgrep -x "script-name" > /dev/null; do
    sleep 1
done



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

timeout 30s ./long-running-script.sh || echo "Timed out after 30s"



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

./script.sh &
job_pid=$!



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

trap "kill $job_pid 2>/dev/null" EXIT
```

### Logging

```bash
#!/bin/bash



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

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



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

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


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

Set-StrictMode -Version Latest



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$ErrorActionPreference = "Stop"



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

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



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

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


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$user = [PSCustomObject]@{
    Name = "John"
    Age = 30
    Email = "john@example.com",
    Address = "123 Main St"
}



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

Write-Output $user.Name



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$user | Add-Member -MemberType NoteProperty -Name "City" -Value "Anytown"



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$users | Where-Object { $_.Age -gt 25 }



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$users | Select-Object Name, Email



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$users | Sort-Object Name



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$users | Group-Object City
```

### Working with JSON

```powershell


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$json = '{"name": "John", "age": 30}'
$obj = $json | ConvertFrom-Json

Write-Output $obj.name



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$data = @{ name = "John"; age = 30 }
$json = $data | ConvertTo-Json -Depth 10
Write-Output $json



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$config = Get-Content "config.json" | ConvertFrom-Json



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$config | ConvertTo-Json -Depth 10 | Set-Content "config.json"
```

### Working with Arrays and Hashtables

```powershell


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$files = @("file1.txt", "file2.txt", "file3.txt")



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$files += "file4.txt"



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$filtered = $files | Where-Object { $_ -like "*.txt" }



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$config = @{
    host = "localhost"
    port = 8080
    tls = $true
}



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

Write-Output $config.host



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$key = "port"
Write-Output $config[$key]



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

foreach ($item in $config.GetEnumerator()) {
    Write-Output "$($item.Name) = $($item.Value)"
}
```

### File Operations

```powershell


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

if (Test-Path "C:\path\to\file.txt") {
    Write-Output "File exists"
}



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

New-Item -ItemType Directory -Path "C:\new\dir" -Force



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

Remove-Item "C:\path\to\file.txt" -Force
Remove-Item "C:\path\to\directory" -Recurse -Force



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

Copy-Item "source.txt" "destination.txt" -Force
Copy-Item "dir\" "backup\" -Recurse



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

Move-Item "old_name.txt" "new_name.txt"



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$content = Get-Content "file.txt"
$content = Get-Content "file.txt" -Raw  # As single string



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$content | Set-Content "file.txt"



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

"more content" | Add-Content "file.txt"
```

### String Operations

```powershell


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$name = "John"
Write-Output "Hello, $name!"



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

Write-Output ("Hello, {0}! Your score is {1:N2}" -f $name, 95.5)



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$string = "  Hello World  "



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$trimmed = $string.Trim()



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

$replaced = $string.Replace("World", "PowerShell")



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

if ($string -like "*World*") {
    Write-Output "Contains 'World'"
}



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

if ($string -match "^Hello") {
    Write-Output "Starts with 'Hello'"
}



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

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

## References & Resources

### Documentation
- [CI/CD Patterns](./references/ci-cd-patterns.md) — GitHub Actions patterns, caching, security scanning, and deployment strategies
- [Shell Scripting Patterns](./references/shell-scripting-patterns.md) — PowerShell and Bash patterns side-by-side for automation

### Scripts
- [Setup Git Hooks](./scripts/setup-git-hooks.ps1) — PowerShell script to install pre-commit, commit-msg, and pre-push hooks

### Examples
- [GitHub Actions Templates](./examples/github-actions-templates.md) — 8 production-ready workflow templates for Node.js, Python, Docker, Terraform


---

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:devops-tooling` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py devops-tooling` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP servers for this skill:
- `GitHub MCP` (optional)

If MCP is unavailable in the current host:
- Use standard local tools such as `git`, `gh`, CI logs, and shell automation scripts for repository and pipeline work.
- Prefer the bundled repo scripts or direct YAML edits when the MCP host does not expose GitHub operations.

<!-- MCP:END -->

## Related Skills
| Skill | Relationship |
|-------|-------------|
| [development-workflow](../development-workflow/SKILL.md) | Project lifecycle that DevOps tooling supports |
| [azure-integrations](../azure-integrations/SKILL.md) | Azure-specific CI/CD and deployment pipelines |
| [documentation-automation](../documentation-automation/SKILL.md) | Pre-commit hooks and automated doc generation |

---
