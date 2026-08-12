"""Opt-in live verification.

Set CLOUDVPS_TOKEN for read-only checks. Set CLOUDVPS_FULL_INTEGRATION=1 to
allow temporary paid resource creation and mutation. The full suite tracks and
best-effort deletes everything it creates.
"""

import os
import time
import unittest
import uuid

from cloudvps import Api, CloudVpsAPIError

TOKEN = os.environ.get("CLOUDVPS_TOKEN")
REGION = os.environ.get("CLOUDVPS_TEST_REGION", "openstack-sam1")
FULL = os.environ.get("CLOUDVPS_FULL_INTEGRATION") == "1"


def _find_value(value, keys):
    if isinstance(value, dict):
        for key in keys:
            if key in value and value[key] is not None:
                return value[key]
        for child in value.values():
            found = _find_value(child, keys)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = _find_value(child, keys)
            if found is not None:
                return found
    return None


@unittest.skipUnless(TOKEN, "CLOUDVPS_TOKEN is not set")
class ReadOnlyLiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = Api(TOKEN, timeout=(10, 60))

    @classmethod
    def tearDownClass(cls):
        cls.api.close()

    def test_read_only_account_and_catalog_surface(self):
        checks = {
            "sizes": self.api.v1.common.sizes,
            "random_name": self.api.v1.common.get_new_name,
            "servers": self.api.v1.servers.list,
            "images_v1": lambda: self.api.v1.images.list(region=REGION),
            "ips": self.api.v1.ips.list,
            "snapshots": lambda: self.api.v1.snapshots.list(region=REGION),
            "vpcs": self.api.v1.vpcs.list,
            "history": lambda: self.api.v1.history.list(limit=1, offset=0),
            "balance": self.api.v1.billing.balance,
            "billing_history": self.api.v1.billing.history,
            "prices": self.api.v1.billing.prices,
            "removed_servers": self.api.v1.removed_servers.list,
            "ssh_keys": self.api.v1.ssh_keys.list,
            "images_v2": lambda: self.api.v2.images.list(REGION, items_per_page=10),
            "plans_v2": lambda: self.api.v2.plans.list(REGION, items_per_page=10),
        }
        results = {}
        for name, check in checks.items():
            with self.subTest(name=name):
                results[name] = check()
                self.assertIsNotNone(results[name])
        print("Live read-only checks:", ", ".join(sorted(results)))


@unittest.skipUnless(TOKEN and FULL, "full live integration is not enabled")
class FullLifecycleLiveTests(unittest.TestCase):
    def setUp(self):
        self.api = Api(TOKEN, timeout=(10, 90))
        self.created = {"servers": [], "snapshots": [], "ips": [], "vpcs": [], "keys": []}
        self.cleanup_results = []
        self.name = f"api-cloudvps-py-{uuid.uuid4().hex[:8]}"

    def tearDown(self):
        for snapshot_id in reversed(self.created["snapshots"]):
            self._cleanup("snapshot", snapshot_id, self.api.v1.snapshots.delete)
        for ip in reversed(self.created["ips"]):
            self._cleanup("ip", ip, self.api.v1.ips.delete)
        for server_id in reversed(self.created["servers"]):
            self._cleanup("server", server_id, self.api.v1.servers.delete)
        for vpc_id in reversed(self.created["vpcs"]):
            self._cleanup("vpc", vpc_id, self.api.v1.vpcs.delete)
        for key_id in reversed(self.created["keys"]):
            self._cleanup("ssh-key", key_id, self.api.v1.ssh_keys.delete)
        self.api.close()
        print("Full integration resources:", self.created)
        print("Cleanup results:", self.cleanup_results)

    def _cleanup(self, kind, identifier, operation):
        try:
            operation(identifier)
            self.cleanup_results.append((kind, identifier, "deleted"))
        except Exception as error:  # cleanup must continue for every resource
            self.cleanup_results.append((kind, identifier, f"failed: {error}"))

    def _wait_action(self, result, timeout=600):
        action_id = _find_value(result, ("action_id",))
        if action_id is None and isinstance(result, dict) and "status" in result:
            action_id = result.get("id")
        if action_id is None:
            return result
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            action = self.api.v1.actions.get(action_id)
            status = _find_value(action, ("status",))
            if status == "completed":
                return action
            if status in {"errored", "failed"}:
                raise AssertionError(f"action {action_id} finished with {status}")
            time.sleep(5)
        raise TimeoutError(f"action {action_id} did not finish")

    def _wait_server(self, server_id, timeout=600):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                server = self.api.v1.servers.get(server_id)
                status = _find_value(server, ("status",))
                if status in {"active", "off"}:
                    return server
            except CloudVpsAPIError as error:
                if error.status_code != 404:
                    raise
            time.sleep(5)
        raise TimeoutError(f"server {server_id} did not become ready")

    def test_full_temporary_resource_lifecycle(self):
        public_key = os.environ.get("CLOUDVPS_TEST_PUBLIC_KEY")
        if not public_key:
            self.fail("CLOUDVPS_TEST_PUBLIC_KEY is required for full integration")

        key = self.api.v1.ssh_keys.create(self.name, public_key)
        key_id = _find_value(key, ("id", "fingerprint"))
        self.assertIsNotNone(key_id)
        self.created["keys"].append(key_id)
        self.api.v1.ssh_keys.rename(key_id, f"{self.name}-renamed")

        vpc = self.api.v1.vpcs.create(self.name)
        vpc_id = _find_value(vpc, ("resource_id", "id"))
        self.assertIsNotNone(vpc_id)
        self.created["vpcs"].append(vpc_id)
        self.api.v1.vpcs.rename(vpc_id, f"{self.name}-renamed")

        plans = self.api.v2.plans.list(REGION, items_per_page=10)
        images = self.api.v2.images.list(
            REGION, items_per_page=10, private=False, type="distribution"
        )
        plan_slug = os.environ.get("CLOUDVPS_TEST_PLAN") or _find_value(
            plans.get("plans", []), ("slug",)
        )
        image_slug = os.environ.get("CLOUDVPS_TEST_IMAGE") or _find_value(
            images.get("images", []), ("slug",)
        )
        self.assertTrue(plan_slug and image_slug)

        created = self.api.v1.servers.create(
            self.name,
            plan_slug,
            image_slug,
            [key_id],
            backups=False,
            floating_ip=True,
            region_slug=REGION,
        )
        server_id = _find_value(created.get("reglet", created), ("id", "resource_id"))
        self.assertIsNotNone(server_id)
        self.created["servers"].append(server_id)
        self._wait_action(created)
        self._wait_server(server_id)

        self.api.v1.servers.rename(server_id, f"{self.name}-renamed")
        self._wait_action(self.api.v1.vpcs.attach(vpc_id, server_id))
        self.assertIn(server_id, self.api.v1.vpcs.members(vpc_id))
        self.api.v1.vpcs.detach(vpc_id, server_id)

        for action in (
            self.api.v1.servers.stop,
            self.api.v1.servers.start,
            self.api.v1.servers.reboot,
            self.api.v1.servers.password_reset,
            self.api.v1.servers.enable_backups,
            self.api.v1.servers.disable_backups,
        ):
            self._wait_action(action(server_id))

        self._wait_action(self.api.v1.servers.resize(server_id, plan_slug))
        self._wait_action(self.api.v1.servers.generate_vnc_link(server_id))
        self._wait_action(self.api.v1.servers.rebuild(server_id, image_slug, [key_id]))

        snapshot_result = self.api.v1.servers.snapshot(
            server_id, f"{self.name}-snapshot", offline=True
        )
        self._wait_action(snapshot_result)
        snapshots = self.api.v1.snapshots.list(region=REGION)
        snapshot_id = _find_value(snapshots, ("id",))
        if snapshot_id is not None:
            self.created["snapshots"].append(snapshot_id)

        ip_result = self.api.v1.ips.create(server_id, ipv4_count=1)
        self._wait_action(ip_result)
        ips = self.api.v1.ips.list(reglet_id=server_id)
        ip = _find_value(ips, ("ip",))
        if ip:
            self.created["ips"].append(ip)
            self.api.v1.ips.update_ptr(ip, f"test-{uuid.uuid4().hex[:8]}.example.test")

        clone_result = self.api.v1.servers.clone(server_id, f"{self.name}-clone", offline=True)
        self._wait_action(clone_result)
        clone_id = _find_value(clone_result, ("resource_id", "reglet_id"))
        if clone_id and clone_id != server_id:
            self.created["servers"].append(clone_id)

        backup_image = os.environ.get("CLOUDVPS_TEST_BACKUP_IMAGE")
        if backup_image:
            self._wait_action(
                self.api.v1.servers.restore(server_id, backup_image, ssh_keys=[key_id])
            )

        license_size = os.environ.get("CLOUDVPS_TEST_ISP_LICENSE")
        if license_size:
            self._wait_action(self.api.v1.servers.resize_isp_license(server_id, license_size))


if __name__ == "__main__":
    unittest.main()
