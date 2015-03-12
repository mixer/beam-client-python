import unittest
import requests
from unittest.mock import MagicMock
from beam.client import Client
from beam.auth import AuthBase

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client().setUrl('http://localhost:1337/api/v%s/')

    def test_gets_when_not_authed(self):
        result = self.client.request('get', 'users/current')
        self.assertEqual(requests.codes.bad_request, result.status_code)

    def test_calls_provider_when_authed(self):
        self.client._provider.authenticated = lambda: True

        mock = MagicMock(return_value='request here')
        self.client._provider.request = mock

        self.assertEqual('request here', self.client.request('get', 'foo/bar'))
        mock.assert_called_with('get', 'http://localhost:1337/api/v1/foo/bar')

    def test_calls_used_provide(self):
        auth = AuthBase()
        provideMock = MagicMock()
        useMock = MagicMock(return_value=provideMock)
        auth.use = useMock

        self.client.auth(auth)
        useMock.assert_called_with(self.client)
        provideMock.assert_called()
