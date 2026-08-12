class Cloud:
    """Compatibility base class retained for 0.2.x imports."""

    path = None

    def __init__(self, api):
        self.api = api

    def get_path(self):
        return self.path
