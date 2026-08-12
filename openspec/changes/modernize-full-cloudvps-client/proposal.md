# Proposal: Modernize the Full REG.Cloud CloudVPS Client

## Intent

Revive `api-cloudvps-py` as a secure, maintained, synchronous Python client
covering the complete public REG.Cloud CloudVPS API v1 and v2 contracts, with a
safe GitHub-to-PyPI release process.

## Problem

The published client has not been released since 2018. It targets Python
2.7-3.7, has no meaningful request-contract tests or GitHub Actions workflows,
and was published to PyPI with a long-lived credential. Its HTTP headers are
shared across client instances, so constructing a second client replaces the
first client's bearer token. Requests have no timeout or consistent HTTP error
handling.

The resource surface has also drifted from the live provider contracts. The
client omits API v2 entirely and lacks current v1 operations for account
settings, billing, IP addresses, Kubernetes kubeconfig, removed servers, and
private networks. Several existing methods target endpoints no longer present
in the current OpenAPI schema.

## Scope

### In scope

- Secure, instance-isolated HTTP transport with configurable timeouts and
  consistent response/error behavior.
- Every operation currently exposed by the live CloudVPS OpenAPI v1 contract.
- API v2 images and plans, including required regional pagination and filters.
- A compatibility and deprecation path for the existing `cloudvps.Api` API.
- Modern Python packaging for Python 3.11-3.14.
- Unit/request-contract tests for every public operation without live mutation.
- CI, dependency maintenance, API drift monitoring, and PyPI Trusted Publishing.
- Updated user, migration, security, and maintainer documentation.

### Out of scope

- REG.Cloud products not present in the CloudVPS v1/v2 OpenAPI documents.
- Replacing or extending the official REG.Cloud Terraform provider.
- An asynchronous client.
- Generated resource models, validation frameworks, or OpenAPI code generation.
- Automatic retries for mutating requests.
- Automated integration tests that create, alter, or delete paid resources.

## Capabilities

### Added capabilities

- `client-transport`: secure authentication, request execution, errors, timeout,
  session lifecycle, and v1/v2 routing.
- `cloudvps-api-v1`: complete coverage of the live API v1 operations.
- `cloudvps-api-v2`: complete coverage of the live API v2 images and plans.
- `public-compatibility`: preserved imports, aliases, deprecations, and versioning.
- `package-quality`: modern packaging, supported Python versions, CI, tests, and
  contract-drift detection.
- `secure-release`: least-privilege GitHub Actions and OIDC PyPI publishing.
- `project-documentation`: current usage, API reference, migration, security,
  and Terraform positioning.

## Compatibility and migration

The PyPI distribution name `api-cloudvps-py`, the `cloudvps` import namespace,
and `from cloudvps import Api` remain supported. Existing resource accessors are
retained as v1 aliases where their provider operations still exist. API v2 is
introduced through an explicit versioned namespace.

Methods targeting endpoints absent from the live OpenAPI schema are not allowed
to keep issuing undocumented requests. They will emit a deprecation warning and
fail locally with migration guidance, or be mapped to a documented equivalent
when the mapping is unambiguous. Response bodies remain ordinary dictionaries
and lists. The change is released as `0.2.0`; removal of deprecated entry points
is reserved for `1.0.0`.

## Security impact

- Bearer tokens become instance-owned and must never appear in representations,
  exceptions, test output, or CI logs.
- Every network request has a finite timeout and verified TLS by default.
- Production publishing uses short-lived OIDC credentials instead of a stored
  PyPI token.
- Only the publish job receives `id-token: write`; all Actions are immutable SHA
  pins and release deployment is protected by a GitHub environment.

## Delivery

Implementation proceeds in reviewable phases: packaging baseline, transport,
API v1, API v2, compatibility, quality/documentation, release hardening, then a
TestPyPI release candidate and production `0.2.0` release.

## Risks and rollback

- Provider drift: lock request-contract tests to the current OpenAPI operation
  inventory and monitor the live schemas on a schedule.
- Compatibility regressions: retain documented aliases, publish a migration
  guide, and test representative 0.1.7 usage.
- Broken release: PyPI files are immutable; yank the affected release, publish a
  corrected patch release, and keep the GitHub release audit trail.
- Provider outage: CI unit tests remain offline; only the advisory drift workflow
  contacts the public schema endpoints.
