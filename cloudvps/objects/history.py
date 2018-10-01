from __future__ import absolute_import
from .base import Cloud


class History(Cloud):
    """
    Module for obtaining operation history
    """

    path = "/history"

    def __init__(self, api):
        super(History, self).__init__(api)

    def list(self):
        """
        Get all history
        """
        data = self.api.get(self.get_path())

        return data

    def get(self, object_id):
        """
        Get history by object_id
        """
        full_path = "{0}/{1}".format(self.get_path(), object_id)
        data = self.api.get(full_path)

        return data
