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


def _find_named(value, name):
    if isinstance(value, dict):
        if value.get("name") == name:
            return value
        for child in value.values():
            found = _find_named(child, name)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = _find_named(child, name)
            if found is not None:
                return found
    return None


def _contains_value(value, expected):
    if value == expected:
        return True
    if isinstance(value, dict):
        return any(_contains_value(child, expected) for child in value.values())
    if isinstance(value, list):
        return any(_contains_value(child, expected) for child in value)
    return False


def _find_action(value):
    if not isinstance(value, dict):
        return None
    action = value.get("action")
    if isinstance(action, dict):
        return action
    actions = value.get("links", {}).get("actions", [])
    if isinstance(actions, list) and actions:
        return actions[0]
    if "status" in value and "id" in value:
        return value
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
        self.name = os.environ.get("CLOUDVPS_TEST_NAME", f"api-cloudvps-py-{uuid.uuid4().hex[:8]}")
        self.key_name = self.name.replace("-", "")

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
        except CloudVpsAPIError as error:
            expected = kind == "vpc" and error.status_code == 501
            status = "not supported" if expected else f"failed: {error}"
            self.cleanup_results.append((kind, identifier, status))
        except Exception as error:  # cleanup must continue for every resource
            self.cleanup_results.append((kind, identifier, f"failed: {error}"))

    def _wait_action(self, result, timeout=600):
        action = _find_action(result)
        if action is None:
            return result
        action_id = action.get("id")
        if action_id is None:
            return action
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            action = _find_action(self.api.v1.actions.get(action_id))
            if action is None:
                raise AssertionError(f"action {action_id} response has no action")
            status = action.get("status", "").replace("_", "-")
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
                locked = bool(_find_value(server, ("locked",)))
                if status in {"active", "off"} and not locked:
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

        key = self.api.v1.ssh_keys.create(self.key_name, public_key)
        key_id = _find_value(key, ("id", "fingerprint"))
        self.assertIsNotNone(key_id)
        self.created["keys"].append(key_id)
        self.api.v1.ssh_keys.rename(key_id, f"{self.key_name}renamed")

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
        self._wait_server(server_id)
        self.assertTrue(_contains_value(self.api.v1.vpcs.members(vpc_id), server_id))
        self._wait_action(self.api.v1.vpcs.detach(vpc_id, server_id))
        self._wait_server(server_id)

        for action in (
            self.api.v1.servers.stop,
            self.api.v1.servers.start,
            self.api.v1.servers.reboot,
            self.api.v1.servers.password_reset,
            self.api.v1.servers.enable_backups,
            self.api.v1.servers.disable_backups,
        ):
            self._wait_action(action(server_id))
            self._wait_server(server_id)

        self._wait_action(self.api.v1.servers.resize(server_id, plan_slug))
        self._wait_server(server_id)
        self._wait_action(self.api.v1.servers.generate_vnc_link(server_id))
        self._wait_server(server_id)
        self._wait_action(self.api.v1.servers.rebuild(server_id, image_slug, [key_id]))
        self._wait_server(server_id)

        snapshot_name = f"{self.name}-snapshot"
        snapshot_action = self._wait_action(
            self.api.v1.servers.snapshot(server_id, snapshot_name, offline=True)
        )
        snapshot_id = _find_value(snapshot_action, ("resource_id", "snapshot_id", "image_id"))
        if snapshot_id is None:
            snapshot = _find_named(self.api.v1.snapshots.list(region=REGION), snapshot_name)
            snapshot_id = _find_value(snapshot, ("id",))
        self.assertIsNotNone(snapshot_id)
        self.created["snapshots"].append(snapshot_id)

        ip_result = self.api.v1.ips.create(server_id, ipv4_count=1)
        self._wait_action(ip_result)
        ips = self.api.v1.ips.list(reglet_id=server_id)
        ip = _find_value(ips, ("ip",))
        if ip:
            self.created["ips"].append(ip)
            self.api.v1.ips.update_ptr(ip, f"test-{uuid.uuid4().hex[:8]}.example.test")

        clone_name = f"{self.name}-clone"
        clone_action = self._wait_action(
            self.api.v1.servers.clone(server_id, clone_name, offline=True)
        )
        clone_id = _find_value(clone_action, ("resource_id", "reglet_id"))
        if clone_id is None:
            clone = _find_named(self.api.v1.servers.list(), clone_name)
            clone_id = _find_value(clone, ("id", "resource_id"))
        self.assertIsNotNone(clone_id)
        if clone_id != server_id:
            self.created["servers"].append(clone_id)

        backup_image = os.environ.get("CLOUDVPS_TEST_BACKUP_IMAGE")
        if backup_image:
            self._wait_action(
                self.api.v1.servers.restore(server_id, backup_image, ssh_keys=[key_id])
            )

        license_size = os.environ.get("CLOUDVPS_TEST_ISP_LICENSE")
        if license_size:
            self._wait_action(self.api.v1.servers.resize_isp_license(server_id, license_size))


class LiveResponseParsingTests(unittest.TestCase):
    def test_find_action_supports_openapi_response_shapes(self):
        action = {"id": "123", "status": "in_progress"}
        self.assertIs(_find_action({"action": action}), action)
        self.assertIs(_find_action({"links": {"actions": [action]}}), action)
        self.assertIs(_find_action(action), action)
        self.assertIsNone(_find_action({"links": {"actions": []}}))


if __name__ == "__main__":
    unittest.main()
