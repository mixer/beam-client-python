import unittest
from beam import Client
from beam.auth import PasswordAuth
from beam.errors import NotAuthenticatedError
from beam.services import UserService

class UserServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client().setUrl('http://localhost:1337/api/v%s/')
        self.client.auth(PasswordAuth('Sibyl53', 'password'))
        self.s = self.client.use(UserService)

    def test_gets_current_not_logged(self):
        with self.assertRaises(NotAuthenticatedError):
            client = Client().setUrl('http://localhost:1337/api/v%s/')
            client.use(UserService).current()

    def test_gets_current_successfully(self):
        result = self.s.current()
        self.assertEqual(2, result['id'])
