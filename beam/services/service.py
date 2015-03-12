from requests import codes
from ..errors import UnknownCodeError

class Service():

    def __init__(self, client):
        """
        Creates a new service based on the given client.
        """
        self.client = client

    def _handle_response(self, response, mapping={}):
        """
        Handles a requests response. If it's OK, it'll return the result
        as JSON. Otherwise it'll see if the error code is defined in the
        mapping dict and, if not, just raise a generic error.
        """

        code = response.status_code
        if code == codes.ok:
            return response.json()
        elif code in mapping:
            raise mapping[code](response)
        else:
            raise UnknownCodeError(response)
