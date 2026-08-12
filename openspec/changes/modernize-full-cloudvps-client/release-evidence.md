# 0.2.0 release evidence

Date: 2026-08-12

## Source and protected release

- Tag: `v0.2.0`
- Tag commit: `8e8dcf587e0cc6a2f2025bbafe69b0a5bd21b652`
- GitHub Release: <https://github.com/wa-pis/api-cloudvps-py/releases/tag/v0.2.0>
- Release workflow: <https://github.com/wa-pis/api-cloudvps-py/actions/runs/31632528600>
- Workflow result: successful (`build`, approved `pypi` deployment, `publish`, and `verify`)
- Workflow artifact: `python-distributions`
- Workflow artifact SHA-256: `43c2809528df6a4833d3fb41064b6e95e4833d13e36b8b0e74119b06a7b74ee8`

## Distribution identity

The downloaded workflow artifact contained exactly the two files published by
PyPI. Their SHA-256 hashes matched PyPI's release JSON and their metadata passed
`twine check`:

| File | SHA-256 |
| --- | --- |
| `api_cloudvps_py-0.2.0-py3-none-any.whl` | `e39014a11fe8ddb2a8264761a07a05b92bb0c3d6cd928bbf7ef60715fd5295cf` |
| `api_cloudvps_py-0.2.0.tar.gz` | `5ceb6a3239c3ecb133b29415a9c20df52b3e467640909eeb27db13850caf7ff9` |

PyPI release: <https://pypi.org/project/api-cloudvps-py/0.2.0/>

## Trusted Publishing and attestations

PyPI's Integrity API returned a publish attestation for both files. Each
attestation identifies:

- publisher kind: `GitHub`
- repository: `wa-pis/api-cloudvps-py`
- workflow: `release.yml`
- environment: `pypi`
- ref: `refs/tags/v0.2.0`
- commit: `8e8dcf587e0cc6a2f2025bbafe69b0a5bd21b652`

Integrity API:

- <https://pypi.org/integrity/api-cloudvps-py/0.2.0/api_cloudvps_py-0.2.0-py3-none-any.whl/provenance>
- <https://pypi.org/integrity/api-cloudvps-py/0.2.0/api_cloudvps_py-0.2.0.tar.gz/provenance>

## Installation verification

The release workflow installed `api-cloudvps-py==0.2.0` from the production
PyPI index on Python 3.14 and imported `cloudvps.Api`. An independent clean
Python 3.11 virtual environment repeated the production-index installation and
confirmed:

```text
0.2.0
cloudvps.api.Api
```

The post-release authenticated CloudVPS smoke test and final OpenSpec archival
remain tracked by tasks 12.4 and 12.5.
