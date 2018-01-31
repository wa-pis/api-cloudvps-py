import unittest
import cloudvps

class CloudTestCase(unittest.TestCase):

    def setUp(self):
        self.api = cloudvps.Api('some_fake_token')

    def testHelpfullFunction(self):
        pass

if __name__ == "__main__":
    unittest.main()
