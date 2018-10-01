from __future__ import absolute_import
from .base import Cloud


class Snapshots(Cloud):
    """
    Module for snapshot operations
    """

    path = "/snapshots"

    def __init__(self, api):
        super(Snapshots, self).__init__(api)

    def list(self):
        data = self.api.get(self.get_path())

        return data

    def get(self, id):
        full_path = "{0}/{1}".format(self.get_path(), id)
        data = self.api.get(full_path)

        return data

    def rename(self, id, name):
        """
        Change name of snapshot
        """
        payload = {"name": name}
        full_path = "{0}/{1}".format(self.get_path(), id)

        data = self.api.put(full_path, payload)

        return data

    def delete(self, id):
        """
        Delete snapshot
        """
        full_path = "{0}/{1}".format(self.get_path(), id)
        data = self.api.delete(full_path)

        return data
