# Delta for CloudVPS API V1

## ADDED Requirements

### Requirement: V1 feedback operations

The v1 client SHALL expose both documented feedback POST operations with their
provider request bodies and response values.

#### Scenario: Send authenticated account feedback

- **GIVEN** a caller supplies the documented email and message fields
- **WHEN** account feedback is sent
- **THEN** the client sends `POST /v1/account/feedback` with that JSON body

#### Scenario: Send feedback hook payload

- **GIVEN** a caller supplies a feedback hook payload
- **WHEN** the hook operation is invoked
- **THEN** the client sends `POST /v1/feedback` with the payload

### Requirement: V1 SSH key lifecycle

The v1 client SHALL support listing, creating, renaming, and deleting SSH keys
using the current account key endpoints.

#### Scenario: SSH key CRUD paths

- **GIVEN** valid key input and a key identifier
- **WHEN** list, create, rename, and delete are invoked
- **THEN** the client uses `GET` and `POST /v1/account/keys`
- **AND** it uses `PUT` and `DELETE /v1/account/keys/{key_id}`
- **AND** create sends `name` and `public_key` while rename sends `name`

### Requirement: V1 account settings

The v1 client SHALL support reading and updating each settings key documented by
the provider without embedding account-specific values in client state.

#### Scenario: Read and update a settings key

- **GIVEN** a supported settings key and update payload
- **WHEN** get and update are invoked
- **THEN** the client sends `GET` and `PUT /v1/account/settings/{settings_key}`
- **AND** the PUT body matches the caller's payload

### Requirement: V1 action lookup

The v1 client SHALL retrieve a single asynchronous provider action by its
identifier.

#### Scenario: Retrieve action state

- **GIVEN** an action identifier
- **WHEN** action lookup is invoked
- **THEN** the client sends `GET /v1/actions/{action_id}`
- **AND** returns the provider action representation unchanged

### Requirement: V1 billing information

The v1 client SHALL expose account balance data, refill history, and the current
resource price list.

#### Scenario: Read all billing views

- **GIVEN** an authenticated client
- **WHEN** balance, billing history, and prices are requested
- **THEN** the client sends `GET /v1/balance_data`
- **AND** `GET /v1/billing_history`
- **AND** `GET /v1/prices`

### Requirement: V1 operation history

The v1 client SHALL list account operation history and preserve all provider
history fields.

#### Scenario: List operation history

- **GIVEN** an authenticated client
- **WHEN** history is requested
- **THEN** the client sends `GET /v1/history`
- **AND** returns the decoded provider response without field renaming

### Requirement: V1 image discovery

The v1 client SHALL list images with the documented `group`, `private`, `region`,
and `type` filters when supplied.

#### Scenario: Filter image list

- **GIVEN** any supported combination of image filters
- **WHEN** images are listed
- **THEN** the client sends `GET /v1/images`
- **AND** includes only supplied filters as query parameters

### Requirement: V1 additional IP lifecycle and PTR

The v1 client SHALL list and create additional IP addresses, delete an address,
and change an address's PTR through the current IP endpoints.

#### Scenario: List and create IP addresses

- **GIVEN** a server identifier and at least one requested IPv4 or IPv6 count
- **WHEN** IP list and create are invoked
- **THEN** the client sends `GET /v1/ips` with supported filters
- **AND** sends `POST /v1/ips` with the requested counts and server identifier

#### Scenario: Update and delete a concrete IP address

- **GIVEN** an IP address and a valid PTR value
- **WHEN** PTR update and delete are invoked
- **THEN** the client sends `PUT /v1/ips/{ip}` with `ptr`
- **AND** sends `DELETE /v1/ips/{ip}`

### Requirement: V1 Kubernetes kubeconfig retrieval

The v1 client SHALL retrieve kubeconfig for a documented Kubernetes cluster
identifier without writing it to disk automatically.

#### Scenario: Retrieve kubeconfig

- **GIVEN** a Kubernetes cluster identifier
- **WHEN** kubeconfig is requested
- **THEN** the client sends `GET /v1/k8s_clusters/{k8s_cluster_id}/get_kubeconfig`
- **AND** returns the provider response to the caller

### Requirement: V1 common discovery operations

The v1 client SHALL expose random server-name generation, legacy size discovery,
and eligible server identifiers for a snapshot.

#### Scenario: Invoke common discovery calls

- **GIVEN** an authenticated client and a snapshot identifier
- **WHEN** the three common operations are invoked
- **THEN** the client sends `GET /v1/random_reglet_name`
- **AND** `GET /v1/sizes`
- **AND** `GET /v1/reglets_for_snapshot/{snapshot_id}`

### Requirement: V1 server lifecycle

The v1 client SHALL support listing, creating, retrieving, renaming, and deleting
servers through the documented reglet endpoints.

#### Scenario: List and retrieve servers

- **GIVEN** optional list filters and a server identifier
- **WHEN** server list and get are invoked
- **THEN** the client sends `GET /v1/reglets` with supplied filters
- **AND** `GET /v1/reglets/{resource_id}`

#### Scenario: Create, rename, and delete a server

- **GIVEN** a documented server-create payload and a server identifier
- **WHEN** create, rename, and delete are invoked
- **THEN** the client sends `POST /v1/reglets` with all supplied documented fields
- **AND** sends `PUT /v1/reglets/{resource_id}` with `name`
- **AND** sends `DELETE /v1/reglets/{resource_id}`

### Requirement: Complete V1 server action coverage

The v1 client SHALL provide a generic server action operation and convenience
operations for every action type in the current `RegletAction` schema: `start`,
`stop`, `reboot`, `rebuild`, `password_reset`, `resize`, `generate_vnc_link`,
`snapshot`, `enable_backups`, `disable_backups`, `restore`, `clone`, and
`resize_isp_license`.

#### Scenario: Invoke any documented server action

- **GIVEN** a server identifier, one documented action type, and its applicable fields
- **WHEN** the generic action or matching convenience operation is invoked
- **THEN** the client sends `POST /v1/reglets/{resource_id}/actions`
- **AND** the JSON body contains the exact action type and supplied applicable fields
- **AND** optional SSH keys never become a list containing `None`

### Requirement: V1 removed server history

The v1 client SHALL list removed servers using the provider's removed-server
representation.

#### Scenario: List removed servers

- **GIVEN** an authenticated client
- **WHEN** removed servers are requested
- **THEN** the client sends `GET /v1/removed_servers`

### Requirement: V1 snapshot lifecycle

The v1 client SHALL list snapshots by optional region and delete a snapshot by
image identifier. Snapshot creation SHALL use the documented server action.

#### Scenario: List and delete snapshots

- **GIVEN** an optional region and snapshot image identifier
- **WHEN** list and delete are invoked
- **THEN** the client sends `GET /v1/snapshots` with the supplied region
- **AND** sends `DELETE /v1/snapshots/{image_id}`

#### Scenario: Create snapshot from a server

- **GIVEN** a server identifier and optional snapshot name/offline mode
- **WHEN** snapshot creation is invoked
- **THEN** the client sends the `snapshot` action to the documented server action endpoint

### Requirement: Complete V1 private network lifecycle

The v1 client SHALL support VPC list, create, get, rename, delete, member list,
member attach, and member detach operations even when a documented provider
operation currently responds with `501 Not Implemented`.

#### Scenario: VPC CRUD paths

- **GIVEN** a VPC name and identifier
- **WHEN** list, create, get, rename, and delete are invoked
- **THEN** the client uses `GET` and `POST /v1/vpcs`
- **AND** uses `GET`, `PUT`, and `DELETE /v1/vpcs/{vpcs_id}`
- **AND** a provider `501` is surfaced as `CloudVpsAPIError`

#### Scenario: Manage VPC members

- **GIVEN** a VPC identifier and server resource identifier
- **WHEN** members are listed, attached, and detached
- **THEN** the client sends `GET` and `POST /v1/vpcs/{vpcs_id}/members`
- **AND** sends `DELETE /v1/vpcs/{vpcs_id}/members/{resource_id}`
