from __future__ import absolute_import
from .base import Cloud


class Images(Cloud):
    """
    Module for working with images
    """

    path = "/images"

    def __init__(self, api):
        super(Images, self).__init__(api)

    def list(self):
        data = self.api.get(self.get_path())

        return data

    def get(self, id):
        full_path = "{0}/{1}".format(self.get_path(), id)

        data = self.api.get(full_path)

        return data

    def get_application(self):
        return self.get("?type=application")

    def get_distribution(self):
        return self.get("?type=distribution")

    def get_private(self):
        return self.get("?private=true")

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
        Delete image
        """
        full_path = "{0}/{1}".format(self.get_path(), id)
        data = self.api.delete(full_path)

        return data
