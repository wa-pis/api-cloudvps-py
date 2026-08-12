# Delta for Client Transport

## ADDED Requirements

### Requirement: Client instance isolation

Each client instance SHALL own its authentication state and SHALL NOT mutate
headers, tokens, sessions, base URLs, or timeouts belonging to another instance.

#### Scenario: Two accounts in one process

- **GIVEN** two clients constructed with different bearer tokens
- **WHEN** each client sends a request
- **THEN** each request contains only its own token
- **AND** constructing either client does not change the other's headers

### Requirement: Secure bearer authentication

The client SHALL authenticate protected requests with the configured bearer
token and MUST prevent that token from appearing in object representations,
exceptions, warnings, test diagnostics, or normal logs.

#### Scenario: API error does not disclose token

- **GIVEN** a client configured with a bearer token
- **WHEN** the provider returns a non-success response
- **THEN** the raised error contains safe status and provider error details
- **AND** the token and complete Authorization header are absent

### Requirement: Versioned request routing

The client SHALL compose v1 and v2 URLs from one configurable base URL without
requiring the caller to include an API version in that base URL.

#### Scenario: V1 and V2 resources share a provider host

- **GIVEN** a client configured with `https://api.cloudvps.reg.ru`
- **WHEN** a v1 sizes call and a v2 plans call are made
- **THEN** their URLs begin with `/v1` and `/v2` respectively
- **AND** neither URL duplicates a version segment

### Requirement: Finite configurable timeout

Every HTTP request SHALL use a finite timeout, defaulting to 30 seconds, and the
caller SHALL be able to provide a Requests-compatible scalar or connect/read
timeout tuple.

#### Scenario: Default timeout

- **GIVEN** a client created without an explicit timeout
- **WHEN** it sends any provider request
- **THEN** the transport passes a 30-second timeout to Requests

#### Scenario: Caller supplied timeout

- **GIVEN** a client configured with a connect/read timeout tuple
- **WHEN** it sends a provider request
- **THEN** the exact tuple is passed to Requests

### Requirement: Structured request composition

The client SHALL send query parameters through the HTTP client's parameter
mapping, JSON bodies through its JSON argument, and SHALL NOT set a manual
`Host` header.

#### Scenario: Filtered collection request

- **GIVEN** a resource collection call with filters
- **WHEN** the request is composed
- **THEN** filters are present in the params mapping
- **AND** the URL contains only the resource path
- **AND** the headers do not include a manually constructed Host value

### Requirement: Consistent success responses

The transport SHALL return decoded provider JSON for successful responses with
a body and SHALL return `None` for a successful `204` or empty response.

#### Scenario: JSON success

- **GIVEN** the provider returns a JSON object with a successful status
- **WHEN** the transport handles the response
- **THEN** it returns the decoded Python value

#### Scenario: Empty deletion success

- **GIVEN** the provider returns `204 No Content`
- **WHEN** the transport handles the response
- **THEN** it returns `None`

### Requirement: Consistent provider errors

The transport SHALL raise `CloudVpsAPIError` for non-success HTTP responses and
SHALL expose the HTTP status, provider code, and provider message when present.
Malformed or non-JSON error bodies MUST still produce a safe actionable error.

#### Scenario: Structured provider error

- **GIVEN** the provider returns status 400 with `code` and `message`
- **WHEN** the transport handles the response
- **THEN** `CloudVpsAPIError` exposes those fields and the status

#### Scenario: Non-JSON provider error

- **GIVEN** the provider returns an HTML or empty error response
- **WHEN** the transport handles the response
- **THEN** `CloudVpsAPIError` is raised without a JSON decoding exception hiding the status

### Requirement: Session lifecycle

The client SHALL reuse one Requests session, SHALL offer an explicit `close()`
operation, and SHALL support use as a context manager.

#### Scenario: Context manager closes resources

- **GIVEN** a client used in a `with` block
- **WHEN** execution leaves the block
- **THEN** the session is closed exactly once

### Requirement: No unsafe implicit retries

The client SHALL NOT retry requests automatically unless a caller explicitly
configures retry behavior on a supplied session.

#### Scenario: Mutating request fails during transport

- **GIVEN** a POST request encounters a connection failure
- **WHEN** no custom retry session was supplied
- **THEN** the transport performs no second POST attempt
- **AND** the original Requests exception remains available as the cause
