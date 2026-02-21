# Example Research Workflow: Evaluate & Select a Python HTTP Client Library

## Scenario

> "I need an HTTP client for a Python async service that makes external API calls.
> It should support both sync testing and async production use, have good typing,
> and be actively maintained."

---

## Phase 1: Planning & Web Search

### 1.1 Define Requirements

| Requirement | Priority | Notes |
|-------------|----------|-------|
| Async support (native) | Must have | Production runs on asyncio |
| Sync API available | Should have | Simplifies testing and scripts |
| Type annotations | Must have | Codebase uses mypy strict mode |
| HTTP/2 support | Nice to have | Some upstream APIs use HTTP/2 |
| Active maintenance | Must have | Security patches, Python version support |
| Streaming responses | Should have | Some endpoints return large payloads |
| Connection pooling | Must have | High-throughput service |
| Retry/timeout control | Must have | Resilience in production |

### 1.2 Identify Candidates

From ecosystem knowledge and web search:

1. **httpx** — Modern async/sync client, requests-compatible API
2. **requests** — The classic sync HTTP library
3. **aiohttp** — Mature async HTTP client and server

### 1.3 Preliminary Comparison

| Criteria | httpx | requests | aiohttp |
|----------|-------|----------|---------|
| Async native | Yes | No | Yes |
| Sync API | Yes | Yes (only) | No (sync wrapper needed) |
| HTTP/2 | Yes (optional) | No | No |
| Type stubs | Built-in py.typed | Third-party types-requests | Third-party stubs |
| Maintenance | Active (Encode team) | Active (PSF/Nate) | Active (aio-libs) |

**Decision:** requests is eliminated (no async). Deep-dive httpx vs aiohttp.

---

## Phase 2: Library Resolution (Context7)

### 2.1 Resolve Library IDs

```
resolve-library-id(libraryName: "python httpx")
→ { id: "/python/encode/httpx", name: "httpx", ... }

resolve-library-id(libraryName: "python aiohttp")
→ { id: "/python/aio-libs/aiohttp", name: "aiohttp", ... }
```

### 2.2 Key Observations from Resolution

- Both libraries are indexed with good documentation coverage
- httpx is under the Encode organization (also maintains Starlette, uvicorn)
- aiohttp is under aio-libs (also maintains aiohttp-cors, aiosignal)

---

## Phase 3: Documentation Fetching & Deep Comparison

### 3.1 Fetch Targeted Documentation

```
get-library-docs(
  context7CompatibleLibraryID: "/python/encode/httpx",
  topic: "async client and connection pooling",
  tokens: 4000
)

get-library-docs(
  context7CompatibleLibraryID: "/python/aio-libs/aiohttp",
  topic: "client session and connection pooling",
  tokens: 4000
)
```

### 3.2 Feature Deep-Dive

#### httpx Async Client Usage (from docs)

```python
import httpx

# Async with connection pooling via client context manager
async with httpx.AsyncClient(
    base_url="https://api.example.com",
    timeout=httpx.Timeout(10.0, connect=5.0),
    limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
) as client:
    response = await client.get("/users", params={"page": 1})
    response.raise_for_status()
    data = response.json()
```

#### aiohttp Client Session Usage (from docs)

```python
import aiohttp

# Async with connection pooling via session
connector = aiohttp.TCPConnector(limit=100, limit_per_host=20)
timeout = aiohttp.ClientTimeout(total=10, connect=5)

async with aiohttp.ClientSession(
    base_url="https://api.example.com",
    connector=connector,
    timeout=timeout,
) as session:
    async with session.get("/users", params={"page": 1}) as response:
        response.raise_for_status()
        data = await response.json()
```

### 3.3 Detailed Comparison

| Feature | httpx | aiohttp |
|---------|-------|---------|
| **API style** | requests-compatible, familiar | Unique API, context managers for responses |
| **Sync + Async** | Both in one package | Async only (sync requires `aiohttp-client` or wrapping) |
| **HTTP/2** | Yes, via `httpx[http2]` (h2) | No native support |
| **Connection pooling** | `httpx.Limits` on client | `TCPConnector` with limit params |
| **Retry support** | Via `httpx` transport or tenacity | Via `aiohttp-retry` third-party package |
| **Streaming** | `async for chunk in response.aiter_bytes()` | `async for chunk in response.content.iter_any()` |
| **Response handling** | Direct access: `response.json()` | Context manager: `async with session.get() as resp` |
| **Type annotations** | Full, ships py.typed | Partial, improving |
| **Middleware/hooks** | Event hooks, custom transports | Signals, trace config |
| **Timeout config** | `httpx.Timeout` (granular) | `aiohttp.ClientTimeout` (granular) |
| **File uploads** | `files={"upload": open(...)}` | `data=aiohttp.FormData()` |
| **Test support** | `httpx.MockTransport` for testing | `aiohttp.test_utils` |
| **WebSocket** | No (separate library needed) | Yes, built-in |
| **Server component** | No | Yes, full ASGI-like server |
| **Install size** | ~600 KB + httpcore | ~1.2 MB + multidict, yarl, etc. |
| **Python version** | 3.8+ | 3.8+ |
| **GitHub stars** | ~13k | ~15k |
| **Monthly PyPI downloads** | ~40M | ~80M |

### 3.4 Benchmark Considerations

- Raw throughput: aiohttp has a slight edge in benchmarks for high-concurrency scenarios due to its C-accelerated parser
- For typical API client use (not server), the difference is negligible
- httpx's HTTP/2 multiplexing can outperform HTTP/1.1 connection pooling for certain upstream APIs

---

## Final Recommendation

### Winner: **httpx**

#### Rationale

1. **Dual sync/async API** — Single dependency for both production (async) and scripting/testing (sync), reducing cognitive overhead and dependency sprawl

2. **Type annotations** — Ships with `py.typed` marker and complete annotations, satisfying our mypy strict requirement without third-party stubs

3. **HTTP/2 support** — Optional but available when needed, future-proofing against upstream API migrations

4. **requests-compatible API** — Minimal learning curve for the team, easy migration from existing requests-based code

5. **Testing story** — `MockTransport` allows deterministic testing without mocking internals, pairs well with `respx` for higher-level mocking

6. **Active maintenance** — Encode team maintains the full async Python web stack (Starlette, uvicorn, httpx), ensuring coherent ecosystem evolution

#### When to Choose aiohttp Instead

- WebSocket client requirements (built into aiohttp)
- Need a combined HTTP client + server in one package
- Existing aiohttp codebase with established patterns
- Maximum raw throughput in extreme concurrency scenarios (10k+ concurrent connections)

### Recommended Setup

```toml
# pyproject.toml
[project]
dependencies = [
    "httpx>=0.28,<1.0",
    "httpx[http2]",  # optional HTTP/2 support
]

[project.optional-dependencies]
test = [
    "respx>=0.22",  # HTTP mocking for httpx
    "pytest-asyncio>=0.24",
]
```

```python
# src/http_client.py
import httpx

DEFAULT_TIMEOUT = httpx.Timeout(timeout=30.0, connect=10.0)
DEFAULT_LIMITS = httpx.Limits(
    max_connections=100,
    max_keepalive_connections=20,
)

def create_client(**kwargs) -> httpx.AsyncClient:
    """Create a configured async HTTP client."""
    return httpx.AsyncClient(
        timeout=kwargs.pop("timeout", DEFAULT_TIMEOUT),
        limits=kwargs.pop("limits", DEFAULT_LIMITS),
        **kwargs,
    )
```
