# EARS Notation Reference

> **Easy Approach to Requirements Syntax** — A structured natural-language notation for writing unambiguous, testable requirements.

## Overview

EARS eliminates vagueness in requirements by providing five sentence templates. Each template addresses a specific type of system behavior, ensuring every requirement answers **when** the behavior occurs and **what** the system shall do.

## The Five EARS Patterns

### 1. Universal (Ubiquitous)

**When it applies:** Behavior that holds at all times, without any trigger or precondition.

**Syntax:**
```
The <system> shall <action>.
```

**Examples:**

| ID | Requirement |
|----|-------------|
| U-01 | The system shall encrypt all data at rest using AES-256. |
| U-02 | The API shall return responses in JSON format. |
| U-03 | The application shall log all authentication attempts. |
| U-04 | The system shall enforce role-based access control on every endpoint. |
| U-05 | The UI shall meet WCAG 2.1 Level AA accessibility standards. |

**Tips:**
- Use sparingly — most behaviors are not truly universal.
- If you can think of a state or event that gates the behavior, use a different pattern.

---

### 2. Event-Driven

**When it applies:** Behavior triggered by a discrete event detected at the system boundary.

**Syntax:**
```
When <event>, the <system> shall <action>.
```

**Examples:**

| ID | Requirement |
|----|-------------|
| E-01 | When the user submits the login form, the system shall validate the credentials against the user store. |
| E-02 | When a new file is uploaded, the system shall scan the file for malware before storing it. |
| E-03 | When the API receives a request without a valid bearer token, the system shall return HTTP 401. |
| E-04 | When the user clicks "Export", the system shall generate a CSV file containing the current dataset. |
| E-05 | When the CI pipeline detects a failing test, the system shall block the merge request. |

**Tips:**
- The event should be observable and instantaneous (a transition, not a state).
- Use past tense or present simple for the event clause.
- Avoid compound events — split into separate requirements or use combination patterns.

---

### 3. State-Driven (While)

**When it applies:** Behavior that holds only while the system is in a particular state.

**Syntax:**
```
While <state>, the <system> shall <action>.
```

**Examples:**

| ID | Requirement |
|----|-------------|
| S-01 | While the system is in maintenance mode, the system shall display a maintenance banner to all users. |
| S-02 | While the user session is active, the system shall refresh the authentication token every 15 minutes. |
| S-03 | While network connectivity is unavailable, the application shall queue data changes locally. |
| S-04 | While the database connection pool is exhausted, the system shall reject new requests with HTTP 503. |
| S-05 | While the feature flag "dark-mode" is enabled, the UI shall render using the dark color scheme. |

**Tips:**
- The state must be a sustained condition, not a fleeting event.
- Make sure entry and exit conditions for the state are defined elsewhere.

---

### 4. Optional Feature

**When it applies:** Behavior that depends on a configurable option, license, or feature inclusion.

**Syntax:**
```
Where <feature/option is included>, the <system> shall <action>.
```

**Examples:**

| ID | Requirement |
|----|-------------|
| O-01 | Where two-factor authentication is enabled, the system shall require an OTP after password verification. |
| O-02 | Where the premium tier is active, the system shall allow export to PDF format. |
| O-03 | Where the audit log module is installed, the system shall record all data mutations with timestamps. |
| O-04 | Where the notification preference includes email, the system shall send email alerts for critical events. |
| O-05 | Where the organization has enabled SSO, the system shall redirect login requests to the configured IdP. |

**Tips:**
- Clearly define what controls the option (feature flag, config setting, license tier).
- Document how the option is enabled/disabled and who controls it.

---

### 5. Unwanted Behavior (Exception / Negative)

**When it applies:** Handling of undesirable situations the system must cope with — errors, faults, edge cases.

**Syntax:**
```
If <unwanted condition>, the <system> shall <mitigation>.
```

**Examples:**

| ID | Requirement |
|----|-------------|
| N-01 | If the database connection fails, the system shall retry up to 3 times with exponential backoff. |
| N-02 | If the uploaded file exceeds 10 MB, the system shall reject the upload with an error message. |
| N-03 | If the external payment gateway is unreachable, the system shall queue the transaction and notify the user. |
| N-04 | If a user enters an invalid email format, the system shall display an inline validation error. |
| N-05 | If the JWT token has expired, the system shall return HTTP 401 and include a `token_expired` error code. |

**Tips:**
- Focus on *what the system does*, not what it doesn't do.
- Pair with Event-Driven requirements that define the happy path.

---

## Combination Patterns

Real requirements often combine patterns. The order matters: **Feature → State → Event → Action**.

### State + Event (most common combination)

```
While <state>, when <event>, the <system> shall <action>.
```

| ID | Requirement |
|----|-------------|
| C-01 | While the user is authenticated, when the user requests their profile, the system shall return the full profile object including email. |
| C-02 | While the system is in read-only mode, when a write request is received, the system shall return HTTP 503 with a retry-after header. |

### Feature + Event

```
Where <feature>, when <event>, the <system> shall <action>.
```

| ID | Requirement |
|----|-------------|
| C-03 | Where email notifications are enabled, when a new comment is posted on the user's item, the system shall send an email notification within 5 minutes. |

### Feature + State + Event

```
Where <feature>, while <state>, when <event>, the <system> shall <action>.
```

| ID | Requirement |
|----|-------------|
| C-04 | Where the auto-save feature is enabled, while the document is being edited, when 30 seconds elapse since the last change, the system shall persist the current document state. |

### Feature + Unwanted

```
Where <feature>, if <unwanted condition>, the <system> shall <mitigation>.
```

| ID | Requirement |
|----|-------------|
| C-05 | Where offline mode is enabled, if network connectivity is lost during a sync operation, the system shall preserve the local changes and retry sync when connectivity is restored. |

---

## Traceability Matrix Template

Use a traceability matrix to link requirements to design, implementation, and test artifacts.

| Req ID | Pattern | Category | Requirement Summary | Design Section | Implementation | Test Case | Status |
|--------|---------|----------|---------------------|----------------|----------------|-----------|--------|
| U-01 | Universal | Security | Encrypt data at rest | §4.2 Encryption | `EncryptionService` | TC-SEC-01 | Implemented |
| E-01 | Event | Auth | Validate login credentials | §3.1 Auth Flow | `AuthController.login()` | TC-AUTH-01 | In Progress |
| S-01 | State | UX | Show maintenance banner | §5.1 Maintenance | `MaintenanceBanner` | TC-UX-01 | Not Started |
| O-01 | Optional | Auth | Require OTP for 2FA | §3.3 MFA | `MfaMiddleware` | TC-AUTH-05 | Not Started |
| N-01 | Unwanted | Reliability | Retry on DB failure | §4.1 Resilience | `RetryPolicy` | TC-REL-01 | Implemented |

---

## Common Mistakes

### 1. Vague Subjects
```
BAD:  The system should handle errors.
GOOD: If an unhandled exception occurs during request processing, the system shall return HTTP 500 and log the exception with stack trace.
```

### 2. Using "Should" Instead of "Shall"
- **Shall** = mandatory, testable.
- **Should** = desirable, ambiguous — avoid in formal requirements.

### 3. Compound Requirements (More Than One "Shall")
```
BAD:  When the user logs in, the system shall validate credentials and redirect to the dashboard and send a welcome email.
GOOD: Split into E-01 (validate), E-02 (redirect), E-03 (send email).
```

### 4. Missing Measurability
```
BAD:  The system shall respond quickly.
GOOD: When the user submits a search query, the system shall return results within 500 milliseconds for the 95th percentile.
```

### 5. Mixing Problem and Solution
```
BAD:  The system shall use Redis for caching.
GOOD: The system shall cache frequently accessed data to achieve sub-100ms response times for read operations.
```
*(Redis is a design decision, not a requirement.)*

### 6. Negative Requirements Without Mitigation
```
BAD:  The system shall not crash on invalid input.
GOOD: If the user provides invalid input, the system shall return a 400 error with a descriptive validation message.
```

---

## Writing Tips

1. **One behavior per requirement** — if you see "and" joining two actions, split.
2. **Start with the pattern keyword** — When/While/Where/If — to immediately signal the type.
3. **Name the actor** — "the system", "the API", "the mobile client" — not just pronouns.
4. **Quantify where possible** — 500ms, 10 retries, 99.9% uptime.
5. **Use consistent terminology** — define a glossary and refer to it.
6. **Review in pairs** — have another person read the requirement aloud; if they ask "what does X mean?", revise.
7. **Assign IDs early** — use a prefix per pattern (`U-`, `E-`, `S-`, `O-`, `N-`, `C-`) for quick identification.
8. **Version your requirements** — track changes alongside code in the same repository.

---

## Quick Reference Card

| Pattern | Keyword | Template |
|---------|---------|----------|
| Universal | *(none)* | The `<system>` shall `<action>`. |
| Event-Driven | **When** | When `<event>`, the `<system>` shall `<action>`. |
| State-Driven | **While** | While `<state>`, the `<system>` shall `<action>`. |
| Optional Feature | **Where** | Where `<feature>`, the `<system>` shall `<action>`. |
| Unwanted Behavior | **If** | If `<condition>`, the `<system>` shall `<mitigation>`. |
| Combination | Mix | Where `<feat>`, while `<state>`, when `<event>`, the `<system>` shall `<action>`. |
