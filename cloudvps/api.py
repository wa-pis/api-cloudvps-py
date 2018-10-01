from builtins import object
import requests
from . import objects


class Api(object):
    token = None
    provider = None
    host = None
    headers = {}
    url = None

    ssh = None
    common = None
    snapshots = None
    images = None
    actions = None
    vps = None

    def __init__(self, token, provider="api.cloudvps.reg.ru"):
        """
        Init api client
        """
        self.token = token
        self.host = provider
        self.set_headers()

        # initial main objects
        self.ssh = objects.ssh_keys.SshKeys(self)
        self.common = objects.common.Common(self)
        self.history = objects.history.History(self)
        self.snapshots = objects.snapshots.Snapshots(self)
        self.images = objects.images.Images(self)
        self.actions = objects.actions.Actions(self)
        self.vps = objects.vps.Vps(self)

    def set_headers(self):
        self.headers["Authorization"] = "Bearer {0}".format(self.token)
        self.headers["Content-Type"] = "application/json"
        self.headers["Host"] = self.host
        self.url = "https://{0}/v1".format(self.host)

    def get(self, path, object_id=None):
        """
        http wrapper for get request
        """
        data = requests.get(self.url + path, headers=self.headers)
        return data.json()

    def post(self, path, payload):
        """
        http wrapper for post request
        """
        data = requests.post(self.url + path, json=payload, headers=self.headers)
        return data.json()

    def put(self, path, payload):
        """
        http wrapper for put request
        """
        data = requests.put(self.url + path, json=payload, headers=self.headers)
        return data.json()

    def delete(self, path):
        """
        http wrapper for delete request
        """
        data = requests.delete(self.url + path, headers=self.headers)

        return data.status_code

    def get_path(self):
        return self.path
