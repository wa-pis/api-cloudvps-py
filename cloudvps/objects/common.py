from .base import Cloud


class Common(Cloud):
    """
    Common functions
    """

    def __init__(self, api):
        super(Common, self).__init__(api)

    def sizes(self):
        """
        Get all plans
        """
        data = self.api.get("/sizes")

        return data

    def get_new_name(self):
        """
        Get random name
        """
        data = self.api.get("/random_reglet_name")

        return data

    def estimate(self):
        """
        Get average time of operation
        """
        data = self.api.get("/estimate")

        return data

    def validate(self, param_name, value):
        """
        Validate parameter ( param_name : value )
        """
        payload = {param_name: value}

        data = self.api.post("/validate", payload)

        return data
