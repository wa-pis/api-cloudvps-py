# Tasks: Modernize the Full REG.Cloud CloudVPS Client

## 1. Contract and package baseline

- [x] 1.1 Commit a machine-readable endpoint manifest containing all 39 live v1 and 2 live v2 method/path pairs from the authoritative OpenAPI documents.
- [x] 1.2 Record the current public 0.1.7 constructor, resource accessors, method signatures, return behavior, and known undocumented endpoints in compatibility fixtures.
- [x] 1.3 Replace `setup.py`, `setup.cfg`, and the mixed `requirements.txt` flow with one Setuptools-backed `pyproject.toml` while keeping the package layout unchanged.
- [x] 1.4 Declare Python 3.11-3.14, the MIT license, current project URLs, classifiers, README content type, and Requests as the only runtime dependency.
- [x] 1.5 Make installed distribution metadata the single version source and expose it through `cloudvps.__version__`.
- [x] 1.6 Remove Python 2 compatibility imports, `future`, `nose`, universal Python 2 wheel configuration, and Travis CI.
- [x] 1.7 Build wheel and sdist from a clean copy, run metadata checks, inspect their file lists, install the wheel into a clean environment, and verify `from cloudvps import Api`.

## 2. Shared HTTP transport

- [x] 2.1 Add the public `CloudVpsAPIError` with safe status, provider code, provider message, and token-redacted string behavior.
- [x] 2.2 Refactor `Api` so token, headers, base URL, timeout, session, and resource containers are instance-owned.
- [x] 2.3 Implement one internal version-aware request path using session methods, query mappings, JSON bodies, and no manual Host header.
- [x] 2.4 Implement default/custom timeout behavior, JSON success handling, empty/204 handling, structured error parsing, and non-JSON error fallback.
- [x] 2.5 Preserve Requests transport failures as chained causes and install no implicit retry policy.
- [x] 2.6 Add session injection, `close()`, and context-manager lifecycle behavior with documented ownership semantics.
- [x] 2.7 Add an identifying package User-Agent without including account or token information.
- [x] 2.8 Add focused tests proving token isolation, token redaction, version routing, request composition, timeout behavior, response handling, lifecycle, and no automatic POST retry.

## 3. API v1 account and account-history resources

- [x] 3.1 Implement authenticated account feedback and feedback-hook POST operations with request-contract tests.
- [x] 3.2 Modernize SSH key list/create/rename/delete and preserve the `api.ssh` compatibility alias with tests.
- [x] 3.3 Implement account settings get/update for provider settings keys with tests.
- [x] 3.4 Restrict actions to documented single-action lookup, preserve valid compatibility behavior, and test the request/response contract.
- [x] 3.5 Implement balance data, billing history, and prices under a billing resource with tests.
- [x] 3.6 Modernize account operation-history listing and test response fidelity.

## 4. API v1 discovery and infrastructure resources

- [x] 4.1 Implement v1 image listing with `group`, `private`, `region`, and `type` filters plus tests.
- [x] 4.2 Implement additional IP list/create/delete and PTR update by concrete IP address plus tests for IPv4 and IPv6 paths.
- [x] 4.3 Implement Kubernetes kubeconfig retrieval without automatic filesystem writes and test the returned payload.
- [x] 4.4 Implement random server name, legacy sizes, and servers-for-snapshot discovery plus tests.
- [x] 4.5 Implement removed-server listing with response-fidelity tests.
- [x] 4.6 Implement snapshot list-by-region and delete-by-image-id plus tests.

## 5. API v1 server lifecycle and actions

- [x] 5.1 Implement server list with documented filters and single-server retrieval with tests.
- [x] 5.2 Implement server creation with all current `RegletCreate` fields, omitting unset optional values, and test representative minimal/full payloads.
- [x] 5.3 Implement server rename and delete with tests for JSON and empty success responses.
- [x] 5.4 Implement the generic documented server action operation and validate that it passes supported fields without adding `None` SSH keys.
- [x] 5.5 Implement and test start, stop, and reboot helpers.
- [x] 5.6 Implement and test rebuild, password reset, and resize helpers.
- [x] 5.7 Implement and test VNC-link generation and snapshot helpers, including optional name/offline fields.
- [x] 5.8 Implement and test backup enable, backup disable, and restore helpers.
- [x] 5.9 Implement and test clone and ISPmanager license resize helpers.
- [x] 5.10 Add a manifest-driven assertion that every current `RegletAction.type` has both generic coverage and a convenience helper.

## 6. API v1 private networks

- [x] 6.1 Implement VPC list, create, and single-resource get with tests.
- [x] 6.2 Implement VPC rename and documented delete, treating provider `501` as a normal `CloudVpsAPIError`, with tests.
- [x] 6.3 Implement VPC member list and attach with tests for action response variants.
- [x] 6.4 Implement VPC member detach and empty-success handling with tests.

## 7. API v2 regional catalogs

- [x] 7.1 Add the explicit `api.v2` namespace while preserving distinct v1 image access.
- [x] 7.2 Implement v2 image pages with required region/page/page-size and optional private/type filters plus tests.
- [x] 7.3 Implement v2 plan pages with all documented filters plus tests.
- [x] 7.4 Verify v2 response envelopes and pagination metadata are returned unchanged and no hidden next-page requests occur.
- [x] 7.5 Test forward-compatible region passthrough without a hard-coded client enum.

## 8. Compatibility and deprecation

- [x] 8.1 Wire `ssh`, `common`, `history`, `snapshots`, `images`, `actions`, and `vps` to their v1 implementations and run compatibility fixtures.
- [x] 8.2 Accept the legacy `provider` constructor argument, translate it to base URL form, and emit one actionable `DeprecationWarning`.
- [x] 8.3 Map every valid legacy method to a documented current operation without changing provider fields.
- [x] 8.4 Make undocumented legacy estimate, validate, action-list, history-item, image mutation/detail, snapshot mutation/detail, and server-PTR methods warn and fail locally without sending network requests.
- [x] 8.5 Document and test consistent `None` behavior for successful empty responses and all deliberate 0.1.7-to-0.2.0 behavior changes.
- [x] 8.6 Add a test that deprecated entry points remain importable for the 0.2 release line.

## 9. Quality automation and integration verification

- [x] 9.1 Organize offline tests by transport/resource domain using the standard library mock facilities or injected session doubles.
- [x] 9.2 Add a coverage check mapping each endpoint-manifest operation to at least one request-contract test.
- [x] 9.3 Configure Ruff for formatting and linting without adding runtime dependencies.
- [x] 9.4 Add pull-request/default-branch CI for Ruff, Python 3.11-3.14 tests, build, metadata validation, and wheel installation with read-only permissions.
- [x] 9.5 Add a read-only scheduled/manual OpenAPI drift workflow that prints added/removed method-path pairs and never writes repository state.
- [x] 9.6 Add Dependabot configuration for Python packaging inputs and GitHub Actions.
- [x] 9.7 Add an opt-in live integration suite using environment-only credentials and a separate full-mutating mode.
- [x] 9.8 Implement live-test resource tracking and best-effort cleanup so all created identifiers and cleanup outcomes are reported even after a failure.
- [x] 9.9 Run the read-only live smoke suite against v1 and v2 with a supplied token and record redacted results (2026-08-12: all 15 checks passed; no credential or account data recorded).
- [ ] 9.10 Run the authorized full live lifecycle suite with minimum temporary resources, verify every feasible mutating operation, clean up, and record costs/results without exposing the token.

## 10. User and maintainer documentation

- [x] 10.1 Rewrite the README quick start with current REG.Cloud links, Python support, environment-based authentication, timeout/error usage, and read-only v1/v2 examples.
- [x] 10.2 Add an explicit unofficial-project disclaimer and a Terraform-versus-Python usage section linking the official provider documentation.
- [x] 10.3 Add a complete API reference mapping every client operation to its provider method/path, parameters, return shape, and errors.
- [x] 10.4 Add clearly labeled server, IP, snapshot, and VPC mutation examples with immediate state/cost warnings.
- [x] 10.5 Add the 0.1.7-to-0.2.0 migration guide covering Python, constructor, namespaces, PTR, empty responses, and all deprecated calls.
- [x] 10.6 Add `CHANGELOG.md` with the 0.2.0 change set and release-note conventions.
- [x] 10.7 Add `SECURITY.md` with supported versions, private reporting, credential redaction, and response expectations.
- [x] 10.8 Add a maintainer release/recovery runbook and a concise contribution/testing guide.
- [x] 10.9 Verify README rendering and every documented code example in an isolated environment.

## 11. GitHub and PyPI supply-chain hardening

- [x] 11.1 Add a minimal release workflow triggered only by published GitHub Releases and validate `v<tag>` against package metadata before OIDC access.
- [x] 11.2 Separate build and publish jobs, pass one checked distribution artifact, and grant `id-token: write` only to the publish job.
- [x] 11.3 Pin checkout, Python setup, artifact transfer, and PyPA publish Actions to reviewed full commit SHAs with release-tag comments.
- [x] 11.4 Configure the GitHub `pypi` environment with release-tag restrictions, required review appropriate to available maintainers, and no-bypass protection where available.
- [x] 11.5 Register PyPI Trusted Publisher for the exact owner/repository, `release.yml`, and `pypi` environment.
- [ ] 11.6 Enable default-branch and `v*` tag rulesets: pull requests, required CI, force-push/delete prevention, and protected release-workflow ownership.
- [x] 11.7 Restrict allowed Actions, require full-SHA pins in repository settings, and enable secret scanning/push protection and dependency alerts where available.
- [x] 11.8 Confirm PyPI maintainer 2FA and recovery access, inventory existing publishers/tokens, and revoke legacy upload tokens after OIDC publication succeeds.

## 12. Release and OpenSpec completion

- [ ] 12.1 Build `0.2.0` release artifacts from the intended tag commit and compare hashes with the workflow artifact.
- [ ] 12.2 Publish and install a TestPyPI release candidate, run import/read-only smoke checks, and resolve packaging defects.
- [ ] 12.3 Publish the protected GitHub Release and approve the production environment deployment.
- [ ] 12.4 Verify PyPI wheel/sdist metadata, Trusted Publishing identity, attestations, hashes, and clean-environment installation.
- [ ] 12.5 Run post-release read-only CloudVPS smoke tests and verify all documentation/release links.
- [ ] 12.6 Sync the seven delta capability specs into `openspec/specs/`, archive the completed change, and retain the implementation/test/release evidence in the change history.
