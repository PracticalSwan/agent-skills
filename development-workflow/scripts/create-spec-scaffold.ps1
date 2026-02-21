<#
.SYNOPSIS
    Creates a spec-driven development scaffold for a project.

.DESCRIPTION
    Generates docs/requirements.md, docs/design.md, and docs/tasks.md with
    pre-filled templates using EARS notation patterns and structured design
    document format. Ready to fill in for any new feature.

.PARAMETER ProjectName
    Name of the project or feature. Used in document titles and headings.

.PARAMETER OutputDir
    Directory where the docs/ folder will be created. Defaults to current directory.

.EXAMPLE
    .\create-spec-scaffold.ps1 -ProjectName "User Authentication" -OutputDir "./my-project"
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectName,

    [Parameter(Mandatory = $false)]
    [string]$OutputDir = "."
)

$ErrorActionPreference = "Stop"

$docsDir = Join-Path $OutputDir "docs"
if (-not (Test-Path $docsDir)) {
    New-Item -ItemType Directory -Path $docsDir -Force | Out-Null
}

$date = Get-Date -Format "yyyy-MM-dd"

# ── requirements.md ──────────────────────────────────────────────────────────

$requirementsContent = @"
# Requirements: $ProjectName

| Field     | Value          |
|-----------|----------------|
| Author    | <!-- @handle --> |
| Created   | $date          |
| Updated   | $date          |
| Status    | Draft          |
| Tracking  | <!-- Ticket --> |

## Glossary

| Term | Definition |
|------|------------|
| <!-- Term 1 --> | <!-- Definition --> |
| <!-- Term 2 --> | <!-- Definition --> |

## Universal Requirements

> Behaviors that hold at all times.

| ID   | Requirement |
|------|-------------|
| U-01 | The system shall <!-- action -->. |
| U-02 | The system shall <!-- action -->. |

## Event-Driven Requirements

> Behaviors triggered by a discrete event.

| ID   | Requirement |
|------|-------------|
| E-01 | When <!-- event -->, the system shall <!-- action -->. |
| E-02 | When <!-- event -->, the system shall <!-- action -->. |
| E-03 | When <!-- event -->, the system shall <!-- action -->. |

## State-Driven Requirements

> Behaviors that hold while the system is in a specific state.

| ID   | Requirement |
|------|-------------|
| S-01 | While <!-- state -->, the system shall <!-- action -->. |
| S-02 | While <!-- state -->, the system shall <!-- action -->. |

## Optional Feature Requirements

> Behaviors gated by a feature flag, license, or configuration.

| ID   | Requirement |
|------|-------------|
| O-01 | Where <!-- feature/option -->, the system shall <!-- action -->. |
| O-02 | Where <!-- feature/option -->, the system shall <!-- action -->. |

## Unwanted Behavior Requirements

> Error handling and edge cases.

| ID   | Requirement |
|------|-------------|
| N-01 | If <!-- unwanted condition -->, the system shall <!-- mitigation -->. |
| N-02 | If <!-- unwanted condition -->, the system shall <!-- mitigation -->. |
| N-03 | If <!-- unwanted condition -->, the system shall <!-- mitigation -->. |

## Combination Requirements

> Requirements that combine multiple patterns.

| ID   | Requirement |
|------|-------------|
| C-01 | While <!-- state -->, when <!-- event -->, the system shall <!-- action -->. |
| C-02 | Where <!-- feature -->, when <!-- event -->, the system shall <!-- action -->. |

## Traceability Matrix

| Req ID | Pattern | Category | Summary | Design Ref | Implementation | Test Case | Status |
|--------|---------|----------|---------|------------|----------------|-----------|--------|
| U-01   | Universal | <!-- cat --> | <!-- summary --> | <!-- section --> | <!-- code --> | <!-- TC --> | Not Started |
| E-01   | Event | <!-- cat --> | <!-- summary --> | <!-- section --> | <!-- code --> | <!-- TC --> | Not Started |

## Non-Functional Requirements

| ID    | Category    | Requirement |
|-------|-------------|-------------|
| NF-01 | Performance | The system shall <!-- performance target -->. |
| NF-02 | Security    | The system shall <!-- security requirement -->. |
| NF-03 | Availability| The system shall <!-- availability target -->. |
"@

$requirementsPath = Join-Path $docsDir "requirements.md"
Set-Content -Path $requirementsPath -Value $requirementsContent -Encoding UTF8

# ── design.md ────────────────────────────────────────────────────────────────

$designContent = @"
# Design: $ProjectName

| Field       | Value                        |
|-------------|------------------------------|
| Author(s)   | <!-- @handle -->             |
| Status      | Draft                        |
| Created     | $date                        |
| Updated     | $date                        |
| Reviewers   | <!-- @reviewer1 -->          |
| Tracking    | <!-- Ticket -->              |

## Overview

<!-- 3-5 sentence summary: What is this? Why now? High-level approach? -->

## Goals

- <!-- Concrete measurable outcome 1 -->
- <!-- Concrete measurable outcome 2 -->
- <!-- Concrete measurable outcome 3 -->

## Non-Goals

- <!-- What this design intentionally does NOT address -->
- <!-- Deferred scope item -->

## Architecture

### Architecture Diagram

``````mermaid
graph LR
    Client[Client] --> API[API Server]
    API --> DB[(Database)]
    API --> External[External Service]
``````

### Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| <!-- Component 1 --> | <!-- What it does --> |
| <!-- Component 2 --> | <!-- What it does --> |

## Data Model

### Entity: <!-- EntityName -->

| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | PK, auto-generated |
| <!-- field --> | <!-- type --> | <!-- constraints --> |
| created_at | timestamp | default: now() |
| updated_at | timestamp | auto-updated |

### Relationships

<!-- Describe entity relationships: 1-to-many, many-to-many, etc. -->

## API Design

### <!-- METHOD --> <!-- /api/path -->

<!-- Description of what this endpoint does. -->

**Request:**
``````json
{
  "field": "value"
}
``````

**Success Response (200):**
``````json
{
  "result": "value"
}
``````

**Error Responses:**

| Status | Code | Description |
|--------|------|-------------|
| 400 | <!-- code --> | <!-- description --> |
| 401 | unauthorized | Missing or invalid authentication |
| 500 | internal_error | Unexpected server error |

## Security Considerations

- **Authentication:** <!-- How are users authenticated? -->
- **Authorization:** <!-- How is access controlled? -->
- **Data protection:** <!-- Encryption, PII handling -->
- **Rate limiting:** <!-- Throttling strategy -->

### Threat Model

| Threat | Mitigation |
|--------|------------|
| <!-- Threat 1 --> | <!-- Mitigation --> |
| <!-- Threat 2 --> | <!-- Mitigation --> |

## Testing Strategy

| Level | Scope | Tools |
|-------|-------|-------|
| Unit | <!-- What is unit-tested --> | <!-- Jest, pytest, etc. --> |
| Integration | <!-- Integration scope --> | <!-- Tools --> |
| E2E | <!-- User flows tested --> | <!-- Playwright, Cypress --> |

### Key Test Scenarios

1. <!-- Happy path scenario -->
2. <!-- Error / edge case scenario -->
3. <!-- Performance scenario -->

## Rollout Plan

| Phase | Audience | Duration | Success Criteria | Rollback Trigger |
|-------|----------|----------|------------------|------------------|
| 1 | Internal | <!-- days --> | <!-- criteria --> | <!-- trigger --> |
| 2 | <!-- % --> | <!-- days --> | <!-- criteria --> | <!-- trigger --> |
| 3 | 100% | — | Feature flag removed | — |

### Feature Flag

- **Name:** ``<!-- flag_name -->``
- **Default:** ``false``
- **Controlled via:** <!-- LaunchDarkly / env var / config -->

## Alternatives Considered

### A. <!-- Alternative 1 -->

- **Pros:** <!-- advantages -->
- **Cons:** <!-- disadvantages -->
- **Verdict:** Rejected — <!-- reason -->

### B. <!-- Alternative 2 -->

- **Pros:** <!-- advantages -->
- **Cons:** <!-- disadvantages -->
- **Verdict:** Rejected — <!-- reason -->

## Open Questions

- [ ] <!-- Question that needs resolution before implementation -->
- [ ] <!-- Another open question -->

## References

- <!-- Link to relevant docs, RFCs, prior art -->
"@

$designPath = Join-Path $docsDir "design.md"
Set-Content -Path $designPath -Value $designContent -Encoding UTF8

# ── tasks.md ─────────────────────────────────────────────────────────────────

$tasksContent = @"
# Implementation Plan: $ProjectName

| Field     | Value          |
|-----------|----------------|
| Author    | <!-- @handle --> |
| Created   | $date          |
| Updated   | $date          |
| Status    | Not Started    |
| Design    | [design.md](./design.md) |
| Reqs      | [requirements.md](./requirements.md) |

## Summary

<!-- Brief description of the implementation scope and approach. -->

## Task Breakdown

### Phase 1: Foundation

| ID | Task | Assignee | Estimate | Depends On | Reqs | Status |
|----|------|----------|----------|------------|------|--------|
| T-01 | <!-- Setup / scaffolding task --> | <!-- @dev --> | <!-- Xh --> | — | <!-- U-01 --> | Not Started |
| T-02 | <!-- Data model / schema task --> | <!-- @dev --> | <!-- Xh --> | T-01 | <!-- E-01 --> | Not Started |
| T-03 | <!-- Core service / logic task --> | <!-- @dev --> | <!-- Xh --> | T-02 | <!-- E-02 --> | Not Started |

### Phase 2: Feature Implementation

| ID | Task | Assignee | Estimate | Depends On | Reqs | Status |
|----|------|----------|----------|------------|------|--------|
| T-04 | <!-- API endpoint task --> | <!-- @dev --> | <!-- Xh --> | T-03 | <!-- E-03 --> | Not Started |
| T-05 | <!-- UI / frontend task --> | <!-- @dev --> | <!-- Xh --> | T-04 | <!-- S-01 --> | Not Started |
| T-06 | <!-- Integration task --> | <!-- @dev --> | <!-- Xh --> | T-04, T-05 | <!-- C-01 --> | Not Started |

### Phase 3: Quality & Release

| ID | Task | Assignee | Estimate | Depends On | Reqs | Status |
|----|------|----------|----------|------------|------|--------|
| T-07 | <!-- Write unit tests --> | <!-- @dev --> | <!-- Xh --> | T-03 | — | Not Started |
| T-08 | <!-- Write integration tests --> | <!-- @dev --> | <!-- Xh --> | T-06 | — | Not Started |
| T-09 | <!-- Write E2E tests --> | <!-- @dev --> | <!-- Xh --> | T-06 | — | Not Started |
| T-10 | <!-- Documentation --> | <!-- @dev --> | <!-- Xh --> | T-06 | — | Not Started |
| T-11 | <!-- Feature flag setup --> | <!-- @dev --> | <!-- Xh --> | T-06 | — | Not Started |
| T-12 | <!-- Phased rollout & monitoring --> | <!-- @dev --> | <!-- Xh --> | T-11 | — | Not Started |

## Dependency Graph

``````mermaid
graph TD
    T01[T-01 Setup] --> T02[T-02 Data Model]
    T02 --> T03[T-03 Core Logic]
    T03 --> T04[T-04 API]
    T03 --> T07[T-07 Unit Tests]
    T04 --> T05[T-05 UI]
    T04 --> T06[T-06 Integration]
    T05 --> T06
    T06 --> T08[T-08 Integration Tests]
    T06 --> T09[T-09 E2E Tests]
    T06 --> T10[T-10 Docs]
    T06 --> T11[T-11 Feature Flag]
    T11 --> T12[T-12 Rollout]
``````

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| <!-- Risk 1 --> | Medium | High | <!-- Plan --> |
| <!-- Risk 2 --> | Low | Medium | <!-- Plan --> |

## Progress Log

### $date
- Created implementation plan.
- <!-- Initial notes -->
"@

$tasksPath = Join-Path $docsDir "tasks.md"
Set-Content -Path $tasksPath -Value $tasksContent -Encoding UTF8

# ── Summary ──────────────────────────────────────────────────────────────────

Write-Host ""
Write-Host "Spec scaffold created for '$ProjectName'" -ForegroundColor Green
Write-Host ""
Write-Host "  $requirementsPath" -ForegroundColor Cyan
Write-Host "  $designPath" -ForegroundColor Cyan
Write-Host "  $tasksPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Fill in requirements.md using EARS notation patterns"
Write-Host "  2. Complete design.md with architecture and API contracts"
Write-Host "  3. Break down work into tasks in tasks.md"
Write-Host ""
