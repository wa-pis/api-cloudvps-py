from builtins import object


class Cloud(object):
    api = None
    path = None

    def __init__(self, api):
        self.api = api

    def list(self):
        pass

    def get(self):
        pass

    def create(self):
        pass

    def rename(self):
        pass

    def delete(self):
        pass

    def get_path(self):
        return self.path
