# GitHub Actions Workflow Templates

> Ready-to-use, production-grade workflow templates. Copy into `.github/workflows/` and customize for your project.

---

## 1. Node.js CI

```yaml
# .github/workflows/node-ci.yml
name: Node.js CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint

  test:
    name: Test (Node ${{ matrix.node-version }})
    runs-on: ubuntu-latest
    timeout-minutes: 15
    strategy:
      fail-fast: false
      matrix:
        node-version: [18, 20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      - run: npm ci
      - run: npm test -- --coverage
      - name: Upload coverage
        if: matrix.node-version == 20
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/
          retention-days: 5

  build:
    name: Build
    needs: [lint, test]
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: dist/
          retention-days: 5
```

---

## 2. Python CI

```yaml
# .github/workflows/python-ci.yml
name: Python CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'
      - run: pip install ruff mypy
      - run: ruff check .
      - run: ruff format --check .

  test:
    name: Test (Python ${{ matrix.python-version }})
    runs-on: ubuntu-latest
    timeout-minutes: 15
    strategy:
      fail-fast: false
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      - run: pip install -r requirements.txt
      - run: pip install -r requirements-dev.txt
      - run: pytest --tb=short --cov=src --cov-report=xml
      - name: Upload coverage
        if: matrix.python-version == '3.12'
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage.xml
          retention-days: 5

  type-check:
    name: Type Check
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'
      - run: pip install -r requirements.txt
      - run: pip install mypy
      - run: mypy src/ --ignore-missing-imports
```

---

## 3. Docker Build + Push

```yaml
# .github/workflows/docker.yml
name: Docker Build & Push

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

permissions:
  contents: read
  packages: write

jobs:
  build:
    name: Build & Push
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix=

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          platforms: linux/amd64,linux/arm64
```

---

## 4. Terraform Plan + Apply

```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  push:
    branches: [main]
    paths: ['infra/**']
  pull_request:
    branches: [main]
    paths: ['infra/**']

permissions:
  contents: read
  pull-requests: write

env:
  TF_VERSION: '1.7'
  WORKING_DIR: infra

jobs:
  plan:
    name: Terraform Plan
    runs-on: ubuntu-latest
    timeout-minutes: 15
    defaults:
      run:
        working-directory: ${{ env.WORKING_DIR }}
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Terraform Init
        run: terraform init -backend-config=backend.hcl

      - name: Terraform Format Check
        run: terraform fmt -check -recursive

      - name: Terraform Validate
        run: terraform validate

      - name: Terraform Plan
        id: plan
        run: terraform plan -no-color -out=tfplan
        env:
          ARM_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
          ARM_CLIENT_SECRET: ${{ secrets.AZURE_CLIENT_SECRET }}
          ARM_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          ARM_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}

      - name: Comment PR with plan
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const plan = `${{ steps.plan.outputs.stdout }}`;
            const truncated = plan.length > 60000
              ? plan.substring(0, 60000) + '\n\n...truncated'
              : plan;
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: `### Terraform Plan\n\`\`\`\n${truncated}\n\`\`\``
            });

      - uses: actions/upload-artifact@v4
        with:
          name: tfplan
          path: ${{ env.WORKING_DIR }}/tfplan

  apply:
    name: Terraform Apply
    needs: plan
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    timeout-minutes: 30
    environment: production
    defaults:
      run:
        working-directory: ${{ env.WORKING_DIR }}
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Terraform Init
        run: terraform init -backend-config=backend.hcl

      - uses: actions/download-artifact@v4
        with:
          name: tfplan
          path: ${{ env.WORKING_DIR }}

      - name: Terraform Apply
        run: terraform apply -auto-approve tfplan
        env:
          ARM_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
          ARM_CLIENT_SECRET: ${{ secrets.AZURE_CLIENT_SECRET }}
          ARM_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          ARM_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
```

---

## 5. Release with Changelog

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags: ['v*']

permissions:
  contents: write

jobs:
  release:
    name: Create Release
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0             # Full history for changelog

      - name: Generate changelog
        id: changelog
        run: |
          PREVIOUS_TAG=$(git tag --sort=-version:refname | head -2 | tail -1)
          CURRENT_TAG=${GITHUB_REF#refs/tags/}

          if [ -z "$PREVIOUS_TAG" ]; then
            PREVIOUS_TAG=$(git rev-list --max-parents=0 HEAD)
          fi

          echo "## What's Changed" > changelog.md
          echo "" >> changelog.md

          # Features
          FEATURES=$(git log "$PREVIOUS_TAG".."$CURRENT_TAG" --pretty=format:"%s" | grep "^feat" || true)
          if [ -n "$FEATURES" ]; then
            echo "### Features" >> changelog.md
            echo "$FEATURES" | while read -r line; do
              echo "- $line" >> changelog.md
            done
            echo "" >> changelog.md
          fi

          # Bug Fixes
          FIXES=$(git log "$PREVIOUS_TAG".."$CURRENT_TAG" --pretty=format:"%s" | grep "^fix" || true)
          if [ -n "$FIXES" ]; then
            echo "### Bug Fixes" >> changelog.md
            echo "$FIXES" | while read -r line; do
              echo "- $line" >> changelog.md
            done
            echo "" >> changelog.md
          fi

          # Other changes
          OTHERS=$(git log "$PREVIOUS_TAG".."$CURRENT_TAG" --pretty=format:"%s" | grep -v "^feat\|^fix" || true)
          if [ -n "$OTHERS" ]; then
            echo "### Other Changes" >> changelog.md
            echo "$OTHERS" | while read -r line; do
              echo "- $line" >> changelog.md
            done
          fi

          echo "" >> changelog.md
          echo "**Full Changelog**: https://github.com/${{ github.repository }}/compare/$PREVIOUS_TAG...$CURRENT_TAG" >> changelog.md

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run build

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          body_path: changelog.md
          files: |
            dist/**
          draft: false
          prerelease: ${{ contains(github.ref, '-beta') || contains(github.ref, '-rc') }}
```

---

## 6. Dependabot Auto-Merge

```yaml
# .github/workflows/dependabot-automerge.yml
name: Dependabot Auto-Merge

on:
  pull_request:

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    name: Auto-Merge Dependabot
    runs-on: ubuntu-latest
    if: github.actor == 'dependabot[bot]'
    timeout-minutes: 10
    steps:
      - name: Fetch Dependabot metadata
        id: metadata
        uses: dependabot/fetch-metadata@v2
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Auto-merge minor and patch updates
        if: >
          steps.metadata.outputs.update-type == 'version-update:semver-minor' ||
          steps.metadata.outputs.update-type == 'version-update:semver-patch'
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Label major updates for manual review
        if: steps.metadata.outputs.update-type == 'version-update:semver-major'
        run: gh pr edit "$PR_URL" --add-label "needs-review"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 7. PR Labeler

```yaml
# .github/workflows/pr-labeler.yml
name: PR Labeler

on:
  pull_request:
    types: [opened, synchronize]

permissions:
  contents: read
  pull-requests: write

jobs:
  label:
    name: Label PR
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4

      - name: Label by files changed
        uses: actions/labeler@v5
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Label by size
        uses: actions/github-script@v7
        with:
          script: |
            const { data: files } = await github.rest.pulls.listFiles({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number,
            });

            const changes = files.reduce((sum, f) => sum + f.additions + f.deletions, 0);

            let sizeLabel;
            if (changes < 10) sizeLabel = 'size/XS';
            else if (changes < 50) sizeLabel = 'size/S';
            else if (changes < 200) sizeLabel = 'size/M';
            else if (changes < 500) sizeLabel = 'size/L';
            else sizeLabel = 'size/XL';

            await github.rest.issues.addLabels({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              labels: [sizeLabel],
            });
```

Requires `.github/labeler.yml`:

```yaml
# .github/labeler.yml
frontend:
  - changed-files:
    - any-glob-to-any-file: ['src/components/**', 'src/pages/**', '*.css']

backend:
  - changed-files:
    - any-glob-to-any-file: ['src/api/**', 'src/services/**']

docs:
  - changed-files:
    - any-glob-to-any-file: ['docs/**', '*.md']

tests:
  - changed-files:
    - any-glob-to-any-file: ['**/*.test.*', '**/*.spec.*', 'tests/**']

ci:
  - changed-files:
    - any-glob-to-any-file: ['.github/**']

dependencies:
  - changed-files:
    - any-glob-to-any-file: ['package.json', 'package-lock.json', 'requirements.txt']
```

---

## 8. Caching Patterns (Standalone Reference)

```yaml
# .github/workflows/caching-examples.yml
name: Caching Reference

on:
  workflow_dispatch:

jobs:
  npm-cache:
    name: npm with built-in cache
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci

  pnpm-cache:
    name: pnpm with store cache
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile

  pip-cache:
    name: pip with built-in cache
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'
      - run: pip install -r requirements.txt

  turbo-cache:
    name: Turborepo remote cache
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npx turbo run build --cache-dir=.turbo
      - uses: actions/cache@v4
        with:
          path: .turbo
          key: turbo-${{ github.sha }}
          restore-keys: turbo-

  docker-layer-cache:
    name: Docker with GHA cache
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          tags: app:test
          cache-from: type=gha
          cache-to: type=gha,mode=max

  multi-path-cache:
    name: Cache multiple directories
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/cache@v4
        with:
          path: |
            node_modules
            ~/.cache/playwright
            .next/cache
          key: deps-${{ runner.os }}-${{ hashFiles('package-lock.json') }}
          restore-keys: |
            deps-${{ runner.os }}-
      - run: npm ci
```
