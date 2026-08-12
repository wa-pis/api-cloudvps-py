import json
import unittest
import warnings
from pathlib import Path
from urllib.parse import urlsplit

from cloudvps import Api, CloudVpsAPIError
from cloudvps.resources import Servers

from .helpers import FakeResponse, FakeSession


class ResourceContractTests(unittest.TestCase):
    def setUp(self):
        self.session = FakeSession()
        self.api = Api("fake-token", session=self.session)

    def test_every_manifest_operation_has_a_request_contract(self):
        api = self.api
        api.v1.feedback.account("user@example.test", "message")
        api.v1.feedback.hook("user@example.test", "message")
        api.v1.ssh_keys.list()
        api.v1.ssh_keys.create("key", "ssh-ed25519 AAAA")
        api.v1.ssh_keys.rename("1", "renamed")
        api.v1.ssh_keys.delete("1")
        api.v1.settings.get("balance_limit_notify")
        api.v1.settings.update("balance_limit_notify", 50)
        api.v1.actions.get(1)
        api.v1.billing.balance()
        api.v1.billing.history()
        api.v1.billing.prices()
        api.v1.history.list(limit=10, offset=2)
        api.v1.images.list(type="distribution", private=False, region="new-region")
        api.v1.ips.list(reglet_id=1)
        api.v1.ips.create(1, ipv4_count=1)
        api.v1.ips.update_ptr("192.0.2.1", "host.example.test")
        api.v1.ips.delete("2001:db8::1")
        api.v1.kubernetes.get_kubeconfig(1)
        api.v1.common.get_new_name()
        api.v1.common.sizes()
        api.v1.common.reglets_for_snapshot("snap-1")
        api.v1.servers.list()
        api.v1.servers.create("server", "size", "image")
        api.v1.servers.get(1)
        api.v1.servers.rename(1, "renamed")
        api.v1.servers.delete(1)
        api.v1.servers.reboot(1)
        api.v1.removed_servers.list()
        api.v1.snapshots.list(region="new-region")
        api.v1.snapshots.delete(1)
        api.v1.vpcs.list()
        api.v1.vpcs.create("network")
        api.v1.vpcs.get(1)
        api.v1.vpcs.rename(1, "renamed")
        api.v1.vpcs.delete(1)
        api.v1.vpcs.members(1)
        api.v1.vpcs.attach(1, 2)
        api.v1.vpcs.detach(1, 2)
        api.v2.images.list("new-region", private=True, type="custom")
        api.v2.plans.list("new-region", vcpus=2, plan_line="hp", unit="hour")

        actual = set()
        for method, url, _kwargs in self.session.calls:
            parts = urlsplit(url).path.split("/")
            version = parts[1]
            path = "/" + "/".join(parts[2:])
            actual.add((version, method, path))

        manifest = json.loads(
            (Path(__file__).parents[1] / "cloudvps" / "endpoints.json").read_text()
        )
        expected = set()
        for version, operations in manifest.items():
            for method, path in operations:
                values = {
                    "key_id": "1",
                    "settings_key": "balance_limit_notify",
                    "action_id": "1",
                    "ip": "192.0.2.1" if method == "PUT" else "2001:db8::1",
                    "k8s_cluster_id": "1",
                    "resource_id": "2" if "/members/" in path else "1",
                    "snapshot_id": "snap-1",
                    "image_id": "1",
                    "vpcs_id": "1",
                }
                expected.add((version, method, path.format(**values)))
        self.assertSetEqual(actual, expected)

    def test_server_create_minimal_and_full_payloads(self):
        self.api.v1.servers.create("name", "size", "image")
        self.api.v1.servers.create(size="size", image="image")
        self.api.v1.servers.create(
            "name",
            "size",
            10,
            [1, "fingerprint"],
            backups=False,
            floating_ip=False,
            isp_license_size="isp_lite6",
            promocode="promo",
            region_slug="future-region",
        )
        minimal = self.session.calls[0][2]["json"]
        unnamed = self.session.calls[1][2]["json"]
        full = self.session.calls[2][2]["json"]
        self.assertEqual(minimal, {"name": "name", "size": "size", "image": "image"})
        self.assertEqual(unnamed, {"size": "size", "image": "image"})
        self.assertEqual(full["ssh_keys"], [1, "fingerprint"])
        self.assertEqual(full["floating_ip"], False)

        with self.assertRaises(ValueError):
            self.api.v1.servers.create(size="size")

    def test_all_server_action_helpers_and_none_omission(self):
        servers = self.api.v1.servers
        helpers = {
            "start": lambda: servers.start(1),
            "stop": lambda: servers.stop(1),
            "reboot": lambda: servers.reboot(1),
            "rebuild": lambda: servers.rebuild(1, "image"),
            "password_reset": lambda: servers.password_reset(1),
            "resize": lambda: servers.resize(1, "size"),
            "generate_vnc_link": lambda: servers.generate_vnc_link(1),
            "snapshot": lambda: servers.snapshot(1),
            "enable_backups": lambda: servers.enable_backups(1),
            "disable_backups": lambda: servers.disable_backups(1),
            "restore": lambda: servers.restore(1, "backup"),
            "clone": lambda: servers.clone(1),
            "resize_isp_license": lambda: servers.resize_isp_license(1, "isp_lite6"),
        }
        self.assertSetEqual(set(helpers), Servers.ACTION_TYPES)
        for action_type, invoke in helpers.items():
            invoke()
            payload = self.session.calls[-1][2]["json"]
            self.assertEqual(payload["type"], action_type)
            self.assertNotIn(None, payload.values())
            self.assertNotEqual(payload.get("ssh_keys"), [None])

    def test_v2_pagination_is_not_implicit(self):
        envelope = {"plans": [{"slug": "small"}], "metadata": {"total": 1}}
        self.session.responses.append(FakeResponse(payload=envelope))
        result = self.api.v2.plans.list("new-region", page=2, items_per_page=10)
        self.assertIs(result, envelope)
        self.assertEqual(len(self.session.calls), 1)
        self.assertEqual(self.session.calls[0][2]["params"]["region"], "new-region")

    def test_empty_server_and_vpc_success_and_vpc_501(self):
        session = FakeSession(
            [
                FakeResponse(204, content=b""),
                FakeResponse(204, content=b""),
                FakeResponse(501, {"code": "NOT_IMPLEMENTED", "message": "not available"}),
            ]
        )
        api = Api("fake-token", session=session)

        self.assertIsNone(api.v1.servers.delete(1))
        self.assertIsNone(api.v1.vpcs.detach(2, 1))
        with self.assertRaises(CloudVpsAPIError) as raised:
            api.v1.vpcs.delete(2)
        self.assertEqual(raised.exception.status_code, 501)

    def test_vpc_attach_response_is_unchanged(self):
        response = {"action": {"id": "provider-action", "status": "in-progress"}}
        self.session.responses.append(FakeResponse(payload=response))
        self.assertIs(self.api.v1.vpcs.attach(1, 2), response)

    def test_representative_query_and_body_contracts(self):
        calls = (
            (lambda: self.api.v1.feedback.account("user@example.test", "hello")),
            (lambda: self.api.v1.settings.update("balance_limit_notify", 50)),
            (lambda: self.api.v1.history.list(limit=10, offset=2)),
            (lambda: self.api.v1.images.list(private=False, group="linux", region="future")),
            (lambda: self.api.v1.ips.create(7, ipv4_count=1, ipv6_count=0)),
            (lambda: self.api.v1.ips.update_ptr("2001:db8::1", "host.example.test")),
            (lambda: self.api.v1.vpcs.attach(3, 7)),
            (lambda: self.api.v2.plans.list("future", page=2, items_per_page=25, vcpus=4)),
        )
        for call in calls:
            call()

        self.assertEqual(
            self.session.calls[0][2]["json"],
            {"user_email": "user@example.test", "message": "hello"},
        )
        self.assertEqual(self.session.calls[1][2]["json"], {"value": 50})
        self.assertEqual(self.session.calls[2][2]["params"], {"limit": 10, "offset": 2})
        self.assertEqual(
            self.session.calls[3][2]["params"],
            {"private": False, "group": "linux", "region": "future"},
        )
        self.assertEqual(
            self.session.calls[4][2]["json"],
            {"reglet_id": 7, "ipv4_count": 1, "ipv6_count": 0},
        )
        self.assertEqual(self.session.calls[5][2]["json"], {"ptr": "host.example.test"})
        self.assertEqual(self.session.calls[6][2]["json"], {"resource_id": 7})
        self.assertEqual(
            self.session.calls[7][2]["params"],
            {"region": "future", "page": 2, "items_per_page": 25, "vcpus": 4},
        )

    def test_compatibility_aliases_and_legacy_failures(self):
        self.assertIs(self.api.ssh, self.api.v1.ssh_keys)
        self.assertIs(self.api.vps, self.api.v1.servers)
        self.assertIs(self.api.images, self.api.v1.images)
        removed = (
            lambda: self.api.common.estimate(),
            lambda: self.api.common.validate("name", "value"),
            lambda: self.api.actions.list(),
            lambda: self.api.history.get(1),
            lambda: self.api.images.get(1),
            lambda: self.api.images.rename(1, "name"),
            lambda: self.api.images.delete(1),
            lambda: self.api.snapshots.get(1),
            lambda: self.api.snapshots.rename(1, "name"),
            lambda: self.api.vps.get_vnc(1),
            lambda: self.api.vps.ptr(1, "host.example.test"),
        )
        before = len(self.session.calls)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            for invoke in removed:
                with self.assertRaises(NotImplementedError):
                    invoke()
        self.assertEqual(len(self.session.calls), before)
        self.assertEqual(len(caught), len(removed))
        self.assertTrue(all(item.category is DeprecationWarning for item in caught))

    def test_generic_action_rejects_unknown_action_locally(self):
        with self.assertRaises(ValueError):
            self.api.v1.servers.action(1, "future_action")
        self.assertFalse(self.session.calls)


if __name__ == "__main__":
    unittest.main()
