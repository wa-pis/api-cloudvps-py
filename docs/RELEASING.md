# Release runbook

1. Complete the OpenSpec tasks, offline CI, OpenAPI drift check, and authorized
   live verification. Confirm temporary resources were removed.
2. Set the unique version in `pyproject.toml`, update `CHANGELOG.md`, and run
   `python -m build && python -m twine check dist/*` from a clean checkout.
3. Verify PyPI Trusted Publisher matches owner `wa-pis`, repository
   `api-cloudvps-py`, workflow `release.yml`, and environment `pypi`.
4. Ensure the `pypi` environment permits only `v*` tags and has the available
   required-review/no-bypass protection. Confirm branch/tag rules and CI.
5. Run the manual `testpypi.yml` workflow from `master`; it builds, publishes
   through the `testpypi` Trusted Publisher, and installs the candidate in a clean
   environment. Do not reuse the TestPyPI build for a different version.
6. Create tag `vX.Y.Z` at the reviewed commit and publish the matching GitHub
   Release. Approve the `pypi` environment deployment after reviewing the build.
7. On PyPI, verify wheel/sdist, SHA-256 hashes, repository provenance, Trusted
   Publisher identity, attestations, and installation from a clean environment.
8. Run the post-release read-only CloudVPS smoke test and check documentation links.

## Recovery

- Reject the environment deployment to stop a release before upload.
- PyPI artifacts cannot be replaced. If an uploaded release is broken, yank it,
  document the reason, and publish a corrected patch version.
- Do not delete the GitHub Release or workflow logs; preserve the audit trail.
- If publishing identity is suspect, remove the PyPI Trusted Publisher, revoke
  remaining tokens, audit workflow changes and maintainers, then register the
  exact trusted workflow again.
