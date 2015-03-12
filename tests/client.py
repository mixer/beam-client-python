import unittest
from beam.client import Client

class ClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_builds_url(self):
        self.assertEqual(
            'https://beam.pro/api/v1/users/current',
            self.client._build_address('users/current')
        )
        self.assertEqual(
            'https://beam.pro/api/v1/users/current',
            self.client._build_address('/users/current')
        )

    def test_sets_api_version_and_url(self):
        self.client.setVersion(2).setUrl('http://localhost:1337/api/v%s/')

        self.assertEqual(
            'http://localhost:1337/api/v2/users/current',
            self.client._build_address('/users/current')
        )
