# Changelog

## 0.2.0 — 2026-08-12

### Added

- Complete live REG.Cloud CloudVPS API v1 and v2 operation coverage.
- Versioned `api.v1` and `api.v2` resource namespaces.
- Billing, IP, Kubernetes kubeconfig, removed-server, VPC, and regional catalog resources.
- Configurable timeouts, context-manager lifecycle, structured safe errors, and OpenAPI drift checks.
- Python 3.11–3.14 CI and PyPI Trusted Publishing workflow.

### Changed

- Modern PEP 517 packaging through `pyproject.toml`.
- Empty successful responses return `None`; HTTP failures raise `CloudVpsAPIError`.
- Tokens and headers are isolated per client instance.

### Removed

- Python 2–3.10, Travis CI, Nose, and the `future` dependency.

### Deprecated

- The `provider` constructor argument and public calls targeting endpoints absent from live OpenAPI.
