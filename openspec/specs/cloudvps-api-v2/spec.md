# Delta for CloudVPS API V2

## ADDED Requirements

### Requirement: Explicit V2 resource namespace

The client SHALL expose API v2 resources through an explicit v2 namespace so
that v1 and v2 image behavior cannot be confused.

#### Scenario: Access V2 plans and images

- **GIVEN** a configured client
- **WHEN** the caller accesses the v2 namespace
- **THEN** image and plan collection operations are available
- **AND** their requests use `/v2` paths
- **AND** existing v1 image access remains distinct

### Requirement: V2 regional image discovery

The v2 client SHALL list images through `GET /v2/images`, requiring `region`,
`page`, and `items_per_page`, and accepting the optional `private` and `type`
filters documented by the provider.

#### Scenario: Request a filtered image page

- **GIVEN** a region, page, page size, private flag, and image type
- **WHEN** v2 images are requested
- **THEN** the client sends `GET /v2/images`
- **AND** all supplied values are sent as query parameters
- **AND** the decoded response includes the provider `images` and `metadata` envelope

### Requirement: V2 regional plan discovery

The v2 client SHALL list plans through `GET /v2/plans`, requiring `region`,
`page`, and `items_per_page`, and accepting optional `vcpus`, `disk`, `memory`,
`plan_line`, and `unit` filters.

#### Scenario: Request a filtered plan page

- **GIVEN** required pagination and any documented plan filters
- **WHEN** v2 plans are requested
- **THEN** the client sends `GET /v2/plans`
- **AND** only supplied filters are sent as query parameters
- **AND** the decoded response includes the provider `plans` and `metadata` envelope

### Requirement: Provider-controlled pagination

The v2 client SHALL preserve provider pagination metadata and SHALL NOT fetch
additional pages implicitly.

#### Scenario: Multiple result pages exist

- **GIVEN** the provider returns metadata indicating more pages
- **WHEN** one collection request completes
- **THEN** the client returns only that response page and its metadata
- **AND** sends no request for the next page

### Requirement: Forward-compatible region values

The client SHALL pass non-empty region slugs to the provider without enforcing a
hard-coded region enum that would reject newly added provider regions.

#### Scenario: Provider introduces a new region

- **GIVEN** a non-empty region slug not known at package release time
- **WHEN** the caller requests v2 images or plans
- **THEN** the client sends the slug unchanged
- **AND** the provider remains responsible for accepting or rejecting it
