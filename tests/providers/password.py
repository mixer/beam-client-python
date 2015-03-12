import unittest
import requests
from unittest.mock import MagicMock
from beam import Client
from beam.auth import PasswordAuth
from beam.errors import AuthenticationFailedError

class PasswordAuthTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client().setUrl('http://localhost:1337/api/v%s/')

    def test_throws_on_invalid(self):
        with self.assertRaises(AuthenticationFailedError):
            PasswordAuth('foo', 'bar').use(self.client).attempt()

    def test_logs_successfully(self):
        PasswordAuth('Sibyl53', 'password').use(self.client).attempt()
        # should not throw an exception :)

    def test_shows_proper_auth_status_when_not_logged(self):
        auth = PasswordAuth('foo', 'bar')
        self.assertEqual(False, auth.authenticated())

        try:
            PasswordAuth('foo', 'bar').use(self.client).attempt()
        except:
            pass

        self.assertEqual(False, auth.authenticated())

    def test_shows_auth_when_successful(self):
        auth = PasswordAuth('Sibyl53', 'password')
        self.assertEqual(False, auth.authenticated())
        auth.use(self.client).attempt()
        self.assertEqual(True, auth.authenticated())

    def test_makes_requests_in_context(self):
        auth = PasswordAuth('Sibyl53', 'password')
        auth.use(self.client).attempt()
        result = auth.request('get', 'http://localhost:1337/api/v1/users/current')
        self.assertEqual(2, result.json()['id'])
