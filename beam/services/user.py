from requests import codes
from .service import Service
from ..errors import NotAuthenticatedError

class UserService(Service):

    def current(self):
        return self._handle_response(
            self.client.request('get', 'users/current'),
            { codes.bad_request: NotAuthenticatedError }
        )
