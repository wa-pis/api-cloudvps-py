from __future__ import absolute_import
from .base import Cloud


class Vps(Cloud):
    """
    Module for work with servers
    """

    path = "/reglets"

    def __init__(self, api):
        super(Vps, self).__init__(api)

    def list(self):
        """
        Get server list
        """
        data = self.api.get(self.get_path())

        return data

    def action(self, path, payload):
        """
        Initiate action
        """
        full_path = "{0}/{1}/actions".format(self.get_path(), path)
        data = self.api.post(full_path, payload)

        return data

    def request_vnc(self, server_id):
        """
        Generate vnc token
        """
        payload = {"type": "generate_vnc_link"}

        return self.action(server_id, payload)

    def get_vnc(self, server_id):
        """
        Get vnc link
        """
        full_path = "{0}/{1}/{2}".format(self.get_path(), server_id, "vnc_link")
        data = self.api.get(full_path)

        return data

    def password_reset(self, server_id):
        """
        Reset server password
        """

        payload = {"type": "password_reset"}

        return self.action(server_id, payload)

    def reboot(self, server_id):
        """
        Reboot server
        """
        payload = {"type": "reboot"}

        return self.action(server_id, payload)

    def resize(self, server_id, size):
        """
        Change size of server
        """
        payload = {"type": "resize", "size": size}

        return self.action(server_id, payload)

    def snapshot(self, server_id, name=None):
        """
        Create snapshot of server
        """
        payload = {"type": "snapshot"}
        if name:
            payload["name"] = name

        return self.action(server_id, payload)

    def rebuild(self, server_id, image, ssh_keys=None):
        """
        Reinstall server
        """
        payload = {"type": "rebuild", "image": image}

        if type(ssh_keys) is list:
            payload["ssh_keys"] = ssh_keys
        else:
            payload["ssh_keys"] = []
            payload["ssh_keys"].append(ssh_keys)

        return self.action(server_id, payload)

    def create(self, name, size, image, ssh_keys=None):
        """
        Add new server
        require fields: name, size, image
        optional: ssh_keys - array of id or id
        """
        payload = {}
        payload["name"] = name
        payload["size"] = size
        payload["image"] = image
        payload["ssh_keys"] = ssh_keys

        data = self.api.post(self.get_path(), payload)

        return data

    def rename(self, server_id, name):
        """
        Rename server
        """
        payload = {"name": name}
        full_path = "{0}/{1}".format(self.get_path(), server_id)

        data = self.api.put(full_path, payload)

        return data

    def delete(self, server_id):
        """
        Delete server
        """
        full_path = "{0}/{1}".format(self.get_path(), server_id)
        data = self.api.delete(full_path)

        return data

    def ptr(self, server_id, ptr):
        """
        Set ptr for ip of the server
        """
        payload = {"ptr": ptr}
        full_path = "{0}/{1}/change_ptr".format(self.get_path(), server_id)

        return self.api.post(full_path, payload)
