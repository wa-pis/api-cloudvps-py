# Delta for Project Documentation

## ADDED Requirements

### Requirement: Current project identity and support policy

The README SHALL identify the package as an unofficial REG.Cloud CloudVPS client,
link to the live v1/v2 provider documentation, and state supported Python and
package versions.

#### Scenario: New user evaluates the package

- **GIVEN** a user opens the repository or PyPI description
- **WHEN** they read the introductory section
- **THEN** they can distinguish the package from an official REG.Cloud product
- **AND** can find the provider API contracts and compatibility policy

### Requirement: Secure installation and authentication guidance

Documentation SHALL show modern pip installation and environment-based token
handling without placing a real token in source code, command history examples,
or committed configuration.

#### Scenario: Follow authentication example

- **GIVEN** a user follows the quick start
- **WHEN** they create the client
- **THEN** the token is obtained from an environment variable
- **AND** examples contain only unmistakably fake placeholders

### Requirement: Complete public API reference

Every public v1 and v2 resource operation, its required and optional parameters,
return shape, empty-success behavior, and relevant errors SHALL be documented.

#### Scenario: Locate an endpoint wrapper

- **GIVEN** any operation in the committed v1/v2 endpoint manifest
- **WHEN** a user searches the API reference
- **THEN** the matching client method and provider path are documented

### Requirement: Safe usage examples

Documentation SHALL provide working read-only examples for common discovery and
separately labeled destructive examples for creation, mutation, and deletion.

#### Scenario: User copies a read-only example

- **GIVEN** the quick start example
- **WHEN** it is executed with a valid token
- **THEN** it performs only documented read operations

#### Scenario: User reads a mutating example

- **GIVEN** an example that creates or deletes a paid resource
- **WHEN** it is displayed
- **THEN** its state and cost impact is called out immediately before the code

### Requirement: Migration guide

The project SHALL document migration from 0.1.7 to 0.2.0, including Python
support, constructor changes, response semantics, version namespaces, fixed PTR
usage, and every deprecated or removed provider endpoint.

#### Scenario: Existing caller upgrades

- **GIVEN** an application using 0.1.7
- **WHEN** its maintainer reads the migration guide
- **THEN** they can map every changed public call to its replacement or documented failure behavior

### Requirement: Changelog and release notes

The project SHALL maintain a human-readable changelog and each release SHALL
describe added operations, fixes, compatibility changes, and security/release
changes.

#### Scenario: Review 0.2.0 impact

- **GIVEN** the 0.2.0 release notes
- **WHEN** a user evaluates the upgrade
- **THEN** all behavior changes and new API domains are discoverable without reading commits

### Requirement: Security reporting guidance

The repository SHALL include a security policy describing supported versions,
private reporting instructions, credential-handling expectations, and what data
must be redacted from reports.

#### Scenario: Reporter finds a token-handling issue

- **GIVEN** a researcher discovers a potential credential leak
- **WHEN** they open the security policy
- **THEN** they find a private reporting path
- **AND** are instructed not to include live bearer tokens

### Requirement: Terraform positioning

Documentation SHALL explain when to use the official REG.Cloud Terraform
provider and when the Python client is appropriate, without claiming that this
package replaces Terraform.

#### Scenario: Infrastructure automation choice

- **GIVEN** a user wants declarative server, SSH-key, or snapshot management
- **WHEN** they read the comparison
- **THEN** they are directed to consider the official Terraform provider
- **AND** Python usage is positioned for imperative workflows and broader API operations

### Requirement: Maintainer release runbook

The repository SHALL document the exact version, CI, GitHub Release, environment
approval, PyPI verification, smoke-test, and rollback sequence.

#### Scenario: Maintainer publishes a release

- **GIVEN** a release candidate passed CI and integration verification
- **WHEN** the maintainer follows the runbook
- **THEN** the tag, package metadata, GitHub Release, and PyPI version match
- **AND** provenance and installation smoke checks are completed
