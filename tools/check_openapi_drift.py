#!/usr/bin/env python3
"""Compare the committed endpoint manifest with live REG.Cloud OpenAPI schemas."""

import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen

SCHEMAS = {
    "v1": "https://api.cloudvps.reg.ru/v1/openapi.json",
    "v2": "https://api.cloudvps.reg.ru/v2/api/swagger.json",
}
METHODS = {"GET", "POST", "PUT", "DELETE", "PATCH"}


def load_json(url):
    request = Request(url, headers={"User-Agent": "api-cloudvps-py-openapi-drift/0.2"})
    with urlopen(request, timeout=30) as response:  # noqa: S310 - fixed HTTPS URLs
        return json.load(response)


def inventory(version, schema):
    operations = set()
    for path, path_item in schema["paths"].items():
        if version == "v2" and path.startswith("/v2/"):
            path = path[3:]
        for method in path_item:
            upper = method.upper()
            if upper in METHODS:
                operations.add((upper, path))
    return operations


def main():
    manifest_path = Path(__file__).parents[1] / "cloudvps" / "endpoints.json"
    manifest = json.loads(manifest_path.read_text())
    failed = False
    for version, url in SCHEMAS.items():
        expected = {tuple(operation) for operation in manifest[version]}
        actual = inventory(version, load_json(url))
        added, removed = sorted(actual - expected), sorted(expected - actual)
        if added or removed:
            failed = True
            print(f"{version} OpenAPI drift detected")
            for operation in added:
                print("  added:  ", *operation)
            for operation in removed:
                print("  removed:", *operation)
        else:
            print(f"{version}: {len(actual)} operations match")
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
