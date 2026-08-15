# Delta for Secure Release

## ADDED Requirements

### Requirement: Release only from an approved version tag

Production publishing SHALL run only for a published GitHub Release whose tag
matches `v<project-version>` and whose commit passed required CI checks.

#### Scenario: Tag and package version disagree

- **GIVEN** a published release tag does not match package metadata
- **WHEN** the release workflow validates inputs
- **THEN** it fails before building or requesting an OIDC token

### Requirement: Build once and publish exact artifacts

The release workflow SHALL build wheel and source distribution once in a
non-publishing job, validate them, and pass exactly those artifacts to the
publishing job.

#### Scenario: Publish job starts

- **GIVEN** the build job completed successfully
- **WHEN** the publish job downloads release artifacts
- **THEN** it publishes the same checked wheel and source distribution
- **AND** does not rebuild from source

### Requirement: PyPI Trusted Publishing

Production publication SHALL use PyPI Trusted Publishing with GitHub OIDC and
MUST NOT depend on a stored PyPI password or API token.

#### Scenario: PyPI authentication

- **GIVEN** the registered repository, workflow filename, and `pypi` environment match
- **WHEN** the publish action authenticates
- **THEN** PyPI mints a short-lived credential from the workflow OIDC identity
- **AND** no long-lived upload credential exists in repository secrets

### Requirement: Least-privilege workflow permissions

Workflow and job permissions SHALL be explicitly declared. Only the production
publish job SHALL receive `id-token: write`; build and CI jobs SHALL use read-only
repository contents permissions.

#### Scenario: Build dependency is compromised

- **GIVEN** code runs in the build job
- **WHEN** it inspects its GitHub token permissions
- **THEN** it cannot request the PyPI OIDC identity
- **AND** it cannot write repository contents

### Requirement: Protected production environment

The publish job SHALL target a GitHub environment named `pypi` restricted to
release tags and protected by the strongest practical reviewer and no-bypass
rules for the maintainer configuration.

#### Scenario: Unapproved production deployment

- **GIVEN** a workflow reaches the production publish job
- **WHEN** environment protection has not passed
- **THEN** the job cannot request its publishing identity or upload artifacts

### Requirement: Immutable Action dependencies

Every external GitHub Action SHALL be pinned to a full commit SHA, with its
reviewed release tag recorded in a same-line comment.

#### Scenario: Upstream moves a release tag

- **GIVEN** an Action's upstream tag is changed
- **WHEN** an existing workflow runs
- **THEN** it still executes the previously reviewed commit SHA

### Requirement: PyPI publish attestations

Release artifacts SHALL be uploaded with the publish attestations produced by
the official PyPA publishing action and Trusted Publisher identity.

#### Scenario: Inspect published artifact provenance

- **GIVEN** a successful production release
- **WHEN** its wheel or source distribution is viewed on PyPI
- **THEN** PyPI shows provenance tied to the repository, workflow, tag commit, and OIDC publisher

### Requirement: Protected source and release references

The default branch and `v*` release tags SHALL be protected against force push,
deletion, and unreviewed changes, and required CI SHALL pass before release
source is accepted.

#### Scenario: Direct unreviewed release-source change

- **GIVEN** a contributor attempts to bypass pull-request and status rules
- **WHEN** they update the protected branch or release tag
- **THEN** GitHub rejects the update unless an explicitly documented emergency bypass applies

### Requirement: Recoverable broken release procedure

Maintainer documentation SHALL define how to stop a pending publication, yank a
broken immutable PyPI release, publish a corrected patch version, and preserve
the related GitHub audit trail.

#### Scenario: Defect found after upload

- **GIVEN** a production release is broken after PyPI accepts it
- **WHEN** maintainers follow the recovery procedure
- **THEN** the release is yanked rather than replaced
- **AND** a new patch version carries the correction
