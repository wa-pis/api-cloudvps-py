import warnings
from importlib.metadata import PackageNotFoundError, version


def package_version():
    try:
        return version("api-cloudvps-py")
    except PackageNotFoundError:
        return "0+unknown"


def _clean(values):
    return {key: value for key, value in values.items() if value is not None}


def _removed(name, replacement=None):
    message = f"{name} targets an endpoint absent from the current CloudVPS OpenAPI contract"
    if replacement:
        message += f"; use {replacement}"
    warnings.warn(message, DeprecationWarning, stacklevel=3)
    raise NotImplementedError(message)


class Resource:
    version = "v1"

    def __init__(self, api):
        self.api = api

    def _request(self, method, path, *, params=None, payload=None):
        return self.api.request(
            method,
            path,
            version=self.version,
            params=_clean(params or {}),
            json=payload,
        )


class Feedback(Resource):
    def account(self, user_email, message):
        return self._request(
            "POST", "/account/feedback", payload={"user_email": user_email, "message": message}
        )

    def hook(self, user_email, message):
        return self._request(
            "POST", "/feedback", payload={"user_email": user_email, "message": message}
        )


class SshKeys(Resource):
    def list(self):
        return self._request("GET", "/account/keys")

    def create(self, name, public_key):
        return self._request(
            "POST", "/account/keys", payload={"name": name, "public_key": public_key}
        )

    def rename(self, key_id, name):
        return self._request("PUT", f"/account/keys/{key_id}", payload={"name": name})

    def delete(self, key_id):
        return self._request("DELETE", f"/account/keys/{key_id}")


class Settings(Resource):
    def get(self, settings_key):
        return self._request("GET", f"/account/settings/{settings_key}")

    def update(self, settings_key, value):
        return self._request("PUT", f"/account/settings/{settings_key}", payload={"value": value})


class Actions(Resource):
    def get(self, action_id):
        return self._request("GET", f"/actions/{action_id}")

    def list(self):
        return _removed("actions.list")


class Billing(Resource):
    def balance(self):
        return self._request("GET", "/balance_data")

    def history(self):
        return self._request("GET", "/billing_history")

    def prices(self):
        return self._request("GET", "/prices")


class History(Resource):
    def list(self, *, limit=None, offset=None):
        return self._request("GET", "/history", params={"limit": limit, "offset": offset})

    def get(self, object_id):
        del object_id
        return _removed("history.get")


class ImagesV1(Resource):
    def list(self, *, type=None, private=None, reglet_id=None, group=None, region=None):
        return self._request(
            "GET",
            "/images",
            params={
                "type": type,
                "private": private,
                "reglet_id": reglet_id,
                "group": group,
                "region": region,
            },
        )

    def get_application(self):
        return self.list(type="application")

    def get_distribution(self):
        return self.list(type="distribution")

    def get_private(self):
        return self.list(private=True)

    def get(self, image_id):
        del image_id
        return _removed("images.get")

    def rename(self, image_id, name):
        del image_id, name
        return _removed("images.rename")

    def delete(self, image_id):
        del image_id
        return _removed("images.delete", "api.v1.snapshots.delete(image_id)")


class IPs(Resource):
    def list(self, *, reglet_id=None):
        return self._request("GET", "/ips", params={"reglet_id": reglet_id})

    def create(self, reglet_id, *, ipv4_count=None, ipv6_count=None):
        return self._request(
            "POST",
            "/ips",
            payload=_clean(
                {"reglet_id": reglet_id, "ipv4_count": ipv4_count, "ipv6_count": ipv6_count}
            ),
        )

    def update_ptr(self, ip, ptr):
        return self._request("PUT", f"/ips/{ip}", payload={"ptr": ptr})

    def delete(self, ip):
        return self._request("DELETE", f"/ips/{ip}")


class Kubernetes(Resource):
    def get_kubeconfig(self, cluster_id):
        return self._request("GET", f"/k8s_clusters/{cluster_id}/get_kubeconfig")


class Common(Resource):
    def sizes(self):
        return self._request("GET", "/sizes")

    def get_new_name(self):
        return self._request("GET", "/random_reglet_name")

    def reglets_for_snapshot(self, snapshot_id):
        return self._request("GET", f"/reglets_for_snapshot/{snapshot_id}")

    def estimate(self):
        return _removed("common.estimate")

    def validate(self, param_name, value):
        del param_name, value
        return _removed("common.validate")


class Servers(Resource):
    ACTION_TYPES = {
        "start",
        "stop",
        "reboot",
        "rebuild",
        "password_reset",
        "resize",
        "generate_vnc_link",
        "snapshot",
        "enable_backups",
        "disable_backups",
        "restore",
        "clone",
        "resize_isp_license",
    }

    def list(self):
        return self._request("GET", "/reglets")

    def get(self, server_id):
        return self._request("GET", f"/reglets/{server_id}")

    def create(
        self,
        name=None,
        size=None,
        image=None,
        ssh_keys=None,
        *,
        backups=None,
        floating_ip=None,
        isp_license_size=None,
        promocode=None,
        region_slug=None,
    ):
        if size is None or image is None:
            raise ValueError("size and image are required")
        payload = _clean(
            {
                "name": name,
                "size": size,
                "image": image,
                "ssh_keys": ssh_keys,
                "backups": backups,
                "floating_ip": floating_ip,
                "isp_license_size": isp_license_size,
                "promocode": promocode,
                "region_slug": region_slug,
            }
        )
        return self._request("POST", "/reglets", payload=payload)

    def rename(self, server_id, name):
        return self._request("PUT", f"/reglets/{server_id}", payload={"name": name})

    def delete(self, server_id):
        return self._request("DELETE", f"/reglets/{server_id}")

    def action(self, server_id, action_type=None, **fields):
        # Accept the old action(server_id, {payload}) form as well.
        if isinstance(action_type, dict):
            payload = dict(action_type)
        else:
            payload = _clean({"type": action_type, **fields})
        if payload.get("type") not in self.ACTION_TYPES:
            raise ValueError(f"unsupported server action: {payload.get('type')!r}")
        return self._request("POST", f"/reglets/{server_id}/actions", payload=payload)

    def start(self, server_id):
        return self.action(server_id, "start")

    def stop(self, server_id):
        return self.action(server_id, "stop")

    def reboot(self, server_id):
        return self.action(server_id, "reboot")

    def rebuild(self, server_id, image, ssh_keys=None, *, isp_license_size=None):
        return self.action(
            server_id,
            "rebuild",
            image=image,
            ssh_keys=ssh_keys,
            isp_license_size=isp_license_size,
        )

    def password_reset(self, server_id):
        return self.action(server_id, "password_reset")

    def resize(self, server_id, size):
        return self.action(server_id, "resize", size=size)

    def generate_vnc_link(self, server_id):
        return self.action(server_id, "generate_vnc_link")

    request_vnc = generate_vnc_link

    def snapshot(self, server_id, name=None, *, offline=None):
        return self.action(server_id, "snapshot", name=name, offline=offline)

    def enable_backups(self, server_id):
        return self.action(server_id, "enable_backups")

    def disable_backups(self, server_id):
        return self.action(server_id, "disable_backups")

    def restore(self, server_id, image, *, ssh_keys=None):
        return self.action(server_id, "restore", image=image, ssh_keys=ssh_keys)

    def clone(self, server_id, name=None, *, offline=None):
        return self.action(server_id, "clone", name=name, offline=offline)

    def resize_isp_license(self, server_id, isp_license_size):
        return self.action(server_id, "resize_isp_license", isp_license_size=isp_license_size)

    def get_vnc(self, server_id):
        del server_id
        return _removed("vps.get_vnc", "vps.request_vnc(server_id)")

    def ptr(self, server_id, ptr):
        del server_id, ptr
        return _removed("vps.ptr", "api.v1.ips.update_ptr(ip, ptr)")


class RemovedServers(Resource):
    def list(self):
        return self._request("GET", "/removed_servers")


class Snapshots(Resource):
    def list(self, *, region=None):
        return self._request("GET", "/snapshots", params={"region": region})

    def delete(self, image_id):
        return self._request("DELETE", f"/snapshots/{image_id}")

    def get(self, image_id):
        del image_id
        return _removed("snapshots.get")

    def rename(self, image_id, name):
        del image_id, name
        return _removed("snapshots.rename")


class Vpcs(Resource):
    def list(self):
        return self._request("GET", "/vpcs")

    def create(self, name):
        return self._request("POST", "/vpcs", payload={"name": name})

    def get(self, vpcs_id):
        return self._request("GET", f"/vpcs/{vpcs_id}")

    def rename(self, vpcs_id, name):
        return self._request("PUT", f"/vpcs/{vpcs_id}", payload={"name": name})

    def delete(self, vpcs_id):
        return self._request("DELETE", f"/vpcs/{vpcs_id}")

    def members(self, vpcs_id):
        return self._request("GET", f"/vpcs/{vpcs_id}/members")

    def attach(self, vpcs_id, resource_id):
        return self._request(
            "POST", f"/vpcs/{vpcs_id}/members", payload={"resource_id": resource_id}
        )

    def detach(self, vpcs_id, resource_id):
        return self._request("DELETE", f"/vpcs/{vpcs_id}/members/{resource_id}")


class ImagesV2(Resource):
    version = "v2"

    def list(self, region, page=1, items_per_page=100, *, private=None, type=None):
        return self._request(
            "GET",
            "/images",
            params={
                "region": region,
                "page": page,
                "items_per_page": items_per_page,
                "private": private,
                "type": type,
            },
        )


class PlansV2(Resource):
    version = "v2"

    def list(
        self,
        region,
        page=1,
        items_per_page=100,
        *,
        vcpus=None,
        disk=None,
        memory=None,
        plan_line=None,
        unit=None,
    ):
        return self._request(
            "GET",
            "/plans",
            params={
                "region": region,
                "page": page,
                "items_per_page": items_per_page,
                "vcpus": vcpus,
                "disk": disk,
                "memory": memory,
                "plan_line": plan_line,
                "unit": unit,
            },
        )


class V1:
    def __init__(self, api):
        self.feedback = Feedback(api)
        self.ssh_keys = SshKeys(api)
        self.settings = Settings(api)
        self.actions = Actions(api)
        self.billing = Billing(api)
        self.history = History(api)
        self.images = ImagesV1(api)
        self.ips = IPs(api)
        self.kubernetes = Kubernetes(api)
        self.common = Common(api)
        self.servers = Servers(api)
        self.removed_servers = RemovedServers(api)
        self.snapshots = Snapshots(api)
        self.vpcs = Vpcs(api)


class V2:
    def __init__(self, api):
        self.images = ImagesV2(api)
        self.plans = PlansV2(api)
