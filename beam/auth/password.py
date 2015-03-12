import requests
from .base import AuthBase
from ..errors import AuthenticationFailedError

class PasswordAuth(AuthBase):

    def __init__(self, username, password, twofactor=None):
        """
        Creates a new password-based authentication provider. The username
        and password you want to use to authenticate with should be passed
        into here. If the user has two-factor enabled, you should also
        pass in their code.
        """
        super(PasswordAuth, self)

        self.credentials = {
            'username': username,
            'password': password,
            'code': twofactor
        }

        # The requests session to use
        self.session = None

    def authenticated(self):
        """
        Returns whether or not the user is currently authenticated.
        """
        return self.session is not None

    def attempt(self):
        """
        Attempts to use the credentials given in a child class to auth to
        the beam service. It throws an error if it cannot do so.
        """
        self._ensure_client()
        self.session = requests.Session()

        response = self.session.post(
            self.client._build_address('users/login'),
            data=self.credentials
        )

        if response.status_code != requests.codes.ok:
            self.session = None
            self._fail('Invalid username or password.')

    def request(self, method, *args, **kwargs):
        """
        Runs a request to the Beam API using the authenticated context
        established be calling .attempt().
        """
        if self.session is None:
            self._fail('Attempted to make a request while not authenticated.')

        return getattr(self.session, method)(*args, **kwargs)
