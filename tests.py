import unittest
import cloudvps


class CloudTestCase(unittest.TestCase):
    def setUp(self):
        self.api = cloudvps.Api("some_fake_token")

    def testCheckVersion(self):
        self.assertEqual(cloudvps.__version__, "0.1.4")

    def testHelpfullFunction(self):
        pass


if __name__ == "__main__":
    unittest.main()
