from __future__ import absolute_import
from .base import Cloud


class Actions(Cloud):
    """
    Module for working with tasks for objects
    """

    path = "/actions"

    def __init__(self, api):
        super(Actions, self).__init__(api)

    def list(self):
        """
        Get list of active task
        """
        data = self.api.get(self.get_path())

        return data

    def get(self, object_id):
        """
        Get details by task id
        """
        full_path = "{0}/{1}".format(self.get_path(), object_id)
        data = self.api.get(full_path)

        return data
