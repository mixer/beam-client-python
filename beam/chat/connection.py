import requests
from .socket import Socket
from .errors import *
from .evented import Evented

class Connection(Evented):

    def __init__(self, config):
        Evented.__init__(self)

        self.config = config
        self.chat_details = None
        self.channel = None
        self.user_id = None


    # Returns the authentication body for logging in to Beam.
    def _get_auth_body(self):
        return {
            'username': self.config.USERNAME,
            'password': self.config.PASSWORD
        }


    # Creates an address to Beam with the given path.
    def _build_addr(self, path):
        return self.config.BEAM_ADDR + path


    # This is the HTTP component of the connection, that occurs
    # before we actually hit the chat server.
    def _log_into_beam(self):
        session = requests.Session()

        # First try to log in
        login_response = session.post(
            self._build_addr('/api/v1/users/login'),
            data=self._get_auth_body()
        )

        # Throw an error if the user login wasn't OK
        if login_response.status_code != requests.codes.ok:
            raise NotAuthenticatedError(login_response)

        self.user_id = login_response.json()['id']

        # Then request auth for the chat server
        chat_response = session.get(
            self._build_addr('/api/v1/chats/%s' % self.channel)
        )

        # If there's an error here... that should not be!
        if chat_response.status_code != requests.codes.ok:
            raise UnknownError(login_response)

        self.chat_details = chat_response.json()


    # This should be called after we login, and is responsible
    # for establishing the websocket component of the connection.
    def _connect_to_chat(self):
        if self.chat_details is None:
            raise Error('You must first log in to Beam!')

        self.ws = Socket(self.chat_details['endpoints'])
        self.ws.on('opened', self._send_auth_packet)
        self.ws.on('message', lambda msg: self.emit('message', msg))


    # Sends an authentication packet to the chat server.
    def _send_auth_packet(self):
        self.ws.send('method', self.channel, self.user_id,
            self.chat_details['authkey'], method='auth')


    # Logs into beam and connects to the chat server
    def authenticate(self, channel):
        self.channel = channel

        self._log_into_beam()
        self._connect_to_chat()

    # Sends a chat message.
    def message(self, msg):
        self.ws.send('method', msg, method='msg')

