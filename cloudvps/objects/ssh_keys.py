from __future__ import absolute_import
from .base import Cloud


class SshKeys(Cloud):
    """
    Module for ssh keys storage
    """

    path = "/account/keys"

    def __init__(self, api):
        super(SshKeys, self).__init__(api)

    def list(self):

        data = self.api.get(self.get_path())

        return data

    def create(self, name, public_key):
        """
        Add new ssh-key
        require fields: name, public_key
        """
        payload = {}
        payload["name"] = name
        payload["public_key"] = public_key

        data = self.api.post(self.get_path(), payload)

        return data

    def rename(self, id, name):
        """
        Change name of ssh key
        """
        payload = {"name": name}
        full_path = "{0}/{1}".format(self.get_path(), id)

        data = self.api.put(full_path, payload)

        return data

    def delete(self, id):
        """
        Delete key from key-storage
        """
        full_path = "{0}/{1}".format(self.get_path(), id)
        data = self.api.delete(full_path)

        return data
