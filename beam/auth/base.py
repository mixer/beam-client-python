from ..errors import AuthenticationFailedError

class AuthBase():

    def __init__(self):
        self.client = None

    def _ensure_client(self):
        """
        Checks that the client is set for the authenticator, throwing an
        error if it isn't.
        """
        if self.client is None:
            this._fail('Client should have been defined, but wasn\'t!')

    def _fail(self, message):
        """
        Helper method to raise a new authentication failed error.
        """
        raise AuthenticationFailedError(message)

    def use(self, client):
        """
        Sets the client to use to authenticate.
        """
        self.client = client
        return self

    def authenticated(self):
        """
        Returns whether or not the user is currently authenticated.
        """
        return False

    def attempt(self):
        """
        Attempts to use the credentials given in a child class to auth to
        the beam service. It throws an error if it cannot do so.
        """
        raise NotImplementedError('attempt() should be implemented!')

    def request(self, method, route, **kwargs):
        """
        Runs a request to the Beam API using the authenticated context
        established be calling .attempt(). Returns a Requests response.
        """
        raise NotImplementedError('request is not implemented')
