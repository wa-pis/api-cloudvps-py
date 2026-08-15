# Delta for Package Quality

## ADDED Requirements

### Requirement: Modern standard package metadata

The project SHALL build through `pyproject.toml` with a PEP 517-compatible
Setuptools backend and SHALL produce one universal Python 3 wheel and one source
distribution containing the license, README, and package sources.

#### Scenario: Build distributions from a clean checkout

- **GIVEN** a clean supported Python environment with build tooling
- **WHEN** `python -m build` is executed
- **THEN** wheel and source distribution artifacts are created
- **AND** both pass package metadata checks
- **AND** the wheel installs and imports without the repository on `sys.path`

### Requirement: Supported Python versions

The package SHALL declare and continuously test Python 3.11, 3.12, 3.13, and
3.14, and SHALL reject Python versions below its declared minimum.

#### Scenario: CI version matrix

- **GIVEN** a pull request changes package code
- **WHEN** CI runs
- **THEN** the test suite passes independently on Python 3.11 through 3.14

### Requirement: Minimal runtime dependencies

The installed package SHALL require only a maintained Requests release at
runtime and SHALL NOT install `future`, `nose`, linters, build tools, or test
tools as runtime dependencies.

#### Scenario: Inspect wheel dependencies

- **GIVEN** the built wheel metadata
- **WHEN** runtime requirements are inspected
- **THEN** Requests is the only direct runtime dependency

### Requirement: Offline request-contract coverage

Every public resource operation SHALL have an offline test that verifies HTTP
method, versioned URL, query parameters, JSON payload, timeout, and applicable
response behavior without contacting REG.Cloud.

#### Scenario: Endpoint manifest is fully tested

- **GIVEN** the committed v1/v2 operation manifest
- **WHEN** the unit suite runs
- **THEN** each manifest operation is exercised by at least one request-contract test
- **AND** no test needs a real bearer token

### Requirement: Transport security regression tests

The test suite SHALL cover client token isolation, token redaction, timeouts,
empty success responses, structured errors, non-JSON errors, and the absence of
automatic mutating retries.

#### Scenario: Security regression suite

- **GIVEN** simulated success, provider error, and connection failure responses
- **WHEN** transport tests run
- **THEN** every required transport behavior is asserted
- **AND** test failure output contains no real credential

### Requirement: Opt-in live integration verification

The project SHALL provide a separately invoked live integration suite that reads
the bearer token from an environment variable, is excluded from normal CI, and
can exercise both read-only and mutating API operations under operator control.

#### Scenario: No token supplied

- **GIVEN** the integration command is run without the token environment variable
- **WHEN** test discovery begins
- **THEN** live tests skip without sending any request

#### Scenario: Full live verification is enabled

- **GIVEN** a token and explicit full-integration mode are present in the environment
- **WHEN** the live suite runs
- **THEN** it verifies v1 and v2 operations against temporary resources where needed
- **AND** attempts cleanup of resources it created
- **AND** reports created resource identifiers, cleanup results, and any charges visible to the API

### Requirement: Fast deterministic CI

Pull-request and default-branch CI SHALL run formatting/lint checks, the offline
test matrix, distribution build, metadata validation, and wheel installation
without using cloud credentials.

#### Scenario: Forked pull request

- **GIVEN** a pull request from an untrusted fork
- **WHEN** CI runs
- **THEN** it receives read-only repository permissions
- **AND** has no PyPI or CloudVPS credential
- **AND** can complete all required checks

### Requirement: OpenAPI operation drift monitoring

A scheduled and manually dispatchable read-only workflow SHALL compare the live
v1/v2 method-path inventory against the committed endpoint manifest without
modifying repository or provider state.

#### Scenario: Provider adds or removes an operation

- **GIVEN** the live OpenAPI inventory differs from the committed manifest
- **WHEN** the drift workflow runs
- **THEN** the workflow fails with the added and removed method-path pairs
- **AND** does not update files or open issues automatically

### Requirement: Dependency update automation

Dependabot SHALL check Python package and GitHub Actions dependencies on a
regular schedule while preserving immutable Action pins.

#### Scenario: A pinned Action has a new release

- **GIVEN** Dependabot detects a new reviewed Action release
- **WHEN** it opens an update pull request
- **THEN** the workflow reference is updated to a new full commit SHA
- **AND** the human-readable release tag remains documented on the same line
