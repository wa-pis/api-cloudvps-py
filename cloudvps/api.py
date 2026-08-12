import warnings
from urllib.parse import urlsplit

import requests

from . import resources


class CloudVpsAPIError(RuntimeError):
    """An HTTP error returned by the REG.Cloud CloudVPS API."""

    def __init__(self, status_code, code=None, message=None, response_text=None):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.response_text = response_text
        detail = message or response_text or "CloudVPS API request failed"
        prefix = f"CloudVPS API error {status_code}"
        if code:
            prefix += f" ({code})"
        super().__init__(f"{prefix}: {detail}")


class Api:
    """Synchronous client for REG.Cloud CloudVPS API v1 and v2."""

    def __init__(
        self,
        token,
        provider=None,
        *,
        base_url="https://api.cloudvps.reg.ru",
        timeout=30,
        session=None,
    ):
        if provider is not None:
            warnings.warn(
                "provider= is deprecated; use base_url='https://host' instead",
                DeprecationWarning,
                stacklevel=2,
            )
            base_url = provider if "://" in provider else f"https://{provider}"

        parsed = urlsplit(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("base_url must be an absolute HTTP(S) URL")
        if not token:
            raise ValueError("token must not be empty")

        self.token = token
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()
        self._owns_session = session is None
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": f"api-cloudvps-py/{resources.package_version()}",
        }

        self.v1 = resources.V1(self)
        self.v2 = resources.V2(self)

        # 0.1.x compatibility aliases. All current endpoints are API v1.
        self.ssh = self.v1.ssh_keys
        self.common = self.v1.common
        self.history = self.v1.history
        self.snapshots = self.v1.snapshots
        self.images = self.v1.images
        self.actions = self.v1.actions
        self.vps = self.v1.servers

    def _redact(self, value):
        return str(value).replace(self.token, "***") if value is not None else None

    def request(self, method, path, *, version="v1", params=None, json=None):
        """Send a versioned request and return decoded provider data."""
        url = f"{self.base_url}/{version}/{path.lstrip('/')}"
        response = self.session.request(
            method,
            url,
            headers=dict(self.headers),
            params=params or None,
            json=json,
            timeout=self.timeout,
        )
        if not 200 <= response.status_code < 300:
            try:
                payload = response.json()
            except (TypeError, ValueError):
                payload = {}
            code = payload.get("code") if isinstance(payload, dict) else None
            message = payload.get("message") if isinstance(payload, dict) else None
            text = self._redact(getattr(response, "text", ""))[:500]
            raise CloudVpsAPIError(
                response.status_code,
                self._redact(code),
                self._redact(message),
                text,
            )
        if response.status_code == 204 or not getattr(response, "content", b""):
            return None
        try:
            return response.json()
        except (TypeError, ValueError):
            return response.text

    # Low-level 0.1.x helpers remain v1-only.
    def get(self, path, object_id=None):
        del object_id
        return self.request("GET", path)

    def post(self, path, payload):
        return self.request("POST", path, json=payload)

    def put(self, path, payload):
        return self.request("PUT", path, json=payload)

    def delete(self, path):
        return self.request("DELETE", path)

    def close(self):
        """Close the internally created session.

        A caller-supplied session remains owned by the caller and is not closed.
        """
        if self._owns_session:
            self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False
