import json
import unittest
from pathlib import Path

from cloudvps import Api

from .helpers import FakeSession


class CompatibilityFixtureTests(unittest.TestCase):
    def test_0_1_7_public_entry_points_remain_importable(self):
        fixture = json.loads((Path(__file__).parent / "fixtures" / "api_0_1_7.json").read_text())
        api = Api("fake-token", session=FakeSession())

        for method in fixture["low_level_methods"]:
            self.assertTrue(callable(getattr(api, method)))
        for resource_name, methods in fixture["resources"].items():
            resource = getattr(api, resource_name)
            for method in methods:
                self.assertTrue(callable(getattr(resource, method)))


if __name__ == "__main__":
    unittest.main()
