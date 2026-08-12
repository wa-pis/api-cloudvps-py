# Design: Modernize the Full REG.Cloud CloudVPS Client

## Context

The existing package is a small synchronous wrapper around `requests` with one
resource object per file. The modernization keeps that recognizable model while
moving shared HTTP behavior into one correct transport path and making API
versions explicit. The live contracts are:

- `https://api.cloudvps.reg.ru/v1/openapi.json`
- `https://api.cloudvps.reg.ru/v2/api/swagger.json`

The implementation is handwritten because the contracts are small (39 v1
operations and 2 v2 operations), the public package already has a handwritten
API, and generated code would create a much larger compatibility surface.

## Goals

- Cover every operation in the current v1 and v2 CloudVPS schemas.
- Fix token isolation and give all HTTP operations one reliable behavior.
- Preserve familiar imports and resource-oriented calls.
- Make endpoint drift detectable through tests and a scheduled read-only check.
- Publish reproducible wheel and source artifacts without stored PyPI secrets.

## Non-goals

- Models beyond dictionaries/lists returned by the provider.
- Async transport, caching, or automatic polling of asynchronous actions.
- Automatic retries of POST, PUT, or DELETE operations.
- A general REG.Cloud SDK outside the CloudVPS contracts.

## Architecture

`Api` owns one `requests.Session`, immutable instance headers, base URL, and
timeout configuration. All resource objects delegate to a single internal
request method. That method builds a versioned URL, sends the request, checks
the status, and either returns decoded JSON, returns `None` for an empty success,
or raises one public API error containing safe diagnostic fields.

The public surface is organized as follows:

```text
Api
├── v1
│   ├── feedback, ssh_keys, settings, actions, billing, history
│   ├── images, ips, kubernetes, common, servers, removed_servers
│   ├── snapshots, and vpcs
│   └── resources expose the documented v1 operations
├── v2
│   ├── images
│   └── plans
└── compatibility aliases
    ├── ssh -> v1.ssh_keys
    ├── common -> v1.common
    ├── history -> v1.history
    ├── snapshots -> v1.snapshots
    ├── images -> v1.images
    ├── actions -> v1.actions
    └── vps -> v1.servers
```

The exact internal namespace/container implementation may remain small, but the
observable versioned and compatibility surfaces are required.

## HTTP behavior

- Constructor shape: token, base URL, timeout, and optional prepared session.
- Default base URL: `https://api.cloudvps.reg.ru`.
- Default timeout: 30 seconds; callers may provide a Requests-compatible scalar
  or connect/read tuple.
- Authentication: an instance-owned `Authorization: Bearer ...` header.
- Requests use JSON bodies and `params` query mappings; no manual `Host` header.
- Success with JSON returns decoded values; `204` or an empty success returns
  `None`.
- Non-success responses raise `CloudVpsAPIError` with status, provider code,
  provider message, and safe response context. The token and Authorization
  header are never retained in the exception string.
- Network exceptions from `requests` remain chained so callers retain the
  original cause.
- `close()` and context-manager methods close only the owned/provided session in
  a documented manner.
- No retry adapter is installed by default.

## API versioning

Resource paths include `/v1` or `/v2`; the base URL never embeds a version. API
v1 and v2 responses are not normalized into shared models. Versioned methods
expose the provider's current request parameters and response envelopes.

V2 collection methods require `region`, `page`, and `items_per_page` and expose
all provider filters. They return the provider envelope including `metadata` so
callers control pagination. No hidden all-pages request loop is added.

## API v1 operation inventory

The implementation and its endpoint manifest cover these live operations:

| Domain | Operations |
| --- | --- |
| Feedback | `POST /account/feedback`, `POST /feedback` |
| SSH keys | `GET/POST /account/keys`, `PUT/DELETE /account/keys/{key_id}` |
| Settings | `GET/PUT /account/settings/{settings_key}` |
| Actions | `GET /actions/{action_id}` |
| Billing | `GET /balance_data`, `GET /billing_history`, `GET /prices` |
| History | `GET /history` |
| Images | `GET /images` |
| IPs | `GET/POST /ips`, `PUT/DELETE /ips/{ip}` |
| Kubernetes | `GET /k8s_clusters/{k8s_cluster_id}/get_kubeconfig` |
| Common | `GET /random_reglet_name`, `GET /sizes`, `GET /reglets_for_snapshot/{snapshot_id}` |
| Servers | `GET/POST /reglets`, `GET/PUT/DELETE /reglets/{resource_id}` |
| Server actions | `POST /reglets/{resource_id}/actions` |
| Removed servers | `GET /removed_servers` |
| Snapshots | `GET /snapshots`, `DELETE /snapshots/{image_id}` |
| VPCs | `GET/POST /vpcs`, `GET/PUT/DELETE /vpcs/{vpcs_id}`, member list/attach/detach |

Server action helpers cover every current `RegletAction.type`: `start`, `stop`,
`reboot`, `rebuild`, `password_reset`, `resize`, `generate_vnc_link`, `snapshot`,
`enable_backups`, `disable_backups`, `restore`, `clone`, and
`resize_isp_license`. A generic action method remains available for forward
compatibility.

## API v2 operation inventory

- `GET /v2/images` with `region`, `page`, `items_per_page`, `private`, and `type`.
- `GET /v2/plans` with `region`, `page`, `items_per_page`, `vcpus`, `disk`,
  `memory`, `plan_line`, and `unit`.

## Compatibility strategy

- `Api(token, provider=...)` continues for one release cycle; `provider` is
  translated to a base URL and emits `DeprecationWarning`.
- Current resource aliases remain available and delegate to v1 resources.
- Existing methods with valid equivalents delegate to the new implementation.
- Undocumented legacy methods (`estimate`, `validate`, action-list/history-item
  accessors, image/snapshot rename/get operations, and server-based PTR) warn and
  fail locally with the replacement where one exists. They never send a request
  to an endpoint absent from the live schema.
- Version metadata has one source in `pyproject.toml`; `cloudvps.__version__`
  reads installed distribution metadata.

## Packaging and quality

Use the existing Setuptools backend through `pyproject.toml`; do not migrate to
another packaging framework or move to a `src/` layout during this change.
Runtime dependencies contain only a maintained Requests version. Development
tools are isolated from runtime metadata.

Offline tests patch or inject the session and assert method, versioned URL,
headers, params, JSON, timeout, response behavior, and token redaction. Every
operation in the endpoint manifest has a request-contract test. A scheduled
read-only workflow compares the live method/path inventory with that manifest;
it does not change source or open issues automatically.

## Release design

CI builds and tests pull requests and the default branch with read-only token
permissions. A production workflow is triggered by a published GitHub Release
whose tag and project version match. Its build job creates wheel and sdist once,
checks them, and uploads one artifact. A separate publish job downloads exactly
that artifact, enters the protected `pypi` environment, receives only
`id-token: write`, and invokes the PyPA publishing action through a full commit
SHA. PyPI Trusted Publishing mints the short-lived credential and produces the
default publish attestations.

## Operational decisions

- Official OpenAPI is the source for endpoints; human documentation supplies
  usage explanations but cannot silently add undocumented calls.
- A provider endpoint may be exposed generically before a convenience helper,
  but the change is incomplete until every listed helper and contract test is
  present.
- Known provider `501 Not Implemented` responses, such as a currently
  unavailable VPC deletion backend, are represented as normal API errors; the
  client still exposes the documented operation.
- Destructive examples are clearly marked and never executed in CI.
