<#
.SYNOPSIS
    Sets up Git hooks for a project (pre-commit, commit-msg, pre-push).

.DESCRIPTION
    Creates Git hooks in the .git/hooks/ directory:
    - pre-commit: lint staged files, check for debug statements
    - commit-msg: validate conventional commit format
    - pre-push: run tests before pushing
    
    Hooks are shell scripts (#!/bin/sh) for cross-platform compatibility
    (Git executes hooks via sh on all platforms, including Windows with Git Bash).

.PARAMETER ProjectDir
    Root directory of the Git repository. Defaults to current directory.

.PARAMETER SkipTests
    If set, the pre-push hook will be skipped.

.PARAMETER Force
    Overwrite existing hooks without prompting.

.EXAMPLE
    .\setup-git-hooks.ps1 -ProjectDir "C:\Projects\my-app"

.EXAMPLE
    .\setup-git-hooks.ps1 -Force
#>

param(
    [Parameter(Mandatory = $false)]
    [string]$ProjectDir = ".",

    [switch]$SkipTests,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$ProjectDir = Resolve-Path $ProjectDir
$hooksDir = Join-Path $ProjectDir ".git" "hooks"

if (-not (Test-Path (Join-Path $ProjectDir ".git"))) {
    Write-Error "Not a git repository: $ProjectDir"
    exit 1
}

if (-not (Test-Path $hooksDir)) {
    New-Item -ItemType Directory -Path $hooksDir -Force | Out-Null
}

function Install-Hook {
    param(
        [string]$Name,
        [string]$Content
    )

    $hookPath = Join-Path $hooksDir $Name

    if ((Test-Path $hookPath) -and -not $Force) {
        Write-Warning "Hook '$Name' already exists. Use -Force to overwrite. Skipping."
        return
    }

    $Content = $Content -replace "`r`n", "`n"
    [System.IO.File]::WriteAllText($hookPath, $Content)

    Write-Host "  Installed: $Name" -ForegroundColor Green
}

# ── pre-commit hook ──────────────────────────────────────────────────────────

$preCommitHook = @'
#!/bin/sh
# pre-commit hook: lint staged files, check for debug statements

RED='\033[0;31m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "${GREEN}[pre-commit]${NC} Running checks on staged files..."

STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$STAGED_FILES" ]; then
    echo "${GREEN}[pre-commit]${NC} No staged files to check."
    exit 0
fi

ERRORS=0

# ── Check for debug statements ──────────────────────────────────────────────
DEBUG_PATTERNS='console\.log\|debugger\|binding\.pry\|import pdb\|breakpoint()'

DEBUG_FILES=$(echo "$STAGED_FILES" | xargs grep -l "$DEBUG_PATTERNS" 2>/dev/null || true)

if [ -n "$DEBUG_FILES" ]; then
    echo "${YELLOW}[pre-commit]${NC} Debug statements found in:"
    for f in $DEBUG_FILES; do
        echo "  ${RED}$f${NC}"
        git diff --cached "$f" | grep -n "$DEBUG_PATTERNS" | head -5
    done
    echo "${YELLOW}[pre-commit]${NC} Remove debug statements or use 'git commit --no-verify' to bypass."
    ERRORS=1
fi

# ── Check for large files ───────────────────────────────────────────────────
MAX_FILE_SIZE=1048576  # 1 MB

for file in $STAGED_FILES; do
    if [ -f "$file" ]; then
        FILE_SIZE=$(wc -c < "$file" 2>/dev/null || echo "0")
        if [ "$FILE_SIZE" -gt "$MAX_FILE_SIZE" ]; then
            echo "${RED}[pre-commit]${NC} Large file detected: $file ($(( FILE_SIZE / 1024 ))KB)"
            ERRORS=1
        fi
    fi
done

# ── Check for merge conflict markers ────────────────────────────────────────
CONFLICT_FILES=$(echo "$STAGED_FILES" | xargs grep -l '<<<<<<<\|>>>>>>>\|=======' 2>/dev/null || true)

if [ -n "$CONFLICT_FILES" ]; then
    echo "${RED}[pre-commit]${NC} Merge conflict markers found in:"
    for f in $CONFLICT_FILES; do
        echo "  $f"
    done
    ERRORS=1
fi

# ── Run linter if available ──────────────────────────────────────────────────
JS_FILES=$(echo "$STAGED_FILES" | grep -E '\.(js|jsx|ts|tsx)$' || true)

if [ -n "$JS_FILES" ]; then
    if command -v npx >/dev/null 2>&1 && [ -f "node_modules/.bin/eslint" ]; then
        echo "${GREEN}[pre-commit]${NC} Running ESLint on staged JS/TS files..."
        echo "$JS_FILES" | xargs npx eslint --quiet
        if [ $? -ne 0 ]; then
            ERRORS=1
        fi
    fi
fi

PY_FILES=$(echo "$STAGED_FILES" | grep -E '\.py$' || true)

if [ -n "$PY_FILES" ]; then
    if command -v ruff >/dev/null 2>&1; then
        echo "${GREEN}[pre-commit]${NC} Running ruff on staged Python files..."
        echo "$PY_FILES" | xargs ruff check
        if [ $? -ne 0 ]; then
            ERRORS=1
        fi
    fi
fi

if [ $ERRORS -ne 0 ]; then
    echo "${RED}[pre-commit]${NC} Commit blocked. Fix the issues above."
    exit 1
fi

echo "${GREEN}[pre-commit]${NC} All checks passed."
exit 0
'@

# ── commit-msg hook ──────────────────────────────────────────────────────────

$commitMsgHook = @'
#!/bin/sh
# commit-msg hook: validate conventional commit format
#
# Format: <type>(<scope>): <subject>
# Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

COMMIT_MSG_FILE=$1
COMMIT_MSG=$(head -1 "$COMMIT_MSG_FILE")

# Allow merge commits
if echo "$COMMIT_MSG" | grep -qE '^Merge '; then
    exit 0
fi

# Allow revert commits
if echo "$COMMIT_MSG" | grep -qE '^Revert '; then
    exit 0
fi

# Validate conventional commit format
PATTERN='^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-zA-Z0-9_-]+\))?(!)?: .{1,100}$'

if ! echo "$COMMIT_MSG" | grep -qE "$PATTERN"; then
    echo ""
    echo "${RED}[commit-msg]${NC} Invalid commit message format."
    echo ""
    echo "  Your message:  $COMMIT_MSG"
    echo ""
    echo "  Expected format: <type>(<scope>): <subject>"
    echo ""
    echo "  Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert"
    echo ""
    echo "  Examples:"
    echo "    feat(auth): add OAuth login flow"
    echo "    fix: resolve null pointer in user service"
    echo "    docs(readme): update installation instructions"
    echo "    feat!: redesign API response format"
    echo ""
    echo "  Rules:"
    echo "    - Type is required"
    echo "    - Scope is optional (lowercase, alphanumeric, hyphens, underscores)"
    echo "    - Subject is required (max 100 chars, no period at end)"
    echo "    - Add ! before : for breaking changes"
    echo ""
    exit 1
fi

# Check subject doesn't end with a period
if echo "$COMMIT_MSG" | grep -qE '\.$'; then
    echo "${RED}[commit-msg]${NC} Subject should not end with a period."
    exit 1
fi

echo "${GREEN}[commit-msg]${NC} Commit message is valid."
exit 0
'@

# ── pre-push hook ────────────────────────────────────────────────────────────

$prePushHook = @'
#!/bin/sh
# pre-push hook: run tests before pushing

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo "${GREEN}[pre-push]${NC} Running tests before push..."

# Detect project type and run tests
if [ -f "package.json" ]; then
    if command -v npm >/dev/null 2>&1; then
        # Check if test script exists
        TEST_SCRIPT=$(node -e "const p=require('./package.json'); console.log(p.scripts && p.scripts.test ? 'yes' : 'no')" 2>/dev/null)
        if [ "$TEST_SCRIPT" = "yes" ]; then
            echo "${GREEN}[pre-push]${NC} Running npm test..."
            npm test --silent
            if [ $? -ne 0 ]; then
                echo "${RED}[pre-push]${NC} Tests failed. Push blocked."
                echo "${YELLOW}[pre-push]${NC} Use 'git push --no-verify' to bypass."
                exit 1
            fi
        else
            echo "${YELLOW}[pre-push]${NC} No test script found in package.json. Skipping."
        fi
    fi
elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
    if command -v pytest >/dev/null 2>&1; then
        echo "${GREEN}[pre-push]${NC} Running pytest..."
        pytest --tb=short -q
        if [ $? -ne 0 ]; then
            echo "${RED}[pre-push]${NC} Tests failed. Push blocked."
            exit 1
        fi
    elif command -v python >/dev/null 2>&1; then
        echo "${GREEN}[pre-push]${NC} Running python -m pytest..."
        python -m pytest --tb=short -q
        if [ $? -ne 0 ]; then
            echo "${RED}[pre-push]${NC} Tests failed. Push blocked."
            exit 1
        fi
    fi
elif [ -f "go.mod" ]; then
    echo "${GREEN}[pre-push]${NC} Running go test..."
    go test ./...
    if [ $? -ne 0 ]; then
        echo "${RED}[pre-push]${NC} Tests failed. Push blocked."
        exit 1
    fi
fi

echo "${GREEN}[pre-push]${NC} All tests passed."
exit 0
'@

# ── Install hooks ────────────────────────────────────────────────────────────

Write-Host ""
Write-Host "Setting up Git hooks in: $ProjectDir" -ForegroundColor Cyan
Write-Host ""

Install-Hook -Name "pre-commit" -Content $preCommitHook
Install-Hook -Name "commit-msg" -Content $commitMsgHook

if (-not $SkipTests) {
    Install-Hook -Name "pre-push" -Content $prePushHook
} else {
    Write-Host "  Skipped: pre-push (tests disabled)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Git hooks installed successfully." -ForegroundColor Green
Write-Host ""
Write-Host "Hooks will run automatically. To bypass:" -ForegroundColor Yellow
Write-Host "  git commit --no-verify     # Skip pre-commit + commit-msg"
Write-Host "  git push --no-verify       # Skip pre-push"
Write-Host ""
