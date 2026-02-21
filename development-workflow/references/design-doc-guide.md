# Technical Design Document Guide

> A practical guide for writing technical design documents that drive alignment, reduce rework, and create a lasting record of architectural decisions.

## When to Write a Design Doc

Write a design doc when:

- A feature requires changes across **two or more system boundaries** (services, databases, APIs).
- The estimated implementation effort exceeds **one sprint / one week**.
- Multiple engineers will contribute to the implementation.
- The change introduces a **new technology, pattern, or dependency**.
- A decision has **long-term implications** that are expensive to reverse.
- Stakeholders outside the immediate team need visibility.

Skip a design doc when:

- The change is a straightforward bug fix with an obvious solution.
- A well-established pattern already covers the case (just reference it).
- The scope is a single file / single function with no cross-cutting impact.

---

## Standard Sections

### 1. Title & Metadata

```markdown
# Design: <Feature Name>

| Field       | Value                        |
|-------------|------------------------------|
| Author(s)   | @handle                      |
| Status      | Draft / In Review / Approved |
| Created     | YYYY-MM-DD                   |
| Updated     | YYYY-MM-DD                   |
| Reviewers   | @reviewer1, @reviewer2       |
| Tracking    | JIRA-1234 / GH Issue #42    |
```

**Tips:**
- Keep status current — reviewers need to know if they should comment or if the doc is final.
- Link the tracking ticket so the doc stays connected to implementation.

---

### 2. Overview / Summary

Write 3-5 sentences. Answer:
- What is this feature?
- Why are we building it now?
- What is the high-level approach?

**Tips:**
- Write this section LAST — it summarizes the entire doc.
- A busy reader should understand the proposal from this section alone.

---

### 3. Goals and Non-Goals

**Goals** — concrete, measurable outcomes this design achieves.

**Non-Goals** — things this design intentionally does NOT address (to prevent scope creep).

```markdown
### Goals
- Allow users to authenticate via OAuth 2.0 with Google and GitHub providers.
- Reduce login friction to under 3 clicks from landing page to dashboard.
- Support account linking when the same email exists across providers.

### Non-Goals
- Implementing SAML-based SSO for enterprise customers (deferred to Q3).
- Migrating existing password-based users to OAuth-only.
- Building a custom identity provider.
```

**Tips:**
- Non-Goals are just as important as Goals — they set boundaries.
- Limit to 3-7 items per section. If you have more, you may need to split the design.

---

### 4. Architecture

Describe the system components involved and how they interact. Include a diagram.

```markdown
### Architecture Diagram

​```mermaid
graph LR
    Client[Browser] --> Gateway[API Gateway]
    Gateway --> AuthService[Auth Service]
    AuthService --> UserDB[(User DB)]
    AuthService --> OAuthProvider[OAuth Provider]
    Gateway --> AppService[App Service]
    AppService --> UserDB
​```

### Component Responsibilities

| Component     | Responsibility                              |
|---------------|---------------------------------------------|
| API Gateway   | Route requests, rate limiting, TLS termination |
| Auth Service  | Token issuance, OAuth flow, session management |
| User DB       | User profiles, credentials, linked accounts   |
| App Service   | Business logic, data access                    |
```

**Tips:**
- Use Mermaid diagrams for version-control-friendly visuals.
- Show data flow direction with arrows.
- Name every component — no anonymous boxes.
- Call out new components vs. existing ones.

---

### 5. Data Model

Define entities, relationships, and key fields.

```markdown
### Entity: User

| Field          | Type       | Constraints              |
|----------------|------------|--------------------------|
| id             | UUID       | PK, auto-generated       |
| email          | string     | unique, indexed          |
| display_name   | string     | max 100 chars            |
| created_at     | timestamp  | default: now()           |
| updated_at     | timestamp  | auto-updated             |

### Entity: OAuthLink

| Field          | Type       | Constraints              |
|----------------|------------|--------------------------|
| id             | UUID       | PK                       |
| user_id        | UUID       | FK → User.id             |
| provider       | enum       | google, github           |
| provider_uid   | string     | unique per provider      |
| access_token   | string     | encrypted at rest        |

### Relationships
- User 1 ←→ N OAuthLink
```

**Tips:**
- Include indexes that matter for query patterns.
- Note encryption, PII, and retention policies.
- If using MongoDB, show the document shape instead of tables.

---

### 6. API Design

Define endpoints, request/response contracts, and error codes.

```markdown
### POST /api/auth/oauth/callback

Handles the OAuth callback from the identity provider.

**Request Body:**
​```json
{
  "provider": "google",
  "code": "4/0AX4XfWh...",
  "redirect_uri": "https://app.example.com/auth/callback"
}
​```

**Success Response (200):**
​```json
{
  "access_token": "eyJhbGci...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "display_name": "Jane Doe"
  }
}
​```

**Error Responses:**

| Status | Code               | Description                        |
|--------|--------------------|------------------------------------|
| 400    | invalid_code       | OAuth code is invalid or expired   |
| 409    | email_conflict     | Email already linked to another account |
| 502    | provider_error     | OAuth provider returned an error   |
```

**Tips:**
- Use concrete example values in request/response bodies.
- Document error codes — consumers need them to build proper error handling.
- Specify authentication requirements for each endpoint.

---

### 7. Security Considerations

Address authentication, authorization, data protection, and threat vectors.

```markdown
### Security

- **Token storage:** Access tokens stored server-side in encrypted format (AES-256-GCM).
  Client receives an opaque session cookie (HttpOnly, Secure, SameSite=Strict).
- **CSRF protection:** State parameter validated in OAuth callback.
- **Rate limiting:** /auth/* endpoints limited to 10 requests/minute per IP.
- **Input validation:** Provider and code parameters validated against allowlists.
- **Audit trail:** All auth events logged with anonymized IP and user agent.

### Threat Model

| Threat                  | Mitigation                                    |
|-------------------------|-----------------------------------------------|
| Token theft via XSS     | HttpOnly cookie, no tokens in localStorage    |
| CSRF on callback        | State parameter with HMAC signature           |
| Brute force on login    | Rate limiting + CAPTCHA after 5 failures      |
| Provider impersonation  | Verify token with provider's public keys      |
```

**Tips:**
- If you store PII, mention GDPR/CCPA compliance.
- Think like an attacker — what would you try?
- Reference OWASP Top 10 for common web threats.

---

### 8. Testing Strategy

Define how the feature will be tested at each level.

```markdown
### Testing Strategy

| Level        | Scope                           | Tools                |
|--------------|---------------------------------|----------------------|
| Unit         | Auth service logic, token utils | Jest, @testing-library |
| Integration  | OAuth flow end-to-end           | Supertest, MSW        |
| E2E          | Login → Dashboard flow          | Playwright             |
| Security     | OWASP ZAP scan on auth endpoints| OWASP ZAP             |
| Performance  | 1000 concurrent logins          | k6                     |

### Key Test Scenarios
1. Happy path: Google OAuth login → new user created → dashboard loaded.
2. Account linking: Login with GitHub → same email as existing Google user → accounts merged.
3. Token expiry: Session expires → user redirected to login → smooth re-auth.
4. Provider failure: Google returns 500 → user sees friendly error → retry option.
```

**Tips:**
- Don't just list tools — describe what each test level covers.
- Include negative / edge-case scenarios.
- Specify performance benchmarks (latency, throughput).

---

### 9. Rollout Plan

How the feature goes from merged PR to production.

```markdown
### Rollout Plan

| Phase | Audience         | Duration | Success Criteria            | Rollback Trigger        |
|-------|------------------|----------|-----------------------------|-------------------------|
| 1     | Internal team    | 3 days   | Zero auth errors in logs    | Any P0 bug              |
| 2     | 10% of users     | 1 week   | Error rate < 0.1%           | Error rate > 1%         |
| 3     | 50% of users     | 1 week   | No degradation in login time| P95 latency > 2s        |
| 4     | 100% of users    | —        | Feature flag removed        | —                       |

### Feature Flag
- Flag name: `oauth_login_enabled`
- Default: `false`
- Controlled via: LaunchDarkly / environment variable

### Monitoring
- Dashboard: Grafana "Auth Service" dashboard
- Alerts: PagerDuty for error rate > 1% on /auth/* endpoints
- Key metrics: login success rate, OAuth callback latency, account linking rate
```

**Tips:**
- Define rollback triggers *before* the rollout.
- Always have a feature flag for significant features.
- Link to the monitoring dashboard.

---

### 10. Alternatives Considered

Document approaches you rejected and why.

```markdown
### Alternatives Considered

#### A. Firebase Authentication
- **Pros:** Managed service, quick integration, supports many providers.
- **Cons:** Vendor lock-in, limited customization for account linking,
  pricing unpredictable at scale.
- **Verdict:** Rejected — account linking requirements exceed Firebase's capabilities.

#### B. Auth0
- **Pros:** Rich feature set, enterprise-grade, good documentation.
- **Cons:** Cost ($$$), external dependency for core auth flow.
- **Verdict:** Deferred — may revisit when enterprise SSO is needed in Q3.

#### C. Custom OAuth implementation (chosen)
- **Pros:** Full control over flows, no vendor dependency, aligns with
  existing infrastructure.
- **Cons:** More engineering effort, must maintain security ourselves.
- **Verdict:** Accepted — best fit for current requirements and team capabilities.
```

**Tips:**
- Include at least 2 alternatives (the "do nothing" option can be one).
- Be honest about trade-offs — this builds reviewer trust.
- A rejected alternative today may become the right choice later; document why for future reference.

---

## Review Process

### Before Sending for Review

1. All sections are complete (no "TBD" placeholders for critical information).
2. Diagrams render correctly.
3. API examples are valid JSON/YAML.
4. Links to external resources work.
5. Spell-check completed.

### Reviewer Checklist

- [ ] Goals are clear and the design achieves them.
- [ ] Non-goals are reasonable and complete.
- [ ] Architecture diagram matches the text description.
- [ ] Data model supports all described API operations.
- [ ] Security considerations address key threats.
- [ ] Rollout plan includes rollback criteria.
- [ ] Alternatives are genuine and fairly evaluated.
- [ ] Testing strategy covers happy paths AND failure modes.

### Review Timeline

| Phase | Duration | Action |
|-------|----------|--------|
| Draft | — | Author writes the doc |
| Review | 2-3 business days | Reviewers leave comments |
| Revise | 1-2 business days | Author addresses feedback |
| Approve | 1 business day | Reviewers confirm / approve |
| Implement | — | Engineering begins |

---

## Architecture Decision Record (ADR) — Lightweight Template

For smaller decisions that don't warrant a full design doc, use an ADR.

```markdown
# ADR-NNN: <Decision Title>

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXX
**Deciders:** @person1, @person2

## Context

What is the issue or question we need to decide on?
What constraints and forces are at play?

## Decision

What is the change we are making?
State the decision clearly in one or two sentences.

## Consequences

### Positive
- Benefit 1
- Benefit 2

### Negative
- Trade-off 1
- Trade-off 2

### Neutral
- Side-effect or observation

## Related
- Links to relevant design docs, issues, or previous ADRs
```

### ADR Naming Convention

```
docs/adr/
├── 001-use-postgres-for-user-data.md
├── 002-adopt-oauth2-for-authentication.md
├── 003-choose-react-over-vue.md
└── README.md   ← index of all ADRs with status
```

**Tips for ADRs:**
- Keep them short (under 1 page).
- Write them at the moment of decision, not after the fact.
- Never delete an ADR — mark it as Deprecated or Superseded.
- Number them sequentially for easy reference.
- Store them in the repository alongside the code they affect.
