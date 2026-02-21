# Python Libraries Evaluation & Selection Guide

## Library Evaluation Criteria

### 1. Maintenance Activity
- **Commit frequency**: Regular commits in the last 6 months
- **Issue response time**: Maintainers respond within days, not months
- **Release cadence**: Stable releases at least quarterly
- **CI/CD status**: Passing builds on main branch

### 2. Community & Popularity
- **GitHub stars**: Indicator of interest (not quality alone)
- **Download stats**: PyPI monthly downloads via pypistats.org
- **Stack Overflow presence**: Active Q&A community
- **Contributors**: Multiple active contributors reduce bus factor

### 3. Security
- **CVE history**: Check via `pip-audit` or safety DB
- **Security advisories**: GitHub security tab, Snyk database
- **Dependency chain**: Fewer transitive dependencies = smaller attack surface
- **Signed releases**: Package signing and provenance attestation

### 4. License Compatibility
- **MIT/BSD/Apache 2.0**: Permissive, safe for most projects
- **LGPL**: Acceptable with dynamic linking
- **GPL**: Copyleft, may restrict proprietary use
- **AGPL**: Network copyleft, restricts SaaS use
- Always verify with `pip show <package>` or pyproject.toml

### 5. API Design Quality
- **Type annotations**: Full typing support (py.typed marker)
- **Documentation**: Comprehensive docs with examples
- **Consistent API surface**: Predictable method naming and signatures
- **Error handling**: Clear exception hierarchy, not bare exceptions
- **Async support**: Native async API if applicable

### 6. Performance & Compatibility
- **Python version support**: Supports 3.10+ minimum (current as of 2025)
- **Platform support**: Linux, macOS, Windows
- **Benchmark data**: Published benchmarks or reproducible comparisons
- **Memory footprint**: Acceptable for target deployment

---

## Library Selection Checklist

Before adopting a library, verify:

- [ ] Active maintenance (commits within last 3 months)
- [ ] 1000+ GitHub stars OR established in domain
- [ ] Compatible license for your project
- [ ] No unpatched critical CVEs
- [ ] Python 3.10+ support
- [ ] Type annotations available
- [ ] Documentation covers your use case
- [ ] Acceptable dependency tree size (`pipdeptree`)
- [ ] Community support channels exist
- [ ] Migration path exists if library is abandoned

---

## Essential Python Libraries by Category

### Web Frameworks

| Library | Version (2025) | Use Case | Key Strength |
|---------|---------------|----------|--------------|
| **FastAPI** | 0.115+ | Async APIs, microservices | Auto OpenAPI docs, Pydantic validation, async-first |
| **Flask** | 3.1+ | Small-to-medium web apps | Simplicity, huge ecosystem of extensions |
| **Django** | 5.1+ | Full-stack web apps | Batteries-included, ORM, admin panel |
| **Litestar** | 2.x | High-performance APIs | Msgspec integration, dependency injection |
| **Starlette** | 0.41+ | ASGI toolkit | Foundation for FastAPI, lightweight |

### Data Processing & Analysis

| Library | Version (2025) | Use Case | Key Strength |
|---------|---------------|----------|--------------|
| **pandas** | 2.2+ | Tabular data analysis | Mature ecosystem, DataFrame API |
| **Polars** | 1.x | High-performance data processing | Rust-backed, lazy evaluation, multi-threaded |
| **NumPy** | 2.1+ | Numerical computing | Array operations, foundation for scientific Python |
| **DuckDB** | 1.1+ | Analytical SQL queries | In-process OLAP, reads Parquet/CSV directly |
| **PyArrow** | 17+ | Columnar data, IPC | Apache Arrow format, zero-copy reads |

### Testing

| Library | Version (2025) | Use Case | Key Strength |
|---------|---------------|----------|--------------|
| **pytest** | 8.x | Unit/integration testing | Fixtures, plugins, parametrize |
| **hypothesis** | 6.x | Property-based testing | Auto-generates edge case inputs |
| **coverage** | 7.x | Code coverage | Branch coverage, HTML reports |
| **pytest-asyncio** | 0.24+ | Async test support | Seamless async fixture/test integration |
| **respx** | 0.22+ | HTTP mocking for httpx | Pattern-matched request mocking |

### Async & Concurrency

| Library | Version (2025) | Use Case | Key Strength |
|---------|---------------|----------|--------------|
| **asyncio** | stdlib | Async I/O | Built-in, standard event loop |
| **trio** | 0.27+ | Structured concurrency | Cancel scopes, nurseries, strict design |
| **anyio** | 4.x | Backend-agnostic async | Works with asyncio and trio |
| **uvloop** | 0.21+ | Fast event loop | Drop-in asyncio speedup on Linux/macOS |

### CLI Tools

| Library | Version (2025) | Use Case | Key Strength |
|---------|---------------|----------|--------------|
| **Typer** | 0.13+ | Modern CLI apps | Type-hint driven, auto help/completions |
| **Click** | 8.x | CLI framework | Composable commands, mature ecosystem |
| **Rich** | 13.x | Terminal formatting | Tables, progress bars, syntax highlighting |
| **Textual** | 0.89+ | Terminal UI apps | TUI framework built on Rich |

### Validation & Serialization

| Library | Version (2025) | Use Case | Key Strength |
|---------|---------------|----------|--------------|
| **Pydantic** | 2.10+ | Data validation | JSON Schema, FastAPI integration, Rust core |
| **msgspec** | 0.19+ | Fast serialization | Zero-copy decoding, struct types |
| **attrs** | 24.x | Class boilerplate reduction | Slots, validators, lightweight |
| **cattrs** | 24.x | Structure/unstructure | Pairs with attrs for serialization |

### HTTP Clients

| Library | Version (2025) | Use Case | Key Strength |
|---------|---------------|----------|--------------|
| **httpx** | 0.28+ | Sync + async HTTP | requests-like API with async support |
| **requests** | 2.32+ | Sync HTTP | Battle-tested, simple API |
| **aiohttp** | 3.11+ | Async HTTP client/server | Mature async ecosystem |

### Database & ORM

| Library | Version (2025) | Use Case | Key Strength |
|---------|---------------|----------|--------------|
| **SQLAlchemy** | 2.0+ | ORM + SQL toolkit | Async support, mature, flexible |
| **SQLModel** | 0.0.22+ | Pydantic + SQLAlchemy | Type-safe ORM with Pydantic models |
| **Motor** | 3.6+ | Async MongoDB | Official async MongoDB driver |
| **Redis (redis-py)** | 5.2+ | Redis client | Async support, cluster mode |

---

## Quick Evaluation Command Sequence

```bash
# Check PyPI stats
pip install pypistats
pypistats overall <package> --last-month

# Audit dependencies
pip install pip-audit
pip-audit

# View dependency tree
pip install pipdeptree
pipdeptree --packages <package>

# Check type stub availability
pip install mypy
mypy --install-types
```
