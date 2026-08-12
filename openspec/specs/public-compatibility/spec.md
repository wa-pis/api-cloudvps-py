# Delta for Public Compatibility

## ADDED Requirements

### Requirement: Distribution and import identity

The modernized release SHALL retain the `api-cloudvps-py` distribution name and
the `cloudvps` import namespace.

#### Scenario: Existing import continues to work

- **GIVEN** version 0.2.0 is installed from its wheel
- **WHEN** user code executes `from cloudvps import Api`
- **THEN** the public client class imports successfully

### Requirement: Existing V1 resource aliases

The `ssh`, `common`, `history`, `snapshots`, `images`, `actions`, and `vps`
accessors SHALL remain available as aliases for their documented v1 resources.

#### Scenario: Existing resource-oriented code

- **GIVEN** code written against a valid 0.1.7 resource accessor
- **WHEN** that accessor invokes an operation still present in v1 OpenAPI
- **THEN** it delegates to the versioned v1 implementation
- **AND** produces the same provider request as the explicit v1 resource

### Requirement: Legacy provider constructor argument

The legacy `provider` constructor argument SHALL remain accepted during the 0.2
release line, SHALL map to the modern base URL configuration, and SHALL emit a
`DeprecationWarning` with the replacement syntax.

#### Scenario: Construct with provider host

- **GIVEN** user code passes `provider="api.cloudvps.reg.ru"`
- **WHEN** the client is constructed
- **THEN** requests use `https://api.cloudvps.reg.ru`
- **AND** one actionable deprecation warning is emitted

### Requirement: Undocumented legacy methods fail locally

Legacy methods whose endpoints are absent from the live v1/v2 OpenAPI contracts
MUST NOT issue undocumented network calls. They SHALL warn and fail locally with
migration guidance, or delegate to a documented equivalent only when the mapping
is unambiguous.

#### Scenario: Server-based legacy PTR method

- **GIVEN** user code invokes the legacy server-id PTR method
- **WHEN** the client cannot unambiguously choose a concrete IP address
- **THEN** no provider request is sent
- **AND** the error points to the IP-address PTR operation

#### Scenario: Removed endpoint without replacement

- **GIVEN** user code invokes a legacy method for `/estimate` or `/validate`
- **WHEN** the method is evaluated
- **THEN** no provider request is sent
- **AND** an actionable deprecation message explains that the endpoint is absent

### Requirement: Provider response fidelity

Public resource operations SHALL return decoded dictionaries, lists, scalars, or
`None` without renaming provider fields or requiring generated model classes.

#### Scenario: Provider adds a response field

- **GIVEN** a successful JSON response containing a field unknown to the client
- **WHEN** the resource method returns
- **THEN** the unknown field remains available to the caller

### Requirement: One package version source

The package SHALL define its release version once and SHALL expose the installed
version through `cloudvps.__version__`.

#### Scenario: Inspect installed version

- **GIVEN** the 0.2.0 wheel is installed
- **WHEN** the caller reads `cloudvps.__version__`
- **THEN** it equals the wheel's distribution metadata version

### Requirement: Deprecation removal boundary

Entry points deprecated by 0.2.x SHALL remain present throughout the 0.2 release
line and MAY be removed only in 1.0.0 or later with release-note documentation.

#### Scenario: Patch release compatibility

- **GIVEN** a method is deprecated in 0.2.0
- **WHEN** a later 0.2.x release is installed
- **THEN** the method remains importable and emits its documented warning/error behavior
