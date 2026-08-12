import unittest
import warnings
from unittest.mock import Mock, patch

import requests

from cloudvps import Api, CloudVpsAPIError

from .helpers import FakeResponse, FakeSession


class TransportTests(unittest.TestCase):
    def test_clients_do_not_share_headers(self):
        first_session = FakeSession()
        second_session = FakeSession()
        first = Api("token-one", session=first_session)
        second = Api("token-two", session=second_session)

        first.common.sizes()
        second.common.sizes()

        self.assertIsNot(first.headers, second.headers)
        self.assertEqual(first_session.calls[0][2]["headers"]["Authorization"], "Bearer token-one")
        self.assertEqual(second_session.calls[0][2]["headers"]["Authorization"], "Bearer token-two")

    def test_default_and_custom_timeout_and_version_routing(self):
        default_session = FakeSession()
        custom_session = FakeSession()
        Api("x", session=default_session).common.sizes()
        Api("y", timeout=(2, 8), session=custom_session).v2.plans.list("future-region")

        self.assertEqual(default_session.calls[0][2]["timeout"], 30)
        self.assertEqual(custom_session.calls[0][2]["timeout"], (2, 8))
        self.assertEqual(default_session.calls[0][1], "https://api.cloudvps.reg.ru/v1/sizes")
        self.assertEqual(custom_session.calls[0][1], "https://api.cloudvps.reg.ru/v2/plans")

    def test_query_and_json_are_structured_and_host_is_not_manual(self):
        session = FakeSession()
        api = Api("x", session=session)
        api.v2.images.list("openstack-msk1", private=False)
        api.v1.ssh_keys.create("key", "ssh-ed25519 AAAA")

        image_call, key_call = session.calls
        self.assertEqual(image_call[2]["params"]["private"], False)
        self.assertNotIn("Host", image_call[2]["headers"])
        self.assertEqual(key_call[2]["json"]["name"], "key")

    def test_json_empty_and_text_success(self):
        session = FakeSession(
            [
                FakeResponse(payload={"value": 1}),
                FakeResponse(204, content=b""),
                FakeResponse(payload=ValueError(), text="kubeconfig", content=b"kubeconfig"),
            ]
        )
        api = Api("x", session=session)

        self.assertEqual(api.common.sizes(), {"value": 1})
        self.assertIsNone(api.v1.snapshots.delete(1))
        self.assertEqual(api.v1.kubernetes.get_kubeconfig(2), "kubeconfig")

    def test_structured_error_is_safe(self):
        token = "super-secret-token"
        session = FakeSession(
            [
                FakeResponse(
                    400,
                    {"code": "INVALID", "message": f"bad {token}"},
                    text=f"bad {token}",
                )
            ]
        )
        with self.assertRaises(CloudVpsAPIError) as raised:
            Api(token, session=session).common.sizes()

        self.assertEqual(raised.exception.status_code, 400)
        self.assertEqual(raised.exception.code, "INVALID")
        self.assertNotIn(token, str(raised.exception))
        self.assertNotIn(token, raised.exception.response_text)

    def test_non_json_error_preserves_status(self):
        session = FakeSession([FakeResponse(503, ValueError(), text="upstream unavailable")])
        with self.assertRaises(CloudVpsAPIError) as raised:
            Api("x", session=session).common.sizes()
        self.assertEqual(raised.exception.status_code, 503)
        self.assertIn("upstream unavailable", str(raised.exception))

    def test_transport_exception_is_not_retried(self):
        session = Mock()
        session.request.side_effect = requests.ConnectionError("down")
        with self.assertRaises(requests.ConnectionError):
            Api("x", session=session).v1.ssh_keys.create("name", "ssh-ed25519 AAAA")
        session.request.assert_called_once()

    def test_context_manager_closes_owned_session_only(self):
        supplied = FakeSession()
        with Api("x", session=supplied):
            pass
        self.assertEqual(supplied.closed, 0)

        owned = FakeSession()
        with patch("cloudvps.api.requests.Session", return_value=owned):
            with Api("x"):
                pass
        self.assertEqual(owned.closed, 1)

    def test_legacy_provider_warns_and_routes(self):
        session = FakeSession()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            api = Api("x", provider="example.test", session=session)
        api.common.sizes()
        self.assertEqual(session.calls[0][1], "https://example.test/v1/sizes")
        self.assertTrue(any(item.category is DeprecationWarning for item in caught))

    def test_invalid_configuration_fails_locally(self):
        with self.assertRaises(ValueError):
            Api("")
        with self.assertRaises(ValueError):
            Api("x", base_url="not-a-url")


if __name__ == "__main__":
    unittest.main()
